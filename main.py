import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import time

# --- [1. MT5 PROFESSIONAL DARK DESIGN] ---
st.set_page_config(page_title="MT5 LIVE - KGO", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #000000; color: #ffffff; }
    .price-up { color: #00ff00; font-weight: bold; font-size: 24px; }
    .price-down { color: #ff0000; font-weight: bold; font-size: 24px; }
    .stButton>button { border-radius: 5px; height: 50px; font-size: 18px; font-weight: bold; }
    /* Terminal stili */
    .terminal { background-color: #1a1a1a; border-top: 2px solid #333; padding: 10px; }
</style>
""", unsafe_allow_html=True)

# --- [2. DATA STORAGE] ---
if 'history' not in st.session_state:
    # Boshlang'ich 50 ta shamcha
    st.session_state.history = pd.DataFrame({
        'Time': pd.date_range(end=datetime.now(), periods=50, freq='S'),
        'Open': np.random.uniform(65000, 65100, 50),
        'High': np.random.uniform(65100, 65200, 50),
        'Low': np.random.uniform(64900, 65000, 50),
        'Close': np.random.uniform(65000, 65100, 50)
    })
if 'balance' not in st.session_state:
    st.session_state.balance = 10000.0

# --- [3. LIVE UPDATE LOGIC] ---
# Oxirgi narxni olish va yangi narx yaratish
last_row = st.session_state.history.iloc[-1]
change = np.random.uniform(-50, 50)
new_close = last_row['Close'] + change

new_data = pd.DataFrame([{
    'Time': datetime.now(),
    'Open': last_row['Close'],
    'High': max(last_row['Close'], new_close) + 10,
    'Low': min(last_row['Close'], new_close) - 10,
    'Close': new_close
}])

st.session_state.history = pd.concat([st.session_state.history, new_data], ignore_index=True).iloc[1:]

# --- [4. INTERFACE] ---
st.title("💹 KGO GLOBAL - MetaTrader 5 LIVE")

col_main, col_side = st.columns([4, 1])

with col_side:
    st.write("### Savdo Paneli")
    price_style = "price-up" if change > 0 else "price-down"
    st.markdown(f"BTC/USDT: <span class='{price_style}'>${new_close:.2f}</span>", unsafe_allow_html=True)
    
    st.write(f"Balans: **${st.session_state.balance:,.2f}**")
    
    lot = st.number_input("Lot:", 0.01, 10.0, 0.1)
    
    if st.button("🟢 BUY", use_container_width=True):
        st.toast("Buy Order Open!")
    if st.button("🔴 SELL", use_container_width=True):
        st.toast("Sell Order Open!")
    
    st.info("Bozor holati: Ochiq")

with col_main:
    # Professional LIVE Grafik
    fig = go.Figure(data=[go.Candlestick(
        x=st.session_state.history['Time'],
        open=st.session_state.history['Open'],
        high=st.session_state.history['High'],
        low=st.session_state.history['Low'],
        close=st.session_state.history['Close'],
        increasing_line_color='#00ff00', # Yashil tepaga
        decreasing_line_color='#ff0000'  # Qizil pastga
    )])

    fig.update_layout(
        template="plotly_dark",
        xaxis_rangeslider_visible=False,
        height=500,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor='#000000',
        paper_bgcolor='#000000'
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# --- [5. AVTOMATIK YANGILASH (LIVE)] ---
# Bu qism saytni o'zi avtomat yangilashga majbur qiladi
time.sleep(1) # Har 1 soniyada yangilanadi
st.rerun()
