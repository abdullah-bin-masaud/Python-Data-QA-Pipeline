"""
Model Regression Tester: Assesses predictive performance degradation between baseline and updated models.
"""
try:
    import pandas as pd
    from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
except ImportError:
    pd = None


class ModelRegressionTester:
    def __init__(self, baseline_csv: str, updated_csv: str):
        self.baseline_csv = baseline_csv
        self.updated_csv = updated_csv

    def evaluate(self, degradation_threshold: float = 0.02) -> dict:
        if pd is None:
            return {"error": "scikit-learn / pandas not installed"}

        df_base = pd.read_csv(self.baseline_csv)
        df_upd = pd.read_csv(self.updated_csv)

        y_true = df_base["y_true"]
        y_base = df_base["y_pred"]
        y_upd = df_upd["y_pred"]

        metrics = {
            "accuracy": {
                "baseline": round(accuracy_score(y_true, y_base), 4),
                "updated": round(accuracy_score(y_true, y_upd), 4),
            },
            "f1": {
                "baseline": round(f1_score(y_true, y_base), 4),
                "updated": round(f1_score(y_true, y_upd), 4),
            },
            "precision": {
                "baseline": round(precision_score(y_true, y_base), 4),
                "updated": round(precision_score(y_true, y_upd), 4),
            },
            "recall": {
                "baseline": round(recall_score(y_true, y_base), 4),
                "updated": round(recall_score(y_true, y_upd), 4),
            }
        }

        # Calculate deltas and regression flags
        has_degradation = False
        for k, v in metrics.items():
            delta = round(v["updated"] - v["baseline"], 4)
            v["delta"] = delta
            if delta < -degradation_threshold:
                v["status"] = "REGRESSION DETECTED"
                has_degradation = True
            else:
                v["status"] = "PASSED"

        return {
            "metrics": metrics,
            "overall_status": "FAILED (Regression Detected)" if has_degradation else "PASSED",
            "threshold": degradation_threshold
        }
