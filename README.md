# Python Automated Data Validation & QA Pipeline

An automated data quality assurance and model regression testing framework designed to validate data integrity, detect anomalies, and guard against machine learning model degradation.

## Pipeline Architecture
```
[ Raw Ingested Data ]
         |
         v
[ DataQualityAuditor ] ---------> [ Missing Values / Outlier Detection ]
         |
         v
[ PipelineValidator ] ----------> [ Transformation & Schema Contracts ]
         |
         v
[ ModelRegressionTester ] ------> [ F1 / Accuracy / Recall Baselines ]
         |
         v
[ Reports & Visualizations ] ---> [ JSON Audit Logs & Matplotlib Plots ]
```

## Features
- **Statistical Outlier Detection:** Interquartile Range (IQR 1.5x) rule dynamically flags numerical anomalies.
- **Missing Value & Schema Audits:** Identifies null values, type mismatches, and duplicate records.
- **Pipeline Stage Contracts:** Enforces row-preservation and non-null constraints across data transformation stages.
- **Model Regression Benchmarking:** Evaluates candidate model predictions against saved production baselines; flags performance drops exceeding configurable threshold.
- **Visual Analytics:** Generates dark-themed comparison charts of model metrics.

## Quickstart
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the end-to-end QA pipeline
python main.py
```
