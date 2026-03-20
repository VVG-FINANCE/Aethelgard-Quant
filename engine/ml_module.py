from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

class MLDirectionalModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, max_depth=5)
        self.is_trained = False

    def prepare_features(self, df):
        data = df.copy()
        data['Returns'] = data['Close'].pct_change()
        data['Vol'] = data['Returns'].rolling(10).std()
        data['Target'] = (data['Returns'].shift(-1) > 0).astype(int)
        return data.dropna()

    def train(self, df):
        features = self.prepare_features(df)
        X = features[['Returns', 'Vol']]
        y = features['Target']
        self.model.fit(X, y)
        self.is_trained = True

    def predict_proba(self, current_features):
        if not self.is_trained: return 0.5
        return self.model.predict_proba(current_features)[0][1]
