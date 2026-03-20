import numpy as np
import pandas as pd
from scipy.stats import norm

class QuantEngine:
    @staticmethod
    def calculate_hurst(series):
        """Calcula o expoente de Hurst para detectar persistência (H>0.5) ou reversão (H<0.5)"""
        lags = range(2, 20)
        tau = [np.sqrt(np.std(np.subtract(series[lag:], series[:-lag]))) for lag in lags]
        poly = np.polyfit(np.log(lags), np.log(tau), 1)
        return poly[0] * 2

    @staticmethod
    def z_score(series):
        return (series.iloc[-1] - series.mean()) / series.std()

    @staticmethod
    def calculate_volatility_regime(df):
        returns = 100 * df['Close'].pct_change().dropna()
        # Simplificação de regime de volatilidade (Rolling Std)
        return returns.rolling(window=20).std().iloc[-1]
