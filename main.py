import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# --- [1. CYBER-MILLIY DESIGN] ---
st.set_page_config(page_title="KGO TRADING PRO", layout="wide", page_icon="📈")

st.markdown("""
<style>
    /* Fon va Milliy naqsh */
    .stApp {
        background-color: #f0f7f9;
        background-image: url("https://www.transparenttextures.com/patterns/oriental-tiles.png");
        color: #1a3a5a;
    }
    
    /* Sarlavha dizayni */
    .main-header {
        text-align: center;
        color: #0088cc;
        font-family: 'Arial Black', sans-serif;
        text-transform: uppercase;
        padding: 20px;
        border-bottom: 3px double #0088cc;
        margin-bottom: 30px;
    }

    /* Signal Kartochkasi */
    .signal-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #00c6ff;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
    }

    /* BUY/SELL Tugmalari - Milliy uslub */
    .stButton>button {
        width: 100%;
        border-radius: 30px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button[key="buy_btn"] {
        background: linear-gradient(90deg, #00e676, #00c853);
        color: white;
    }
    .stButton>button[key="sell_btn"] {
        background: linear-gradient(90deg, #ff1744, #d50000);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- [2. VIRTUAL MA'LUMOT YARATISH (Real data yo'qligi uchun)] ---
def generate_data(days=365):
    np.random.seed(42)
    dates = [datetime.now() - timedelta(days=x) for x in range(days)]
    dates.reverse()
    price = 60000 + np.cumsum(np.random.randn(days) * 500)
    high = price + np.random.rand(days) * 1000
    low = price - np.random.rand(days) * 1000
    volume = np.random.randint(1000, 5000, days)
    
    data = pd.DataFrame({
        'Date': dates,
        'Open': price,
        'High': high,
        'Low': low,
        'Close': price + np.random.randn(days) * 200,
        'Volume': volume
    })
    return data

# --- [3. KGO AI SIGNAL VA ZONALAR LOGIKASI] ---
def calculate_signals(data):
    # RSI (Relative Strength Index) - 14 kunlik
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # Moving Average (MA) - 20 kunlik
    data['MA20'] = data['Close'].rolling(window=20).mean()

    # KGO AI Signal
    latest = data.iloc[-1]
    prev = data.iloc[-2]
    
    signal = "NEUTRAL"
    strength = "0%"

    if latest['RSI'] < 30 and latest['Close'] < latest['MA20']:
        signal = "STRONG BUY"
        strength = "85%"
    elif latest['RSI'] > 70 and latest['Close'] > latest['MA20']:
        signal = "STRONG SELL"
        strength = "90%"
    elif latest['MA20'] > prev['MA20'] and latest['Close'] > latest['MA20']:
        signal = "BUY"
        strength = "65%"
    elif latest['MA20'] < prev['MA20'] and latest['Close'] < latest['MA20']:
        signal = "SELL"
        strength = "70%"
        
    return signal, strength, latest

# --- [4. SAYT INTERFEYSI] ---
st.markdown('<h1 class="main-header">📈 KGO TRADING ULTIMATE PRO</h1>', unsafe_allow_html=True)
st.write("<p style='text-align:center;'>Milliy Tahlil va AI Signallar Platformasi</p>", unsafe_allow_html=True)

# sidebar
st.sidebar.markdown(f"<h2 style='color:#0072ff;'>👤 KGO Treder Junior</h2>", unsafe_allow_html=True)
symbol = st.sidebar.selectbox("Aktiv:", ["Bitcoin (BTC/USDT)", "Ethereum (ETH/USDT)", "KGO Coin (KGO/USDT)"])
timeframe = st.sidebar.radio("Taymfreym:", ["1 Min", "5 Min", "15 Min", "1 H", "1 D"])

# Ma'lumotlarni yuklash (simulyatsiya)
df = generate_data()
signal, strength, latest_data = calculate_signals(df)

# --- [5. GRAFIKA VA CHIZISH] ---
# O'zbekona ranglar palitrasi
KGO_COLORS = {
    'bg': '#f0f7f9',
    'buy': '#00c853', # O'zbekiston yashili
    'sell': '#d50000', # O'zbekiston qizili
    'ma': '#00c6ff', # O'zbekiston ko'ki
    'grid': 'rgba(26, 58, 90, 0.05)'
}

fig = go.Figure()

# Shamchalar (Candlesticks)
fig.add_trace(go.Candlestick(
    x=df['Date'],
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close'],
    name='Narx',
    increasing_line_color=KGO_COLORS['buy'],
    decreasing_line_color=KGO_COLORS['sell']
))

# Moving Average Line
fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df['MA20'],
    name='MA20 (KGO Zona)',
    line=dict(color=KGO_COLORS['ma'], width=2)
))

# BUY/SELL Zonalarni chizish (Simulyatsiya)
# Pastki zona (BUY ZONE)
fig.add_shape(type="rect",
    x0=df['Date'].iloc[0], y0=latest_data['Low'] * 0.98,
    x1=df['Date'].iloc[-1], y1=latest_data['Low'] * 1.0,
    fillcolor=KGO_COLORS['buy'], opacity=0.1, line_width=0
)
# Yuqori zona (SELL ZONE)
fig.add_shape(type="rect",
    x0=df['Date'].iloc[0], y0=latest_data['High'] * 1.0,
    x1=df['Date'].iloc[-1], y1=latest_data['High'] * 1.02,
    fillcolor=KGO_COLORS['sell'], opacity=0.1, line_width=0
)

# Grafik sozlamalari (Milliy dizayn)
fig.update_layout(
    title=f'{symbol} - KGO Tahlil Grafigi ({timeframe})',
    xaxis_title='Vaqt',
    yaxis_title='Narx ($)',
    xaxis_rangeslider_visible=False,
    paper_bgcolor=KGO_COLORS['bg'],
    plot_bgcolor=KGO_COLORS['bg'],
    font=dict(color='#1a3a5a'),
    xaxis=dict(gridcolor=KGO_COLORS['grid']),
    yaxis=dict(gridcolor=KGO_COLORS['grid']),
    margin=dict(l=0, r=0, t=40, b=0),
    height=600
)

# --- [6. ASOSIY BLOK: SIGNAL VA BOSHQARUV] ---
col1, col2 = st.columns([3, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # KGO AI Signal paneli
    st.markdown(f"""
    <div class="signal-card">
        <h3>🤖 KGO AI SIGNAL</h3>
        <hr>
        <h1 style="color:{KGO_COLORS['buy'] if 'BUY' in signal else KGO_COLORS['sell'] if 'SELL' in signal else 'gray'};">
            {signal}
        </td>
        <p>Signal Kuchi: {strength}</p>
        <small>Oxirgi Narx: ${latest_data['Close']:.2f}</small>
    </div>
    """, unsafe_allow_html=True)

    # Buy/Sell o'yini (Tugmalar)
    st.write("### Savdo qilish")
    amount = st.number_input("Miqdorni kiriting ($):", value=100, step=10)
    col3, col4 = st.columns(2)
    with col3:
        if st.button("📈 BUY", key="buy_btn"):
            st.success(f"Xarid qilindi: {amount}$")
    with col4:
        if st.button("📉 SELL", key="sell_btn"):
            st.error(f"Sotildi: {amount}$")

    # Qo'shimcha indikator
    st.write("---")
    st.write(f"RSI (14): {latest_data['RSI']:.2f}")
    if latest_data['RSI'] < 30:
        st.warning("Narx juda past, sotib olish vaqti bo'lishi mumkin!")
    elif latest_data['RSI'] > 70:
        st.warning("Narx juda baland, sotish vaqti bo'lishi mumkin!")

# --- [FOOTER] ---
st.sidebar.markdown("<br><br><br><p style='text-align:center; opacity:0.5;'>KGO Trading | Junior FinTech 2026</p>", unsafe_allow_html=True)
