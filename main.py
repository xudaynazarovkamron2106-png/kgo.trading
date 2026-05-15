import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import time

# ==========================================
# 1. MT5 PRO DARK UI
# ==========================================
st.set_page_config(page_title="KGO TRADING PRO", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #000000; color: #ffffff; }
    .main-header { font-size: 35px; color: #00ff00; font-weight: 900; text-align: center; margin-bottom: 20px; text-shadow: 0 0 15px #00ff00; }
    .metric-card { background-color: #131722; padding: 20px; border-radius: 4px; border: 1px solid #2a2e39; text-align: center; }
    .stat-val { font-size: 28px; font-weight: bold; font-family: 'Courier New', monospace; }
    .status-live { color: #00ff00; font-weight: bold; animation: blinker 1s linear infinite; font-size: 20px; }
    @keyframes blinker { 50% { opacity: 0; } }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SESSION STATE RESET (Xatoni oldini olish)
# ==========================================
# Agar history turi noto'g'ri bo'lsa, uni tozalaymiz
if 'history' not in st.session_state or not isinstance(st.session_state.history, list):
    st.session_state.history = list(np.random.uniform(66400, 66450, 100))
    st.session_state.balance = 50000.00

# ==========================================
# 3. INTERFACE PLACEHOLDERS
# ==========================================
st.markdown('<div class="main-header">KGO GLOBAL LIVE TERMINAL 💹</div>', unsafe_allow_html=True)

header_placeholder = st.empty()
chart_placeholder = st.empty()

# ==========================================
# 4. LIVE UPDATE ENGINE
# ==========================================
while True:
    # Narxni hisoblash
    last_p = float(st.session_state.history[-1])
    change = np.random.normal(0, 4) 
    new_p = last_p + change
    
    # Ma'lumotni yangilash
    st.session_state.history.append(new_p)
    if len(st.session_state.history) > 150:
        st.session_state.history.pop(0)

    # 1. Tepagi Panel (Refresh bo'lmasdan yangilanadi)
    p_color = "#00ff00" if change >= 0 else "#ff4b4b"
    
    with header_placeholder.container():
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f'<div class="metric-card"><div style="color:gray; font-size:12px;">BALANCE</div><div class="stat-val">${st.session_state.balance:,.2f}</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="metric-card"><div style="color:gray; font-size:12px;">PAIR</div><div class="stat-val" style="color:#2962ff">BTC/USDT</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="metric-card"><div style="color:gray; font-size:12px;">LIVE PRICE</div><div class="stat-val" style="color:{p_color};">${new_p:,.2f}</div></div>', unsafe_allow_html=True)
        c4.markdown(f'<div class="metric-card"><div style="color:gray; font-size:12px;">STATUS</div><div class="status-live">● LIVE</div></div>', unsafe_allow_html=True)

    # 2. Grafikni yangilash
    with chart_placeholder.container():
        fig = go.Figure()
        
        # Area Chart (Silliq chiziq)
        fig.add_trace(go.Scatter(
            y=st.session_state.history,
            mode='lines',
            line=dict(color=p_color, width=3),
            fill='tozeroy',
            fillcolor=f'rgba({0 if change < 0 else 0}, {255 if change >= 0 else 0}, {0 if change >= 0 else 255}, 0.1)'
        ))
        
        # Oxirgi narx belgisi
        fig.add_trace(go.Scatter(
            x=[len(st.session_state.history)-1],
            y=[new_p],
            mode='markers',
            marker=dict(color=p_color, size=12, line=dict(color='white', width=1))
        ))

        fig.update_layout(
            template="plotly_dark",
            height=500,
            margin=dict(l=0, r=0, t=0, b=0),
            plot_bgcolor='black',
            paper_bgcolor='black',
            showlegend=False,
            yaxis=dict(side="right", gridcolor="#1e222d", tickformat=",.2f"),
            xaxis=dict(showgrid=False, showticklabels=False)
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Tezlik (0.4 soniya - juda silliq)
    time.sleep(0.4)
