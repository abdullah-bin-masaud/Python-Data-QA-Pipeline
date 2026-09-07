"""
Visual reporting module generating diagnostic charts for data quality and model regression.
"""
from pathlib import Path

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


def plot_metrics_comparison(metrics_dict: dict, output_path: str):
    """Generates comparison bar chart between baseline and candidate models."""
    if plt is None:
        return

    plt.style.use("dark_background")
    labels = list(metrics_dict.keys())
    baseline_vals = [metrics_dict[k]["baseline"] for k in labels]
    updated_vals = [metrics_dict[k]["updated"] for k in labels]

    x = range(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar([i - width/2 for i in x], baseline_vals, width, label="Baseline Model", color="#00d4ff")
    ax.bar([i + width/2 for i in x], updated_vals, width, label="Candidate Model", color="#f0883e")

    ax.set_ylabel("Score (0.0 - 1.0)")
    ax.set_title("Model Regression Testing: Metric Performance Comparison")
    ax.set_xticks(list(x))
    ax.set_xticklabels([l.upper() for l in labels])
    ax.set_ylim(0.5, 1.05)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
