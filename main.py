import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# ==========================================
# 1. MT5 CLASSIC INTERFACE (GRAY & BLACK)
# ==========================================
st.set_page_config(page_title="MetaTrader 5 - Terminal", layout="wide")

# MT5 ning klassik kulrang va to'q rangli stili
st.markdown("""
<style>
    .stApp { background-color: #2b2b2b; color: #e0e0e0; }
    .mt5-header { background-color: #3c3c3c; padding: 5px; border-bottom: 1px solid #1a1a1a; font-size: 14px; }
    .market-watch { background-color: #1e1e1e; border-right: 1px solid #1a1a1a; height: 800px; padding: 10px; }
    .terminal-box { background-color: #1e1e1e; border-top: 2px solid #1a1a1a; height: 200px; padding: 10px; font-family: sans-serif; font-size: 12px; }
    .stButton>button { border-radius: 0px; background-color: #4a4a4a; color: white; border: 1px solid #1a1a1a; height: 30px; font-size: 12px; }
    .buy-btn { background-color: #2e7d32 !important; }
    .sell-btn { background-color: #c62828 !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATA ENGINE (MT5 LOGIC)
# ==========================================
if 'history' not in st.session_state:
    st.session_state.balance = 10000.00
    st.session_state.positions = []
    # 21 xil vaqt oralig'i simulyatsiyasi uchun boshlang'ich ma'lumot
    times = [datetime.now() - timedelta(minutes=i) for i in range(100)]
    prices = np.random.uniform(66000, 66500, 100)
    st.session_state.history = pd.DataFrame({
        'Time': sorted(times),
        'Open': prices,
        'High': prices + 20,
        'Low': prices - 20,
        'Close': prices + 5
    })

# ==========================================
# 3. INTERFACE LAYOUT (MT5 STRUCTURE)
# ==========================================

# Yuqori Toolbar (MT5 kabi)
st.markdown('<div class="mt5-header">File | View | Insert | Charts | Tools | Window | Help</div>', unsafe_allow_html=True)

# Asosiy 3 talik bo'lim
col_market, col_main = st.columns([1, 4])

with col_market:
    st.markdown("### Market Watch")
    # MT5 kabi jadval ko'rinishidagi narxlar
    market_data = {
        "Symbol": ["BTCUSD", "ETHUSD", "XAUUSD", "EURUSD"],
        "Bid": [66430.10, 3450.20, 2350.50, 1.0850],
        "Ask": [66432.50, 3451.80, 2351.10, 1.0852]
    }
    st.table(pd.DataFrame(market_data))
    
    st.markdown("---")
    st.markdown("### Navigator")
    st.caption("📂 Accounts\n\n📊 Indicators\n\n🤖 Expert Advisors")

with col_main:
    # 1. Grafik qismi
    fig = go.Figure(data=[go.Candlestick(
        x=st.session_state.history['Time'],
        open=st.session_state.history['Open'],
        high=st.session_state.history['High'],
        low=st.session_state.history['Low'],
        close=st.session_state.history['Close'],
        increasing_line_color='#26a69a', decreasing_line_color='#ef5350'
    )])
    
    fig.update_layout(
        template="plotly_dark",
        height=500,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_rangeslider_visible=False,
        plot_bgcolor='#000000',
        paper_bgcolor='#1e1e1e',
        yaxis=dict(side="right", gridcolor="#2a2a2a")
    )
    st.plotly_chart(fig, use_container_width=True)

    # 2. Savdo tugmalari (One-Click Trading)
    t1, t2, t3 = st.columns([1, 1, 2])
    with t1:
        if st.button("SELL", use_container_width=True):
            st.session_state.positions.append({"Symbol": "BTCUSD", "Type": "Sell", "Volume": 0.1, "Price": 66430.10})
    with t2:
        if st.button("BUY", use_container_width=True):
            st.session_state.positions.append({"Symbol": "BTCUSD", "Type": "Buy", "Volume": 0.1, "Price": 66432.50})
    with t3:
        st.write(f"**Balance:** ${st.session_state.balance:,.2f}")

    # 3. Terminal (Pastki qism)
    st.markdown('<div class="terminal-box">', unsafe_allow_html=True)
    st.markdown("### Toolbox")
    tab1, tab2, tab3 = st.tabs(["Trade", "Exposure", "History"])
    
    with tab1:
        if st.session_state.positions:
            st.dataframe(pd.DataFrame(st.session_state.positions), use_container_width=True)
        else:
            st.caption("No open positions.")
    
    with tab3:
        st.caption("No trade history.")
    st.markdown('</div>', unsafe_allow_html=True)

# Avtomatik yangilash (miltillashsiz harakat uchun)
if st.button("Refresh Terminal"):
    st.rerun()
