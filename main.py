import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import time
from plotly.subplots import make_subplots

# ==========================================
# 1. MT5 ULTIMATE CONFIGURATION
# ==========================================
st.set_page_config(page_title="KGO TERMINAL PRO v5.2", layout="wide", initial_sidebar_state="collapsed")

# Professional Dark Theme CSS
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #d1d4dc; }
    .main-header { font-family: 'Segoe UI', sans-serif; font-size: 32px; color: #00ff00; font-weight: 900; border-bottom: 2px solid #1e222d; padding-bottom: 10px; margin-bottom: 20px; text-shadow: 2px 2px 4px #000; text-align: center; }
    .stButton>button { border-radius: 4px; font-weight: 900; height: 60px; font-size: 20px; transition: 0.2s; border: none; text-transform: uppercase; width: 100%; }
    .buy-btn { background-color: #089981 !important; color: white !important; }
    .sell-btn { background-color: #f23645 !important; color: white !important; }
    .metric-card { background-color: #131722; padding: 15px; border-radius: 4px; border: 1px solid #2a2e39; text-align: center; }
    .stat-val { font-size: 22px; font-weight: bold; color: #ffffff; }
    .stat-label { font-size: 11px; color: #787b86; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CORE ENGINE & DATA
# ==========================================
if 'history' not in st.session_state:
    st.session_state.balance = 50000.00
    st.session_state.trades = []
    
    # Generate Initial Data
    times = [datetime.now() - timedelta(seconds=i) for i in range(150)]
    times.reverse()
    prices = np.random.uniform(66000, 66500, 150)
    
    st.session_state.history = pd.DataFrame({
        'Time': times,
        'Open': prices,
        'High': prices + 30,
        'Low': prices - 30,
        'Close': prices + 5
    })

def get_live_tick():
    df = st.session_state.history
    last_close = df.iloc[-1]['Close']
    
    move = np.random.normal(0, 25)
    new_p = last_close + move
    
    new_row = pd.DataFrame([{
        'Time': datetime.now(),
        'Open': last_close,
        'High': max(last_close, new_p) + np.random.uniform(2, 10),
        'Low': min(last_close, new_p) - np.random.uniform(2, 10),
        'Close': new_p
    }])
    
    st.session_state.history = pd.concat([df, new_row], ignore_index=True).iloc[1:]
    return new_p

current_p = get_live_tick()

# Indicators
def calc_indicators(df):
    df['MA10'] = df['Close'].rolling(window=10).mean()
    df['MA30'] = df['Close'].rolling(window=30).mean()
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    df['RSI'] = 100 - (100 / (1 + (gain/loss.replace(0, 1e-9)))) # 0 ga bo'lishdan qochish
    return df

df_final = calc_indicators(st.session_state.history)

# ==========================================
# 3. INTERFACE
# ==========================================
st.markdown('<div class="main-header">KGO GLOBAL PRO TERMINAL 💹</div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="metric-card"><div class="stat-label">Balance</div><div class="stat-val">${st.session_state.balance:,.2f}</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="metric-card"><div class="stat-label">Symbol</div><div class="stat-val" style="color:#2962ff">BTC/USDT</div></div>', unsafe_allow_html=True)
with m3:
    color = "#00ff00" if current_p > df_final.iloc[-2]['Close'] else "#ff0000"
    # XATO TUZATILDI: Formatlash to'g'ri qilindi
    st.markdown(f'<div class="metric-card"><div class="stat-label">Live Price</div><div class="stat-val" style="color:{color}">${current_p:,.2f}</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="metric-card"><div class="stat-label">Status</div><div class="stat-val" style="color:#00ff00">LIVE</div></div>', unsafe_allow_html=True)

# ==========================================
# 4. CHART & PANEL
# ==========================================
left, right = st.columns([4, 1])

with left:
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.8, 0.2])
    
    fig.add_trace(go.Candlestick(
        x=df_final['Time'], open=df_final['Open'], high=df_final['High'],
        low=df_final['Low'], close=df_final['Close'],
        increasing_line_color='#089981', decreasing_line_color='#f23645', name="Price"
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(x=df_final['Time'], y=df_final['MA10'], line=dict(color='#2962ff', width=1.5), name="MA10"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df_final['Time'], y=df_final['RSI'], line=dict(color='#9b59b6', width=2), name="RSI"), row=2, col=1)

    fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=600, 
                      margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="black", plot_bgcolor="black")
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with right:
    st.markdown("### Savdo")
    lots = st.number_input("Lots:", 0.01, 10.0, 0.10)
    
    if st.button("BUY", key="buy_btn"):
        st.session_state.trades.append({"Time": datetime.now().strftime("%H:%M:%S"), "Type": "BUY", "Price": round(current_p, 2)})
        st.toast(f"BUY @ {current_p:,.2f}")
    
    st.write("")
    
    if st.button("SELL", key="sell_btn"):
        st.session_state.trades.append({"Time": datetime.now().strftime("%H:%M:%S"), "Type": "SELL", "Price": round(current_p, 2)})
        st.toast(f"SELL @ {current_p:,.2f}")

    st.write("---")
    if st.session_state.trades:
        st.write("**So'nggi savdo:**")
        st.write(st.session_state.trades[-1])

# ==========================================
# 5. ENGINE
# ==========================================
time.sleep(1)
st.rerun()
