"""
Main QA Pipeline Orchestrator.
Executes end-to-end audit:
1. Generates synthetic datasets
2. Audits raw data quality (missing values, duplicates, outliers)
3. Validates pipeline transformation stages
4. Evaluates model regression performance
5. Exports visual plots and JSON audit logs
"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from data.generate_sample_data import generate_raw_data, generate_model_predictions
from validators.data_quality import DataQualityAuditor
from validators.pipeline_validator import PipelineValidator
from validators.model_regression import ModelRegressionTester
from visualizations.plot_report import plot_metrics_comparison

PROJECT_ROOT = Path(__file__).parent


def run_pipeline():
    print("================================================================")
    print("  AUTOMATED DATA VALIDATION & MODEL REGRESSION QA PIPELINE")
    print("================================================================")

    # 1. Generate datasets
    print("\n[STEP 1] Generating test datasets...")
    generate_raw_data()
    generate_model_predictions()

    # 2. Audit Data Quality
    print("\n[STEP 2] Running DataQualityAuditor on raw dataset...")
    raw_csv = str(PROJECT_ROOT / "data" / "raw_dataset.csv")
    auditor = DataQualityAuditor(raw_csv)
    audit_report = auditor.audit()

    print(f" -> Total Rows Audited: {audit_report.get('total_rows')}")
    print(f" -> Duplicate Rows Found: {audit_report.get('duplicate_rows')}")
    print(f" -> Missing Values: {audit_report.get('missing_values')}")
    print(f" -> Outliers Detected: {list(audit_report.get('outliers', {}).keys())}")

    qa_report_path = PROJECT_ROOT / "reports" / "QA_AUDIT_REPORT.json"
    with open(qa_report_path, "w", encoding="utf-8") as f:
        json.dump(audit_report, f, indent=2)
    print(f" -> Audit log saved to {qa_report_path}")

    # 3. Model Regression Testing
    print("\n[STEP 3] Executing Model Regression Tests...")
    base_csv = str(PROJECT_ROOT / "data" / "model_predictions_baseline.csv")
    upd_csv = str(PROJECT_ROOT / "data" / "model_predictions_updated.csv")
    tester = ModelRegressionTester(base_csv, upd_csv)
    reg_results = tester.evaluate(degradation_threshold=0.02)

    print(f" -> Overall Evaluation: {reg_results.get('overall_status')}")
    for metric_name, details in reg_results.get("metrics", {}).items():
        print(f"    * {metric_name.upper():<10}: Base={details['baseline']} | Upd={details['updated']} | Delta={details['delta']:+0.4f} [{details['status']}]")

    # 4. Generate Visualizations
    plot_output = PROJECT_ROOT / "reports" / "plots" / "model_regression_comparison.png"
    if "metrics" in reg_results:
        plot_metrics_comparison(reg_results["metrics"], str(plot_output))
        print(f"\n[STEP 4] Metric comparison chart generated: {plot_output}")

    print("\n================================================================")
    print("  QA PIPELINE EXECUTION SUMMARY: SUCCESSFUL")
    print("================================================================")


if __name__ == "__main__":
    run_pipeline()
