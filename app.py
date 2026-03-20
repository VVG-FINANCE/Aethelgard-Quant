import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import time
import os

# Importações dos nossos módulos
from config import Config
from data_manager import DataManager
from engine.core import ScoringEngine
from engine.quantitative_tools import KalmanFilter
from engine.ml_module import MLDirectionalModel
from engine.history_manager import HistoryManager

# Configuração da Página
st.set_page_config(page_title="Aethelgard Quant | EURUSD", layout="wide")

# Estilização CSS
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 1.8rem; }
    .stApp { background-color: #0e1117; color: white; }
    .main-card { background: #1e222d; padding: 20px; border-radius: 10px; border: 1px solid #363c4e; }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("🇪🇺🇺🇸 Aethelgard Quant Engine")
    st.caption("Sistema de Análise Quantitativa e Econofísica - v1.0")

    # --- SIDEBAR CONFIGURAÇÕES ---
    st.sidebar.header("⚙️ Painel de Controle")
    refresh_rate = st.sidebar.slider("Refresh (segundos)", 5, 60, 15)
    
    st.sidebar.subheader("Parâmetros Quant")
    vol_lookback = st.sidebar.number_input("Lookback Volatilidade", 10, 50, 20)
    
    # --- COLETA DE DADOS ---
    with st.spinner('Sincronizando com o mercado...'):
        df = DataManager.fetch_data()

    if df is not None:
        # Certifica que a coluna Close é numérica e remove erros de conversão
df['Close'] = pd.to_numeric(df['Close'], errors='coerce')

# Remove linhas que ficaram com valor nulo (NaN) após a conversão
df = df.dropna(subset=['Close'])

# Agora sim, roda o Filtro de Kalman
if not df.empty:
    kf = KalmanFilter(process_variance=1e-5, measurement_variance=1e-3)
    df['Kalman'] = [kf.update(x) for x in df['Close']]

        # 1. Aplicação do Filtro de Kalman (Redução de Ruído)
        kf = KalmanFilter(process_variance=1e-5, measurement_variance=1e-3)
        df['Kalman'] = [kf.update(x) for x in df['Close']]

        # 2. Motor de Machine Learning (Predição de Direção)
        ml_engine = MLDirectionalModel()
        ml_engine.train(df)
        # Preparar última linha para predição
        last_ret = df['Close'].pct_change().tail(1).values.reshape(-1, 1)
        ml_prob = ml_engine.predict_proba(last_ret)

        # 3. Cálculo de Score Base (Técnico + Monte Carlo + Hurst)
        base_score = ScoringEngine.calculate_score(df)

        # 4. Fusão de Inteligência (Score Final Ponderado)
        # 70% Modelos Matemáticos/Econofísica + 30% Probabilidade ML
        final_score = (base_score * 0.7) + (ml_prob * 100 * 0.3)

        # --- INTERFACE DE MÉTRICAS ---
        last_price = df['Close'].iloc[-1]
        prev_price = df['Close'].iloc[-2]
        change_pips = (last_price - prev_price) * 10000

        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("PREÇO ATUAL", f"{last_price:.5f}", f"{change_pips:.1f} Pips")
        with m2:
            st.metric("CONFIANÇA DO SISTEMA", f"{final_score:.1f}%")
        with m3:
            status = "FORTE COMPRA" if final_score > 70 else "FORTE VENDA" if final_score < 30 else "NEUTRO"
            st.metric("SENTIMENTO", status)

        # --- GRÁFICO AVANÇADO ---
        fig = go.Figure()
        # Candlesticks
        fig.add_trace(go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'], name="Market"
        ))
        # Linha Kalman
        fig.add_trace(go.Scatter(
            x=df.index, y=df['Kalman'], 
            name="Filtro de Kalman", 
            line=dict(color='#FFD700', width=1.5)
        ))
        
        fig.update_layout(
            template="plotly_dark", 
            height=500, 
            margin=dict(l=0,r=0,b=0,t=0),
            xaxis_rangeslider_visible=False
        )
        st.plotly_chart(fig, use_container_width=True)

        # --- GERADOR DE OPORTUNIDADES ---
        if final_score > 65 or final_score < 35:
            st.success(f"🎯 Oportunidade Estruturada Detectada: {status}")
            c1, c2, c3 = st.columns(3)
            
            tipo = "BUY" if final_score > 65 else "SELL"
            adj = 0.0015 if tipo == "BUY" else -0.0015
            
            c1.info(f"**ENTRADA**\n\n{last_price:.5f}")
            c2.success(f"**TAKE PROFIT**\n\n{last_price + adj:.5f}")
            c3.error(f"**STOP LOSS**\n\n{last_price - (adj/1.5):.5f}")
            
            # Persistência do sinal
            if st.button("Logar Sinal no Histórico"):
                signal = {
                    "timestamp": str(df.index[-1]),
                    "type": tipo,
                    "price": last_price,
                    "score": final_score
                }
                HistoryManager.save_signal(signal)
                st.toast("Sinal salvo com sucesso!")

        # --- RODAPÉ E STATUS ---
        with st.sidebar:
            st.divider()
            st.write("### 📜 Histórico Recente")
            history = HistoryManager.load_history()
            if history:
                for item in history[-5:]: # Mostrar últimos 5
                    st.caption(f"{item['timestamp']} | {item['type']} | Score: {item['score']:.1f}")
            
            if st.button("Limpar Dados"):
                if os.path.exists("data/signals_history.json"):
                    os.remove("data/signals_history.json")
                    st.rerun()

    # Loop de Atualização
    time.sleep(refresh_rate)
    st.rerun()

if __name__ == "__main__":
    main()
