from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
import numpy as np


class FirmExitPredictor:
    def __init__(self):
        self.rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.gb_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
        self.is_trained = False

    def train_dummy_model(self):
        np.random.seed(42)
        n_samples = 500
        # Features: liquidity, debt_equity, turnover, demand, owner_age_norm,
        #           yrs_no_successor_norm, revenue_concentration, certs_at_risk_norm
        X = np.random.rand(n_samples, 8)

        # Weighted risk score — higher owner age + no successor + high debt = more exits
        risk_score = (
            0.15 * (1 - X[:, 0])   # low liquidity → risk
            + 0.10 * X[:, 1]       # high debt → risk
            + 0.10 * X[:, 2]       # high turnover → risk
            + 0.10 * (1 - X[:, 3]) # low demand → risk
            + 0.20 * X[:, 4]       # old owner → risk
            + 0.15 * X[:, 5]       # long time w/o successor → risk
            + 0.10 * X[:, 6]       # revenue concentration → risk
            + 0.10 * X[:, 7]       # certs at risk → risk
        )
        y = (risk_score + np.random.normal(0, 0.08, n_samples) > 0.5).astype(int)

        self.rf_model.fit(X, y)
        self.gb_model.fit(X, y)
        self.is_trained = True

    def predict_exit_probability(self, firm_features: list) -> float:
        if not self.is_trained:
            self.train_dummy_model()

        features_array = np.array(firm_features).reshape(1, -1)
        rf_prob = self.rf_model.predict_proba(features_array)[0][1]
        gb_prob = self.gb_model.predict_proba(features_array)[0][1]
        ensemble_prob = 0.5 * rf_prob + 0.5 * gb_prob
        return float(round(ensemble_prob, 4))