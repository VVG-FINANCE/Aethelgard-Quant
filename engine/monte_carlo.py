import numpy as np

class MonteCarloSimulator:
    @staticmethod
    def simulate(current_price, volatility, tp_dist, sl_dist, simulations=500, steps=60):
        results = []
        dt = 1 # por minuto
        for _ in range(simulations):
            prices = [current_price]
            for _ in range(steps):
                change = np.random.normal(0, volatility)
                prices.append(prices[-1] + change)
            results.append(prices)
        
        results = np.array(results)
        prob_tp = np.mean(np.any(results >= current_price + tp_dist, axis=1))
        prob_sl = np.mean(np.any(results <= current_price - sl_dist, axis=1))
        
        return prob_tp, prob_sl, results
