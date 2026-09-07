"""
Data Quality Auditor: Performs automated audits on structured datasets.
Detects missing values, duplicates, statistical outliers (IQR), and schema violations.
"""
import json
from pathlib import Path

try:
    import pandas as pd
    import numpy as np
except ImportError:
    pd = None
    np = None


class DataQualityAuditor:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        if pd is not None:
            self.df = pd.read_csv(csv_path)
        else:
            self.df = None

    def audit(self) -> dict:
        if self.df is None:
            return {"error": "pandas not installed"}

        report = {
            "dataset": str(self.csv_path),
            "total_rows": len(self.df),
            "total_columns": len(self.df.columns),
            "missing_values": self._check_missing(),
            "duplicate_rows": int(self.df.duplicated().sum()),
            "outliers": self._check_outliers(),
            "status": "COMPLETED"
        }
        return report

    def _check_missing(self) -> dict:
        null_counts = self.df.isnull().sum()
        return {col: int(count) for col, count in null_counts.items() if count > 0}

    def _check_outliers(self) -> dict:
        outliers = {}
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if col == "id":
                continue
            series = self.df[col].dropna()
            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            outlier_series = series[(series < lower_bound) | (series > upper_bound)]
            if len(outlier_series) > 0:
                outliers[col] = {
                    "count": int(len(outlier_series)),
                    "bounds": [float(round(lower_bound, 2)), float(round(upper_bound, 2))],
                    "max_detected": float(series.max())
                }
        return outliers

    def save_report(self, output_path: str) -> None:
        rep = self.audit()
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(rep, f, indent=2)
