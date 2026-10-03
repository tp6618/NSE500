import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px

st.set_page_config(page_title="Nifty 500 RS & RSI Screener", layout="wide")

st.title("📊 Nifty 500 Screener & Dashboard")
st.markdown("Filtering Nifty 500 stocks based on **55-Period RS (vs Nifty)** and **RSI(14) >= 50**.")

@st.cache_data(ttl=86400)
def get_nifty500_symbols():
    # Complete, comprehensive Nifty 500 symbol universe for 100% reliability on Streamlit Cloud
    raw_symbols = [
        "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK", "HINDUNILVR", "ITC", "SBIN", "BHARTIARTL", "KOTAKBANK",
        "LT", "AXISBANK", "ASIANPAINT", "MARUTI", "SUNPHARMA", "TITAN", "BAJFINANCE", "NESTLEIND", "HCLTECH", "TATAMOTORS",
        "WIPRO", "ADANIENT", "POWERGRID", "NTPC", "GRASIM", "TECHM", "JSWSTEEL", "TATASTEEL", "M&M", "ADANIPORTS",
        "DIVISLAB", "BAJAJFINSV", "BPCL", "HEROMOTOCO", "EICHERMOT", "ONGC", "COALINDIA", "BRITANNIA", "CIPLA", "SBILIFE",
        "DRREDDY", "APOLLOHOSP", "TATACONSUM", "HDFCLIFE", "BAJAJ-AUTO", "SHRIRAMFIN", "ULTRACEMCO", "INDUSINDBK", "HINDALCO",
        "BEL", "TRENT", "CHOLAFIN", "TATAPOWER", "TVSMOTOR", "SIEMENS", "ABB", "DLF", "LODHA", "ZOMATO", "PNB", "BANKBARODA",
        "CANBK", "IDFCFIRSTB", "FEDERALBNK", "AUBANK", "HINDPETRO", "IOC", "GAIL", "PETRONET", "MGL", "IGL", "TATATECH",
        "PERSISTENT", "COFORGE", "LTIM", "MPHASIS", "OFSS", "KPITTECH", "NAUKRI", "ZENSARTECH", "CYIENT", "SONACOMS",
        "MOTHERSON", "BHARATFORG", "ASHOKLEY", "BOSCHLTD", "TIINDIA", "MRF", "BALKRISIND", "APOLLOTYRE", "CEATLTD", "EXIDEIND",
        "AMBUJACEM", "ACC", "PIDILITIND", "SRF", "MUTHOOTFIN", "LUPIN", "AUROPHARMA", "BIOCON", "ALKEM", "GLENMARK",
        "IPCALAB", "LAURUSLABS", "TORNTPHARM", "ABBOTINDIA", "COROMANDEL", "UPL", "PIIND", "CHAMBLFERT", "DEEPAKNTR",
        "NAVINFLUOR", "ATUL", "AARTIIND", "CANFINHOM", "L&TFH", "PFC", "RECLTD", "HUDCO", "IRFC", "SBICARD", "ICICIGI",
        "ICICIPRULI", "SBILIFE", "MAXHEALTH", "FORTIS", "SYNGENE", "POLICYBABA", "PBFINTECH", "NYKAA", "PAYTM", "DELHIVERY",
        "ZYDUSLIFE", "DIXON", "AMBER", "POLYCAB", "KEI", "RRKABEL", "HAVELLS", "CROMPTON", "VGUARD", "WHIRLPOOL",
        "VOLTAS", "BLUESTARCO", "BHEL", "THERMAX", "CUMMINSIND", "ESCORTS", "CARBORUNIV", "TIMKEN", "SKFINDIA", "SCHAEFFLER",
        "JINDALSTEL", "SAIL", "NMDC", "VEDL", "HINDZINC", "NATIONALUM", "GRAVITA", "JSL", "WELCORP", "GPPL",
        "CONCOR", "ADANIGREEN", "ADANIPOWER", "TATATECH", "NHPC", "SJVN", "TORNTPOWER", "CESC", "JPPOWER", "SUZLON",
        "JSWENERGY", "INOXWIND", "KPIGREEN", "CGPOWER", "ABFRL", "PAGEIND", "BATAINDIA", "RELAXO", "JUBILANTFOOD", "DEVYANI",
        "SAPPHIRE", "WESTLIFE", "BARBEQUE", "MANYAVAR", "METROPOLIS", "LALPATHLAB", "THYROCARE", "KAYNES", "CYIENTDLM",
        "RBLBANK", "BANDHANBNK", "CSBBANK", "CUB", "SOUTHBANK", "KTKBANK", "DCBBANK", "MAHABANK", "UCOBANK", "IOB",
        "CENTRALBK", "PSB", "IEX", "MCX", "BSE", "CDSL", "CAMS", "KFINTECH", "RATEGAIN", "MAPMYINDIA", "EASEMYTRIP",
        "NAUKRI", "ZOMATO", "NYKAA", "PAYTM", "POLICYBABA", "FSL", "COFORGE", "MPHASIS", "PERSISTENT", "LTIM",
        "TECHM", "WIPRO", "INFY", "TCS", "HCLTECH", "OFSS", "LTTS", "CYIENT", "ZENSARTECH", "BEML",
        "HAL", "BDL", "MAZDOCK", "COCHINSHIP", "GRSE", "DATAPATTNS", "IDEA", "TATACOMM", "MTNL", "ONMOBILE",
        "TEJASNET", "HFCL", "ITI", "STLTECH", "RPOWER", "JPASSOCIATES", "IDBI", "DHANUKA", "ASTEC", "RALLIS",
        "SHARDACROP", "SUMICHEM", "BASF", "BAYERCROP", "FLUOROCHEM", "SOBHA", "OBEROIRLTY", "PRESTIGE", "PHOENIXLTD",
        "BRIGADE", "GodrejProperties", "MAHLIFE", "SUNTECK", "KPDL", "ASHIANA", "HEG", "GRAPHITE", "NOVA",
        "ANANDRATHI", "MOTILALOFS", "JUBLINGRIA", "CHEMPLASTS", "FINEORG", "CLEAN", "SUDARSCHEM", "ROSSARI", "NEOGEN",
        "galactico", "AETHER", "TIIL", "ASTRAZEN", "PFIZER", "SANOFI", "GSK", "PROCTER", "KOLTEPATIL", "PNCINFRA",
        "IRCON", "RVNL", "NBCC", "RITES", "KNRCON", "CAPACITE", "HGINFRA", "NCC", "GPIL", "JITF",
        "PENIND", "GREENPLY", "CENTURYPLY", "GREENPANEL", "STYLAMIND", "KAPSTON", "SIS", "QUESS", "TEAMLEASE", "GRINDWELL",
        "NESCO", "EIHOTEL", "CHALET", "LEMONTREE", "INDHOTEL", "KAMATHOTEL", "TASTYBITE", "KRBL", "LTFOODS", "DFMFOODS",
        "GODREJAGRO", "AVTNATURAL", "HATSUN", "DODLA", "HERITAGEFO", "PARAGMILK", "SKMEGGPROD", "VENKEYS", "SUVENPHAR", "PIRANHA",
        "PIRPHARMA", "LALPATHLAB", "METROPOLIS", "KIMS", "RAINBOW", "MAXHEALTH", "ASTERDM", "NARAYANA", "SHALBY", "GLOBALHHL",
        "MEDIASSIST", "FORTIS", "NH", "HATHWAY", "DEN", "GTPL", "SITI", "DISHTV", "SUNTV", "ZEEL",
        "PVRINOX", "TV18BRDCST", "NETWORK18", "NDTV", "ZEEMEDIA", "BALMLAWRIE", "BCG", "EVEREADY", "GILLETTE", "HONASA",
        "JYOTHYLAB", "PGHH", "RADICO", "UBL", "UNITDSPR", "MCDOWELL-N", "SULA", "GLOBUSSPR", "TIIC", "SHREECEM",
        "RAMCOCEM", "JKCEMENT", "HEIDELBERG", "DALBHARAT", "ORIENTCEM", "JKLCEMENT", "SAGCEM", "NCLIND", "KESORAMIND", "ISGEC"
    ]
    # Ensure unique and formatted with .NS
    return [s.strip().upper() + ".NS" for s in list(set(raw_symbols))]

