import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import time

# ==========================================
# 1. MT5 DARK MODE - PROFESSIONAL CSS
# ==========================================
st.set_page_config(page_title="KGO TRADING LIVE", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #000000; color: #ffffff; }
    .main-header { font-size: 35px; color: #00ff00; font-weight: 900; text-align: center; font-family: sans-serif; margin-bottom: 20px; text-shadow: 0 0 10px #00ff00; }
    .metric-card { background-color: #131722; padding: 20px; border-radius: 4px; border: 1px solid #2a2e39; text-align: center; min-height: 100px; }
    .stat-val { font-size: 26px; font-weight: bold; font-family: 'Courier New', monospace; }
    .stat-label { font-size: 12px; color: #787b86; margin-bottom: 10px; }
    .status-live { color: #00ff00; font-weight: bold; animation: blinker 1s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SESSION STATE - DATA LOGIC
# ==========================================
# Agarda session_state da eski ma'lumot bo'lsa, uni o'chirib yuboramiz (Xatoni oldini olish)
if 'history' not in st.session_state or isinstance(st.session_state.history, pd.DataFrame):
    st.session_state.history = list(np.random.uniform(66400, 66450, 100))
    st.session_state.balance = 50000.00

# ==========================================
# 3. INTERFACE ELEMENTS
# ==========================================
st.markdown('<div class="main-header">KGO GLOBAL TRADING TERMINAL 💹</div>', unsafe_allow_html=True)

# Joylarni (Placeholders) yaratamiz
header_placeholder = st.empty()
chart_placeholder = st.empty()

# ==========================================
# 4. LIVE ANIMATION LOOP
# ==========================================
while True:
    # 1. Narxni yangilash
    last_p = st.session_state.history[-1]
    # Kichikroq va realistik o'zgarish
    change = np.random.normal(0, 3) 
    new_p = last_p + change
    
    # Ro'yxatni yangilash
    st.session_state.history.append(new_p)
    if len(st.session_state.history) > 150: # Grafik sig'imi
        st.session_state.history.pop(0)

    # 2. Tepagi panellarni yangilash
    price_color = "#00ff00" if change >= 0 else "#ff0000"
    
    with header_placeholder.container():
        m1, m2, m3, m4 = st.columns(4)
        m1.markdown(f'<div class="metric-card"><div class="stat-label">ACCOUNT BALANCE</div><div class="stat-val">${st.session_state.balance:,.2f}</div></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="metric-card"><div class="stat-label">TRADING PAIR</div><div class="stat-val" style="color:#2962ff">BTC/USDT</div></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="metric-card"><div class="stat-label">LIVE PRICE</div><div class="stat-val" style="color:{price_color};">${new_p:,.2f}</div></div>', unsafe_allow_html=True)
        m4.markdown(f'<div class="metric-card"><div class="stat-label">MARKET STATUS</div><div class="status-live" style="font-size:24px;">● LIVE</div></div>', unsafe_allow_html=True)

    # 3. Grafikni (Silliq) yangilash
    with chart_placeholder.container():
        fig = go.Figure()
        
        # Grafik chizig'i
        fig.add_trace(go.Scatter(
            y=st.session_state.history,
            mode='lines',
            line=dict(color=price_color, width=3),
            fill='tozeroy',
            fillcolor=f'rgba({0 if change < 0 else 0}, {255 if change >= 0 else 0}, {0 if change >= 0 else 255}, 0.1)'
        ))
        
        # Oxirgi narx nuqtasi
        fig.add_trace(go.Scatter(
            x=[len(st.session_state.history)-1],
            y=[new_p],
            mode='markers',
            marker=dict(color=price_color, size=10, symbol='circle')
        ))

        fig.update_layout(
            template="plotly_dark",
            height=550,
            margin=dict(l=0, r=0, t=0, b=0),
            plot_bgcolor='black',
            paper_bgcolor='black',
            showlegend=False,
            yaxis=dict(side="right", gridcolor="#1e222d"),
            xaxis=dict(showgrid=False, showticklabels=False)
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # 4. Kichik kutish (Tezlikni sozlash)
    time.sleep(0.5)
