import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# ==========================================
# 1. MT5 CLASSIC DESIGN
# ==========================================
st.set_page_config(page_title="MetaTrader 5 Terminal", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #1e1e1e; color: #dcdcdc; }
    .mt5-toolbar { background-color: #383838; padding: 5px; border-bottom: 1px solid #000; font-size: 13px; color: #fff; }
    .market-watch { background-color: #2b2b2b; border: 1px solid #111; padding: 10px; height: 600px; }
    .stButton>button { border-radius: 0px; background-color: #444; color: white; border: 1px solid #222; height: 35px; width: 100%; }
    .buy-btn { background-color: #2e7d32 !important; font-weight: bold; }
    .sell-btn { background-color: #c62828 !important; font-weight: bold; }
    .terminal-section { background-color: #2b2b2b; border-top: 2px solid #000; padding: 10px; margin-top: 20px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATA INITIALIZATION (MT5_DF)
# ==========================================
# O'zgaruvchi nomini mt5_df qildik, shunda eski xato chiqmaydi
if 'mt5_df' not in st.session_state:
    st.session_state.balance = 10000.00
    st.session_state.open_trades = []
    
    # Boshlang'ich shamchalar
    start_time = datetime.now() - timedelta(hours=5)
    times = [start_time + timedelta(minutes=i*5) for i in range(100)]
    prices = np.random.uniform(66000, 66500, 100)
    
    st.session_state.mt5_df = pd.DataFrame({
        'Time': times,
        'Open': prices,
        'High': prices + 25,
        'Low': prices - 25,
        'Close': prices + 10
    })

# ==========================================
# 3. INTERFACE LAYOUT
# ==========================================

# 1. Toolbar
st.markdown('<div class="mt5-toolbar">File | View | Insert | Charts | Tools | Help</div>', unsafe_allow_html=True)

col_sidebar, col_chart = st.columns([1, 4])

with col_sidebar:
    st.markdown("### Market Watch")
    # MT5 kabi jadval
    watch_list = pd.DataFrame({
        "Symbol": ["BTCUSD", "ETHUSD", "XAUUSD", "GBPUSD"],
        "Bid": [66430.5, 3450.2, 2350.8, 1.2650],
        "Ask": [66432.1, 3451.5, 2351.2, 1.2652]
    })
    st.table(watch_list)
    
    st.markdown("---")
    st.write(f"💰 **Balance:** ${st.session_state.balance:,.2f}")
    lot = st.number_input("Lots:", 0.01, 10.0, 0.1)
    
    if st.button("BUY", key="buy_mt5"):
        price = 66432.1
        st.session_state.open_trades.append({"Time": datetime.now().strftime("%H:%M"), "Type": "Buy", "Lots": lot, "Price": price})
        st.toast(f"Buy Order Opened: {lot} lots")
        
    if st.button("SELL", key="sell_mt5"):
        price = 66430.5
        st.session_state.open_trades.append({"Time": datetime.now().strftime("%H:%M"), "Type": "Sell", "Lots": lot, "Price": price})
        st.toast(f"Sell Order Opened: {lot} lots")

with col_chart:
    # Professional Candlestick Chart
    fig = go.Figure(data=[go.Candlestick(
        x=st.session_state.mt5_df['Time'],
        open=st.session_state.mt5_df['Open'],
        high=st.session_state.mt5_df['High'],
        low=st.session_state.mt5_df['Low'],
        close=st.session_state.mt5_df['Close'],
        increasing_line_color='#26a69a', decreasing_line_color='#ef5350'
    )])
    
    fig.update_layout(
        template="plotly_dark",
        height=550,
        margin=dict(l=0, r=0, t=10, b=10),
        xaxis_rangeslider_visible=False,
        plot_bgcolor='#000',
        paper_bgcolor='#2b2b2b',
        yaxis=dict(side="right", gridcolor="#333")
    )
    st.plotly_chart(fig, use_container_width=True)

# 4. Terminal (Pastki qism)
st.markdown('<div class="terminal-section">', unsafe_allow_html=True)
st.markdown("### Toolbox")
if st.session_state.open_trades:
    st.dataframe(pd.DataFrame(st.session_state.open_trades), use_container_width=True)
else:
    st.caption("No open positions. Trade history is empty.")
st.markdown('</div>', unsafe_allow_html=True)

# Manual Refresh
if st.button("🔄 Update Quotes"):
    st.rerun()
