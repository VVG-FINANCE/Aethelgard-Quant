from engine.quantitative_tools import QuantEngine
from engine.monte_carlo import MonteCarloSimulator
import pandas_ta as ta

class ScoringEngine:
    @classmethod
    def calculate_score(cls, df):
        # 1. Indicadores Técnicos
        rsi = ta.rsi(df['Close'], length=14).iloc[-1]
        
        # 2. Econofísica
        hurst = QuantEngine.calculate_hurst(df['Close'].values)
        
        # 3. Monte Carlo
        vol = df['Close'].pct_change().std()
        prob_tp, prob_sl, _ = MonteCarloSimulator.simulate(df['Close'].iloc[-1], vol, 0.0010, 0.0008)
        
        # Lógica de Score
        score = 50
        # Tendência e Persistência
        if hurst > 0.55 and rsi > 55: score += 15
        if hurst < 0.45 and rsi > 70: score -= 10 # Reversão provável
        
        # Probabilidade Estatística
        score += (prob_tp - prob_sl) * 100
        
        return np.clip(score, 0, 100)
