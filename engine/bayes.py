class BayesianInference:
    @staticmethod
    def update_probability(prior, likelihood_success, likelihood_fail, observed_success):
        """
        Calcula a probabilidade posterior usando o Teorema de Bayes.
        """
        if observed_success:
            numerator = likelihood_success * prior
        else:
            numerator = (1 - likelihood_success) * prior
            
        denominator = (likelihood_success * prior) + (likelihood_fail * (1 - prior))
        return numerator / denominator if denominator != 0 else prior
