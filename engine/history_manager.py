import json
import os

class HistoryManager:
    FILE_PATH = "data/signals_history.json"

    @classmethod
    def save_signal(cls, signal_data):
        history = cls.load_history()
        history.append(signal_data)
        if not os.path.exists("data"): os.makedirs("data")
        with open(cls.FILE_PATH, 'w') as f:
            json.dump(history, f)

    @classmethod
    def load_history(cls):
        if os.path.exists(cls.FILE_PATH):
            with open(cls.FILE_PATH, 'r') as f:
                return json.load(f)
        return []
