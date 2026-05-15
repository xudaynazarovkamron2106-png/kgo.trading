import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import time

# --- [1. MT5 PROFESSIONAL INTERFACE CONFIG] ---
st.set_page_config(page_title="MetaTrader 5 - KGO Edition", layout="wide", page_icon="💹")

# MT5 Dark Theme Style
st.markdown("""
<style>
    .stApp { background-color: #1c1c1c; color: #ffffff; }
    header {visibility: hidden;}
    .main-header { font-size: 24px; font-weight: bold; color: #f0f0f0; border-bottom: 1px solid #444; padding: 10px; margin-bottom: 20px; }
    .mt5-sidebar { background-color: #2b2b2b; padding: 15px; border-right: 1px solid #444; }
    .stButton>button { width: 100%; border-radius: 2px; font-weight: bold; height: 50px; border: none; }
    div[data-testid="stMetricValue"] { color: #00ff00; font-size: 20px; }
    /* MT5 BUY/SELL Buttons */
    .buy-btn { background-color: #2e7d32 !important; color: white !important; }
    .sell-btn { background-color: #c62828 !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# --- [2. STATE MANAGEMENT (REAL-TIME DATA)] ---
if 'price_history' not in st.session_state:
    st.session_state.price_history = pd.DataFrame({
        'Date': pd.date_range(end=datetime.now(), periods=100, freq='1min'),
        'Open': np.random.uniform(65000, 66000, 100),
        'High': np.random.uniform(66000, 67000, 100),
        'Low': np.random.uniform(64000, 65000, 100),
        'Close': np.random.uniform(65000, 66000, 100)
    })
if 'balance' not in st.session_state:
    st.session_state.balance = 10000.0
if 'positions' not in st.session_state:
    st.session_state.positions = []

# --- [3. REAL-TIME PRICE UPDATE] ---
def update_price():
    last_price = st.session_state.price_history.iloc[-1]['Close']
    change = np.random.uniform(-100, 100)
    new_price = last_price + change
    new_row = {
        'Date': datetime.now(),
        'Open': last_price,
        'High': new_price + 50,
        'Low': new_price - 50,
        'Close': new_price
    }
    st.session_state.price_history = pd.concat([st.session_state.price_history, pd.DataFrame([new_row])], ignore_index=True).iloc[1:]

update_price()
current_data = st.session_state.price_history.iloc[-1]

# --- [4. LAYOUT: MT5 STRUCTURE] ---
# Top Bar
st.markdown('<div class="main-header">MetaTrader 5 - KGO GLOBAL (Real-Time)</div>', unsafe_allow_html=True)

col_sidebar, col_chart, col_orders = st.columns([1, 4, 1])

with col_sidebar:
    st.markdown("### Market Watch")
    st.metric("BTCUSD", f"${current_data['Close']:.2f}", f"{np.random.uniform(-1, 1):.2f}%")
    st.metric("ETHUSD", f"${current_data['Close']/20:.2f}", "-0.15%")
    st.metric("GOLD", "$2,350.10", "+0.45%")
    
    st.divider()
    st.write(f"💰 Balance: **${st.session_state.balance:,.2f}**")
    lot_size = st.number_input("Lots:", value=0.1, step=0.1)

with col_chart:
    # Professional Candlestick Chart
    fig = go.Figure(data=[go.Candlestick(
        x=st.session_state.price_history['Date'],
        open=st.session_state.price_history['Open'],
        high=st.session_state.price_history['High'],
        low=st.session_state.price_history['Low'],
        close=st.session_state.price_history['Close'],
        increasing_line_color='#26a69a', decreasing_line_color='#ef5350',
        increasing_fillcolor='#26a69a', decreasing_fillcolor='#ef5350'
    )])
    
    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=10, r=10, t=10, b=10),
        height=500,
        xaxis_rangeslider_visible=False,
        plot_bgcolor="#1c1c1c",
        paper_bgcolor="#1c1c1c"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Bottom Terminal (Positions)
    st.markdown("### Toolbox (Trade History)")
    if st.session_state.positions:
        st.table(pd.DataFrame(st.session_state.positions))
    else:
        st.info("No active positions.")

with col_orders:
    st.markdown("### New Order")
    if st.button("🔴 SELL", type="primary", use_container_width=True):
        st.session_state.positions.append({"Type": "SELL", "Price": current_data['Close'], "Lot": lot_size, "Time": datetime.now().strftime("%H:%M:%S")})
        st.toast(f"Sell Order Placed at {current_data['Close']:.2f}")
    
    st.write("") # Spacer
    
    if st.button("🟢 BUY", use_container_width=True):
        st.session_state.positions.append({"Type": "BUY", "Price": current_data['Close'], "Lot": lot_size, "Time": datetime.now().strftime("%H:%M:%S")})
        st.toast(f"Buy Order Placed at {current_data['Close']:.2f}")

    st.divider()
    st.markdown("**Account Summary**")
    st.write(f"Equity: {st.session_state.balance}")
    st.write(f"Margin: {lot_size * 500}")

# Auto-refresh using Streamlit's fragment-like behavior (Simulated with button for stability)
if st.button("🔄 REFRESH MARKET"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("MT5 Mode: Active. Trading server: KGO-LONDON")
