import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import time
from plotly.subplots import make_subplots

# ==========================================
# 1. PLATFORMA SOZLAMALARI (MT5 STYLE)
# ==========================================
st.set_page_config(page_title="KGO TRADING TERMINAL v5.0", layout="wide", initial_sidebar_state="expanded")

# Maxsus CSS: Haqiqiy birja interfeysi
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #d1d4dc; }
    .main-header { font-family: 'Courier New', monospace; font-size: 28px; color: #00ff00; border-bottom: 2px solid #222; margin-bottom: 15px; }
    .stButton>button { border-radius: 4px; font-weight: 800; height: 45px; transition: 0.3s; border: 1px solid #444; }
    .buy-btn { background-color: #089981 !important; color: white !important; }
    .sell-btn { background-color: #f23645 !important; color: white !important; }
    .metric-box { background-color: #131722; padding: 15px; border-radius: 8px; border: 1px solid #2a2e39; }
    .terminal-window { background-color: #131722; border: 1px solid #2a2e39; font-family: monospace; font-size: 12px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. MA'LUMOTLAR OMBORI (SESSION STATE)
# ==========================================
if 'init' not in st.session_state:
    st.session_state.init = True
    st.session_state.balance = 25000.00
    st.session_state.equity = 25000.00
    st.session_state.positions = []
    st.session_state.history_log = []
    
    # Boshlang'ich 200 ta shamcha (Data History)
    base_time = datetime.now() - timedelta(minutes=200)
    times = [base_time + timedelta(minutes=i) for i in range(200)]
    prices = np.random.uniform(64000, 65000, 200)
    
    st.session_state.df = pd.DataFrame({
        'Time': times,
        'Open': prices,
        'High': prices + 50,
        'Low': prices - 50,
        'Close': prices + 10,
        'Volume': np.random.randint(100, 1000, 200)
    })

# ==========================================
# 3. MATEMATIK HISOB-KITOB (INDICATORS)
# ==========================================
def apply_indicators(df):
    # MA 20 va MA 50
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()
    
    # RSI (Relative Strength Index)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

# Live narxni yangilash
def tick_price():
    last_close = st.session_state.df['Close'].iloc[-1]
    volatility = 45 # Bozor "hayajoni"
    change = np.random.normal(0, volatility)
    new_price = last_close + change
    
    new_row = {
        'Time': datetime.now(),
        'Open': last_close,
        'High': max(last_close, new_close) + np.random.uniform(0, 15),
        'Low': min(last_close, new_close) - np.random.uniform(0, 15),
        'Close': new_price,
        'Volume': np.random.randint(500, 2000)
    }
    st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_row])], ignore_index=True).iloc[1:]
    return new_price

current_price = tick_price()
st.session_state.df = apply_indicators(st.session_state.df)

# ==========================================
# 4. INTERFEYS: TEPADAGI PANEL (DASHBOARD)
# ==========================================
st.markdown('<div class="main-header">KGO GLOBAL TRADING TERMINAL 🚀</div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="metric-box">💰 Balance<br><h2 style="color:white;">${st.session_state.balance:,.2f}</h2></div>', unsafe_allow_html=True)
with m2:
    pnl_color = "#00ff00" if st.session_state.equity >= st.session_state.balance else "#ff4b4b"
    st.markdown(f'<div class="metric-box">📊 Equity<br><h2 style="color:{pnl_color};">${st.session_state.equity:,.2f}</h2></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric-box">📈 Symbol<br><h2 style="color:#0088ff;">BTC/USDT</h2></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="metric-box">⏱ Server Time<br><h2 style="color:gray;">{datetime.now().strftime("%H:%M:%S")}</h2></div>', unsafe_allow_html=True)

# ==========================================
# 5. ASOSIY QISM: GRAFIK VA SAVDO
# ==========================================
left_col, right_col = st.columns([3.5, 1])

with left_col:
    # PROFESSIONAL MULTI-CHART (Candles + Volume + RSI)
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.05, row_heights=[0.7, 0.3])

    # Candlestick
    fig.add_trace(go.Candlestick(
        x=st.session_state.df['Time'],
        open=st.session_state.df['Open'], high=st.session_state.df['High'],
        low=st.session_state.df['Low'], close=st.session_state.df['Close'],
        name="Price", increasing_line_color='#089981', decreasing_line_color='#f23645'
    ), row=1, col=1)

    # Moving Averages
    fig.add_trace(go.Scatter(x=st.session_state.df['Time'], y=st.session_state.df['MA20'], line=dict(color='#2962ff', width=1), name="MA20"), row=1, col=1)
    fig.add_trace(go.Scatter(x=st.session_state.df['Time'], y=st.session_state.df['MA50'], line=dict(color='#ff9800', width=1), name="MA50"), row=1, col=1)

    # RSI
    fig.add_trace(go.Scatter(x=st.session_state.df['Time'], y=st.session_state.df['RSI'], line=dict(color='#787b86', width=1.5), name="RSI"), row=2, col=1)
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

    fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=600, 
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # TERMINAL WINDOW (Pastdagi ochiq pozitsiyalar)
    st.markdown("### 🖥 Trade Terminal")
    if st.session_state.positions:
        trade_df = pd.DataFrame(st.session_state.positions)
        st.dataframe(trade_df, use_container_width=True)
    else:
        st.markdown('<div style="color:gray; padding:20px;">No active trades. Market is waiting for orders...</div>', unsafe_allow_html=True)

with right_col:
    # SAVDO PANELI (ORDER ENTRY)
    st.markdown("### ⚡ Execution")
    lot_size = st.number_input("Lot Size:", 0.01, 100.0, 0.1, step=0.1)
    tp = st.number_input("Take Profit (Price):", 0.0, 100000.0, current_price + 500)
    sl = st.number_input("Stop Loss (Price):", 0.0, 100000.0, current_price - 500)
    
    st.write("")
    
    b1, b2 = st.columns(2)
    with b1:
        if st.button("BUY", key="b_buy", use_container_width=True):
            st.session_state.positions.append({
                "Symbol": "BTCUSD", "Type": "BUY", "Volume": lot_size, 
                "Open Price": round(current_price, 2), "Time": datetime.now().strftime("%H:%M:%S")
            })
            st.toast(f"Market Buy Order Filled: {lot_size} lots", icon="✅")
            
    with b2:
        if st.button("SELL", key="b_sell", use_container_width=True):
            st.session_state.positions.append({
                "Symbol": "BTCUSD", "Type": "SELL", "Volume": lot_size, 
                "Open Price": round(current_price, 2), "Time": datetime.now().strftime("%H:%M:%S")
            })
            st.toast(f"Market Sell Order Filled: {lot_size} lots", icon="🚀")

    st.write("---")
    # MARKET DEPTH (ORDER BOOK)
    st.markdown("### 📊 Order Book")
    bids = pd.DataFrame({'Price': [current_price-i*10 for i in range(1,6)], 'Size': np.random.uniform(0.1, 2.5, 5)})
    asks = pd.DataFrame({'Price': [current_price+i*10 for i in range(1,6)], 'Size': np.random.uniform(0.1, 2.5, 5)})
    
    st.write("Asks (Sellers)")
    st.dataframe(asks.sort_values('Price', ascending=False), hide_index=True)
    st.write("Bids (Buyers)")
    st.dataframe(bids, hide_index=True)

# ==========================================
# 6. AUTO-ANIMATION ENGINE
# ==========================================
time.sleep(1.5) # Bozor harakat tezligi
st.rerun()
