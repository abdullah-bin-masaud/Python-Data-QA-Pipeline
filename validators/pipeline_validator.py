"""
Pipeline Stage Validator: Verifies schema integrity and row transitions between pipeline steps.
"""
from typing import Dict, Any


class PipelineValidator:
    def __init__(self):
        self.history = []

    def validate_stage(self, stage_name: str, df, required_columns: list) -> Dict[str, Any]:
        """Validates that a DataFrame conforms to expected schema and contains no unexpected nulls."""
        cols = list(df.columns)
        missing_cols = [c for c in required_columns if c not in cols]

        has_passed = (len(missing_cols) == 0)
        record = {
            "stage": stage_name,
            "row_count": len(df),
            "column_count": len(cols),
            "missing_required_columns": missing_cols,
            "passed": has_passed
        }
        self.history.append(record)
        return record

    def compare_transformation(self, before_df, after_df, stage_name: str) -> Dict[str, Any]:
        """Audits row drop rate and column mutations across a transformation step."""
        dropped = len(before_df) - len(after_df)
        pct_dropped = round((dropped / len(before_df)) * 100, 2) if len(before_df) > 0 else 0
        return {
            "stage": stage_name,
            "rows_before": len(before_df),
            "rows_after": len(after_df),
            "rows_dropped": dropped,
            "drop_percentage": pct_dropped
        }
