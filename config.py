import streamlit as st

class Config:
    SYMBOL = "EURUSD=X"
    PIP_ADJUSTMENT = 0.0000  # Ajuste manual de spread/delay
    TIMEFRAME = "1m"
    WINDOW_SIZE = 100
    
    # Parâmetros de Risco
    DEFAULT_TP_PIPS = 15
    DEFAULT_SL_PIPS = 10
    
    # Cores
    COLOR_UP = "#26a69a"
    COLOR_DOWN = "#ef5350"
    
    @staticmethod
    def get_api_interval(fail_count):
        intervals = [5, 10, 15, 20, 30, 60]
        return intervals[min(fail_count, len(intervals)-1)]
