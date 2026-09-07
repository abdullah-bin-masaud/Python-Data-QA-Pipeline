"""
Generates synthetic datasets with intentionally injected anomalies for QA testing.
Creates:
    - raw_dataset.csv (missing fields, extreme outliers, duplicate rows, format violations)
    - model_predictions_baseline.csv (ground truth + baseline predictions)
    - model_predictions_updated.csv (updated model predictions with intentional minor degradation)
"""
import random
import csv
from pathlib import Path

DATA_DIR = Path(__file__).parent


def generate_raw_data(num_rows: int = 1000):
    departments = ["Engineering", "Quality Assurance", "DevOps", "Data Science", "Embedded Systems"]
    rows = []

    for i in range(1, num_rows + 1):
        age = random.randint(22, 58)
        salary = random.randint(45000, 160000)
        dept = random.choice(departments)
        score = round(random.uniform(60.0, 99.0), 1)
        email = f"emp{i}@company.org"

        # Injected anomalies:
        if i % 25 == 0:
            salary = 9999999  # Extreme Outlier
        if i % 30 == 0:
            age = None        # Missing Value
        if i % 40 == 0:
            email = "invalid_email_format"  # Format violation

        rows.append([i, age, salary, dept, score, email])

    # Inject duplicate records
    for d in range(15):
        rows.append(rows[d * 10])

    csv_path = DATA_DIR / "raw_dataset.csv"
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "age", "salary", "department", "quality_score", "email"])
        writer.writerows(rows)

    print(f"[*] Generated {len(rows)} raw rows at {csv_path}")


def generate_model_predictions(num_samples: int = 500):
    baseline_rows = []
    updated_rows = []

    for i in range(num_samples):
        y_true = random.choice([0, 1])

        # Baseline: ~88% accurate
        if random.random() < 0.88:
            y_base = y_true
        else:
            y_base = 1 - y_true

        # Updated: ~84% accurate (simulating a slight regression to detect)
        if random.random() < 0.84:
            y_upd = y_true
        else:
            y_upd = 1 - y_true

        baseline_rows.append([i, y_true, y_base])
        updated_rows.append([i, y_true, y_upd])

    with open(DATA_DIR / "model_predictions_baseline.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["sample_id", "y_true", "y_pred"])
        w.writerows(baseline_rows)

    with open(DATA_DIR / "model_predictions_updated.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["sample_id", "y_true", "y_pred"])
        w.writerows(updated_rows)

    print("[*] Generated baseline and candidate model prediction datasets.")


if __name__ == "__main__":
    generate_raw_data()
    generate_model_predictions()
