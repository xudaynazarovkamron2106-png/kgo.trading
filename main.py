import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import time

# ==========================================
# 1. MT5 PRO DESIGN (SILIT EFFEKT)
# ==========================================
st.set_page_config(page_title="KGO SMART TERMINAL", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #000000; color: #d1d4dc; }
    .main-header { font-size: 30px; color: #00ff00; font-weight: 900; text-align: center; margin-bottom: 20px; }
    .metric-card { background-color: #131722; padding: 15px; border-radius: 5px; border: 1px solid #2a2e39; text-align: center; }
    .price-live { font-family: 'Courier New', monospace; font-size: 28px; font-weight: bold; }
    .status-live { color: #00ff00; font-weight: bold; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SESSION STATE (DATA STORAGE)
# ==========================================
if 'history' not in st.session_state:
    st.session_state.balance = 50000.00
    prices = np.random.uniform(66400, 66450, 100)
    st.session_state.history = list(prices)

# ==========================================
# 3. LIVE UI PLACEHOLDERS
# ==========================================
st.markdown('<div class="main-header">KGO GLOBAL SMART LIVE</div>', unsafe_allow_html=True)

# Tepagi panellar uchun joy ajratamiz
header_place = st.empty()
chart_place = st.empty()

# ==========================================
# 4. INFINITE LIVE LOOP (DOIMIY ISHLAYDI)
# ==========================================
while True:
    # 1. Narxni yangilash (Simulyatsiya)
    last_p = st.session_state.history[-1]
    change = np.random.normal(0, 5)
    new_p = last_p + change
    st.session_state.history.append(new_p)
    if len(st.session_state.history) > 100:
        st.session_state.history.pop(0)

    # 2. Header panelini yangilash (Sayt refresh bo'lmasdan)
    color = "#00ff00" if change >= 0 else "#ff0000"
    with header_place.container():
        m1, m2, m3, m4 = st.columns(4)
        m1.markdown(f'<div class="metric-card">BALANCE<br><div class="stat-val">${st.session_state.balance:,.2f}</div></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="metric-card">SYMBOL<br><div class="stat-val" style="color:#2962ff">BTC/USDT</div></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="metric-card">LIVE PRICE<br><div class="price-live" style="color:{color}">${new_p:,.2f}</div></div>', unsafe_allow_html=True)
        m4.markdown(f'<div class="metric-card">STATUS<br><div class="status-live">LIVE</div></div>', unsafe_allow_html=True)

    # 3. Grafikni yangilash
    with chart_place.container():
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=st.session_state.history, 
            mode='lines+markers',
            line=dict(color='#00ff00' if change >= 0 else '#ff0000', width=2),
            fill='tozeroy',
            fillcolor='rgba(0, 255, 0, 0.1)' if change >= 0 else 'rgba(255, 0, 0, 0.1)'
        ))
        fig.update_layout(
            template="plotly_dark", height=500, margin=dict(l=0, r=0, t=0, b=0),
            plot_bgcolor='black', paper_bgcolor='black',
            yaxis=dict(side="right"), xaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # 4. Kutish (Tezlikni nazorat qilish)
    time.sleep(0.5) # 0.5 soniyada bir marta "silliq" yangilanadi
