import json
import math
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
LAKE_PATH = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant" / "zinc_kish_invariant.jsonl"

OUT_JSON = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant" / "C5_6_2_bootstrap_summary.json"
OUT_FIG = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant" / "C5_6_2_bootstrap_stability.png"

BOOTSTRAP_SAMPLES = 1000  # fast + statistically strong
MODULUS = 16.0 / math.pi

def load_scalars(path):
    vals = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            s = obj.get("scalar_invariant", None)
            if s is not None:
                vals.append(float(s))
    return np.array(vals, dtype=float)

def main():
    print("=== C5.6.2 Bootstrap Stability ===")

    scalars = load_scalars(LAKE_PATH)
    n = scalars.size

    means = []
    stds = []

    for _ in range(BOOTSTRAP_SAMPLES):
        sample = np.random.choice(scalars, size=n, replace=True)
        means.append(float(np.mean(sample)))
        stds.append(float(np.std(sample)))

    means = np.array(means)
    stds = np.array(stds)

    summary = {
        "bootstrap_samples": BOOTSTRAP_SAMPLES,
        "mean_of_means": float(np.mean(means)),
        "std_of_means": float(np.std(means)),
        "mean_of_stds": float(np.mean(stds)),
        "std_of_stds": float(np.std(stds)),
        "full_mean": float(np.mean(scalars)),
        "full_std": float(np.std(scalars)),
        "modulus": MODULUS,
    }

    with OUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))

    # Plot bootstrap distributions
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    axes[0].hist(means, bins=60, color="steelblue", alpha=0.7)
    axes[0].axvline(summary["full_mean"], color="red", linestyle="--")
    axes[0].set_title("Bootstrap Means")
    axes[0].set_xlabel("Mean scalar")
    axes[0].set_ylabel("Frequency")

    axes[1].hist(stds, bins=60, color="orange", alpha=0.7)
    axes[1].axvline(summary["full_std"], color="red", linestyle="--")
    axes[1].set_title("Bootstrap Standard Deviations")
    axes[1].set_xlabel("Std scalar")
    axes[1].set_ylabel("Frequency")

    plt.tight_layout()
    plt.savefig(OUT_FIG, dpi=300)
    plt.close()

    print(f"Saved: {OUT_JSON}")
    print(f"Saved: {OUT_FIG}")
    print("=== C5.6.2 COMPLETE ===")

if __name__ == "__main__":
    main()