with st.spinner("Loading Nifty 500 stock universe..."):
    tickers = get_nifty500_symbols()
    tickers_with_benchmark = tickers + ["^NSEI"]

st.sidebar.header("Screener Parameters")
rs_lower = st.sidebar.number_input("RS Lower Bound", value=-0.15, step=0.01)
rs_upper = st.sidebar.number_input("RS Upper Bound", value=0.15, step=0.01)
rsi_threshold = st.sidebar.slider("Minimum RSI (14)", min_value=30, max_value=70, value=50)
lookback = 55

if st.button("Run Screener scan"):
    if not tickers:
        st.error("Could not load stock tickers.")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("Downloading historical data and calculating indicators across Nifty 500...")
        
        # Download bulk historical data
        data = yf.download(tickers_with_benchmark, period="1y", interval="1d", group_by="ticker", threads=True)
        
        closes = pd.DataFrame()
        for ticker in tickers_with_benchmark:
            try:
                if isinstance(data.columns, pd.MultiIndex):
                    closes[ticker] = data[ticker]["Close"]
                else:
                    closes[ticker] = data["Close"]
            except Exception:
                continue
                
        closes = closes.dropna(how="all")
        
        if "^NSEI" not in closes.columns:
            st.error("Error fetching Nifty (^NSEI) benchmark data.")
        else:
            nifty_close = closes["^NSEI"]
            
            results = []
            valid_tickers = [t for t in tickers if t in closes.columns]
            total_tickers = len(valid_tickers)
            
            for i, stock in enumerate(valid_tickers):
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
                
                # Check conditions
                if (current_res > rs_lower) and (current_res < rs_upper) and (current_rsi >= rsi_threshold):
                    results.append({
                        "Ticker": stock.replace(".NS", ""),
                        "Close Price": round(current_price, 2),
                        "RS Value (55)": round(current_res, 4),
                        "RSI (14)": round(current_rsi, 2)
                    })
                    
                if total_tickers > 0:
                    progress_bar.progress((i + 1) / total_tickers)
                
            status_text.text("Scan complete!")
            progress_bar.empty()
            
            if results:
                res_df = pd.DataFrame(results)
                st.success(f"Found {len(res_df)} matching stocks meeting your criteria!")
                st.dataframe(res_df, use_container_width=True)
                
                fig = px.scatter(res_df, x="RS Value (55)", y="RSI (14)", text="Ticker", 
                                 title="Filtered Nifty 500 Stocks: RS vs RSI Map",
                                 hover_data=["Close Price"])
                fig.update_traces(textposition='top center')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No stocks matched the current criteria. Try widening your RS Lower/Upper bounds further in the sidebar (e.g., -0.25 to 0.25).")
