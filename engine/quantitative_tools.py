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
import numpy as np

class KalmanFilter:
    def __init__(self, process_variance=1e-5, measurement_variance=1e-3):
        self.process_variance = process_variance
        self.measurement_variance = measurement_variance
        self.posteri_estimate = 0.0
        self.posteri_error_estimate = 1.0

    def update(self, measurement):
        priori_estimate = self.posteri_estimate
        priori_error_estimate = self.posteri_error_estimate + self.process_variance

        blending_factor = priori_error_estimate / (priori_error_estimate + self.measurement_variance)
        self.posteri_estimate = priori_estimate + blending_factor * (measurement - priori_estimate)
        self.posteri_error_estimate = (1 - blending_factor) * priori_error_estimate
        return self.posteri_estimate
