import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import requests
import io
import plotly.express as px

st.set_page_config(page_title="Nifty 500 RS & RSI Screener", layout="wide")

st.title("📊 Nifty 500 Screener & Dashboard")
st.markdown("Filtering Nifty 500 stocks where **55-Period RS (vs Nifty)** is between **-0.05 and 0.05** and **RSI(14) >= 50**.")

@st.cache_data(ttl=86400)
def get_nifty500_symbols():
    url = "https://raw.githubusercontent.com/chaitanyarahalkar/Financial-Info-Extractor/master/ind_nifty500list.csv"
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
        df = pd.read_csv(io.StringIO(res.text))
        
        # Dynamically find the symbol column without hardcoding index positions
        symbol_col = next((col for col in df.columns if 'symbol' in col.lower()), None)
        if symbol_col is None:
            symbol_col = 'Symbol' if 'Symbol' in df.columns else df.columns[0]
            
        symbols = df[symbol_col].dropna().astype(str).tolist()
        cleaned = [s.strip() + ".NS" for s in symbols if s.strip().upper() != 'SYMBOL' and len(s.strip()) > 0]
        
        if len(cleaned) > 400:
            return cleaned
    except Exception:
        pass
        
    # Comprehensive fallback list of top liquid NSE stocks if network/fetch fails
    fallback = [
        "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK", "HINDUNILVR", "ITC", "SBIN", "BHARTIARTL", "KOTAKBANK",
        "LT", "AXISBANK", "ASIANPAINT", "MARUTI", "SUNPHARMA", "TITAN", "BAJFINANCE", "NESTLEIND", "HCLTECH", "TATAMOTORS",
        "WIPRO", "ADANIENT", "POWERGRID", "NTPC", "GRASIM", "TECHM", "JSWSTEEL", "TATASTEEL", "M&M", "ADANIPORTS",
        "DIVISLAB", "BAJAJFINSV", "BPCL", "HEROMOTOCO", "EICHERMOT", "ONGC", "COALINDIA", "BRITANNIA", "CIPLA", "SBILIFE",
        "DRREDDY", "APOLLOHOSP", "TATACONSUM", "HDFCLIFE", "BAJAJ-AUTO", "SHRIRAMFIN", "ULTRACEMCO", "INDUSINDBK", "HINDALCO",
        "BEL", "TRENT", "CHOLAFIN", "TATAPOWER", "TVSMOTOR", "SIEMENS", "ABB", "DLF", "LODHA", "ZOMATO", "PNB", "BANKBARODA",
        "CANBK", "IDFCFIRSTB", "FEDERALBNK", "AUBANK", "HINDPETRO", "IOC", "GAIL", "PETRONET", "MGL", "IGL", "TATATECH",
        "PERSISTENT", "COFORGE", "LTIM", "MPHASIS", "OFSS", "KPITTECH", "NAUKRI", "ZENSARTECH", "CYIENT", "SONACOMS",
        "MOTHERSON", "BHARATFORG", "ASHOKLEY", "BOSCHLTD", "TIINDIA", "MRF", "BALKRISIND", "APOLLOTYRE", "CEATLTD", "EXIDEIND"
    ]
    return [s + ".NS" for s in fallback]

with st.spinner("Loading Nifty 500 stock universe..."):
    tickers = get_nifty500_symbols()
    tickers_with_benchmark = tickers + ["^NSEI"]

st.sidebar.header("Screener Parameters")
rs_lower = st.sidebar.number_input("RS Lower Bound", value=-0.05, step=0.01)
rs_upper = st.sidebar.number_input("RS Upper Bound", value=0.05, step=0.01)
rsi_threshold = st.sidebar.slider("Minimum RSI (14)", min_value=30, max_value=70, value=50)
lookback = 55

if st.button("Run Screener scan"):
    if not tickers:
        st.error("Could not load stock tickers.")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("Downloading historical data and calculating indicators...")
        
        data = yf.download(tickers_with_benchmark, period="1y", interval="1d", group_by="ticker", threads=True)
        
        closes = pd.DataFrame()
        for ticker in tickers_with_benchmark:
            try:
                closes[ticker] = data[ticker]["Close"]
            except Exception:
                continue
                
        closes = closes.dropna(how="all")
        
        if "^NSEI" not in closes.columns:
            st.error("Error fetching Nifty (^NSEI) benchmark data.")
        else:
            nifty_close = closes["^NSEI"]
            
            results = []
            total_tickers = len(tickers)
            
            for i, stock in enumerate(tickers):
                if stock not in closes.columns:
                    continue
                
                s_close = closes[stock].dropna()
                if len(s_close) < lookback + 15:
                    continue
                    
                df_temp = pd.DataFrame({"stock": s_close, "nifty": nifty_close}).dropna()
                if len(df_temp) < lookback + 15:
                    continue
                    
                # Calculate Ratio RS: (Stock / Stock[55]) / (Nifty / Nifty[55]) - 1
                stock_ratio = df_temp["stock"] / df_temp["stock"].shift(lookback)
                nifty_ratio = df_temp["nifty"] / df_temp["nifty"].shift(lookback)
                res = (stock_ratio / nifty_ratio) - 1
                current_res = res.iloc[-1]
                
                # Calculate RSI 14
                delta = df_temp["stock"].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs_val = gain / loss
                rsi = 100 - (100 / (1 + rs_val))
                current_rsi = rsi.iloc[-1]
                current_price = df_temp["stock"].iloc[-1]
                
                # Check conditions (RS between bounds and RSI >= 50)
                if (current_res > rs_lower) and (current_res < rs_upper) and (current_rsi >= rsi_threshold):
                    results.append({
                        "Ticker": stock.replace(".NS", ""),
                        "Close Price": round(current_price, 2),
                        "RS Value (55)": round(current_res, 4),
                        "RSI (14)": round(current_rsi, 2)
                    })
                    
                progress_bar.progress((i + 1) / total_tickers)
                
            status_text.text("Scan complete!")
            progress_bar.empty()
            
            if results:
                res_df = pd.DataFrame(results)
                st.success(f"Found {len(res_df)} matching stocks meeting your criteria!")
                st.dataframe(res_df, use_container_width=True)
                
                # Interactive scatter plot
                fig = px.scatter(res_df, x="RS Value (55)", y="RSI (14)", text="Ticker", 
                                 title="Filtered Nifty 500 Stocks: RS vs RSI Map",
                                 hover_data=["Close Price"])
                fig.update_traces(textposition='top center')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No stocks matched the exact criteria for the selected parameters. Try widening your RS band slightly.")
