import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from data_manager import DataManager
from engine.core import ScoringEngine
from config import Config
import time

st.set_page_config(page_title="Aethelgard Quant | EURUSD", layout="wide")

# CSS para Mobile-First
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 1.8rem; }
    .stApp { background-color: #0e1117; color: white; }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("🇪🇺🇺🇸 EUR/USD Quant Engine")
    
    # Sidebar
    st.sidebar.header("Configurações")
    refresh_rate = st.sidebar.slider("Refresh (segundos)", 5, 60, 15)
    pip_adj = st.sidebar.number_input("Pip Adjustment", value=0.0000, format="%.4f")
    
    # Data Fetching
    df = DataManager.fetch_data()
    
    if df is not None:
        last_price = df['Close'].iloc[-1]
        prev_price = df['Close'].iloc[-2]
        change = (last_price - prev_price) * 10000 # em Pips
        
        # Top Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Price", f"{last_price:.5f}", f"{change:.1f} Pips")
        
        # Score Logic
        score = ScoringEngine.calculate_score(df)
        col2.metric("System Score", f"{score:.1f}%")
        
        # Status
        status = "COMPRA" if score > 65 else "VENDA" if score < 35 else "NEUTRO"
        col3.metric("Recomendação", status)

        # Plotly Chart
        fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['Open'], high=df['High'],
                low=df['Low'], close=df['Close'])])
        fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0,r=0,b=0,t=0))
        st.plotly_chart(fig, use_container_width=True)

        # Oportunidade Estruturada
        if score > 65 or score < 35:
            with st.expander("🎯 OPORTUNIDADE DETECTADA", expanded=True):
                st.write(f"**Sentido:** {status}")
                st.write(f"**Zonas de Entrada:** {last_price:.5f} | {last_price-0.0002:.5f}")
                st.write(f"**Take Profit:** {last_price + 0.0015 if status == 'COMPRA' else last_price - 0.0015:.5f}")
                st.write(f"**Stop Loss:** {last_price - 0.0010 if status == 'COMPRA' else last_price + 0.0010:.5f}")

    # Auto-refresh logic
    time.sleep(refresh_rate)
    st.rerun()

if __name__ == "__main__":
    main()
