import yfinance as yf
import pandas as pd
from config import Config

class DataManager:
    @staticmethod
    def fetch_data(symbol=Config.SYMBOL, interval="1m", period="1d"):
        try:
            df = yf.download(symbol, interval=interval, period=period, progress=False)
            if df.empty: return None
            # Ajuste de Pips
            df['Close'] = df['Close'] + Config.PIP_ADJUSTMENT
            return df
        except Exception as e:
            return None

    @staticmethod
    def get_latest_price(df):
        return df['Close'].iloc[-1]
