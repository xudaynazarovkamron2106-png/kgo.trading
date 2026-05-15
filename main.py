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
st.set_page_config(page_title="KGO TERMINAL PRO v5.1", layout="wide", initial_sidebar_state="collapsed")

# Professional Dark Theme CSS
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #d1d4dc; }
    .main-header { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 32px; color: #00ff00; font-weight: 900; border-bottom: 2px solid #1e222d; padding-bottom: 10px; margin-bottom: 20px; text-shadow: 2px 2px 4px #000; }
    .stButton>button { border-radius: 2px; font-weight: 900; height: 60px; font-size: 20px; transition: 0.2s; border: none; text-transform: uppercase; }
    .buy-btn { background-color: #089981 !important; color: white !important; box-shadow: 0 4px #056656; }
    .buy-btn:active { box-shadow: 0 0 #056656; transform: translateY(4px); }
    .sell-btn { background-color: #f23645 !important; color: white !important; box-shadow: 0 4px #b22833; }
    .sell-btn:active { box-shadow: 0 0 #b22833; transform: translateY(4px); }
    .metric-card { background-color: #131722; padding: 20px; border-radius: 4px; border: 1px solid #2a2e39; text-align: center; }
    .stat-val { font-size: 24px; font-weight: bold; color: #ffffff; }
    .stat-label { font-size: 12px; color: #787b86; text-transform: uppercase; }
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
    
    # Realistik narx o'zgarishi (Volatility)
    move = np.random.normal(0, 25)
    new_p = last_close + move
    
    # XATO TO'G'IRLANDI: new_close o'rniga new_p ishlatiladi
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

# Indikatorlar (MA & RSI)
def calc_indicators(df):
    df['MA10'] = df['Close'].rolling(window=10).mean()
    df['MA30'] = df['Close'].rolling(window=30).mean()
    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    df['RSI'] = 100 - (100 / (1 + (gain/loss)))
    return df

df_final = calc_indicators(st.session_state.history)

# ==========================================
# 3. INTERFACE: TOP NAVIGATION
# ==========================================
st.markdown('<div class="main-header">KGO GLOBAL PRO TERMINAL 💹</div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="metric-card"><div class="stat-label">Account Balance</div><div class="stat-val">${st.session_state.balance:,.2f}</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="metric-card"><div class="stat-label">Active Symbol</div><div class="stat-val" style="color:#2962ff">BTC/USDT</div></div>', unsafe_allow_html=True)
with m3:
    color = "#00ff00" if current_p > df_final.iloc[-2]['Close'] else "#ff0000"
    st.markdown(f'<div class="metric-card"><div class="stat-label">Live Price</div><div class="stat-val" style="color:{color}">${current_p:,.2.2f}</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="metric-card"><div class="stat-label">Server Status</div><div class="stat-val" style="color:#00ff00">ONLINE</div></div>', unsafe_allow_html=True)

# ==========================================
# 4. MAIN CHART & TRADE PANEL
# ==========================================
left, right = st.columns([3.8, 1.2])

with left:
    # Advanced Multi-Subplot Chart
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.8, 0.2])
    
    # Candles
    fig.add_trace(go.Candlestick(
        x=df_final['Time'], open=df_final['Open'], high=df_final['High'],
        low=df_final['Low'], close=df_final['Close'],
        increasing_line_color='#089981', decreasing_line_color='#f23645', name="Price"
    ), row=1, col=1)
    
    # MA Lines
    fig.add_trace(go.Scatter(x=df_final['Time'], y=df_final['MA10'], line=dict(color='#2962ff', width=1.5), name="Fast MA"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df_final['Time'], y=df_final['MA30'], line=dict(color='#ff9800', width=1.5), name="Slow MA"), row=1, col=1)
    
    # RSI Subplot
    fig.add_trace(go.Scatter(x=df_final['Time'], y=df_final['RSI'], line=dict(color='#9b59b6', width=2), name="RSI"), row=2, col=1)
    fig.add_hline(y=70, line_dash="dot", line_color="#ff4b4b", row=2, col=1)
    fig.add_hline(y=30, line_dash="dot", line_color="#00ff00", row=2, col=1)

    fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=650, 
                      margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="black", plot_bgcolor="black")
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Trade History Table
    st.markdown("### 📜 Trading Log")
    if st.session_state.trades:
        st.table(pd.DataFrame(st.session_state.trades).tail(5))
    else:
        st.info("No trades executed in this session.")

with right:
    st.markdown("### 🛠 Execution")
    lots = st.number_input("Volume (Lots):", 0.01, 50.0, 0.10)
    st.write("---")
    
    # BUY BUTTON
    if st.button("BUY", key="buy", use_container_width=True, help="Market Buy"):
        st.session_state.trades.append({
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Action": "BUY", "Price": round(current_p, 2), "Lots": lots
        })
        st.success(f"Executed BUY at ${current_p:,.2f}")
    
    st.write("")
    
    # SELL BUTTON
    if st.button("SELL", key="sell", use_container_width=True, help="Market Sell"):
        st.session_state.trades.append({
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Action": "SELL", "Price": round(current_p, 2), "Lots": lots
        })
        st.error(f"Executed SELL at ${current_p:,.2f}")
    
    st.write("---")
    st.markdown("#### 📊 Market Stats")
    st.write(f"High (24h): {df_final['High'].max():,.2f}")
    st.write(f"Low (24h): {df_final['Low'].min():,.2f}")
    st.write(f"RSI Value: {round(df_final['RSI'].iloc[-1], 2)}")

# ==========================================
# 5. LIVE ENGINE
# ==========================================
time.sleep(1.2) # Tezlik (soniya)
st.rerun()
