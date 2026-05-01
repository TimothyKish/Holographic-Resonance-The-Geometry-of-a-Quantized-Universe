import json
import math
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
LAKE_PATH = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant" / "zinc_kish_invariant.jsonl"

OUT_JSON = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant" / "C5_6_3_bin_sensitivity_summary.json"
OUT_FIG = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant" / "C5_6_3_bin_sensitivity.png"

MODULUS = 16.0 / math.pi
BINS = [40, 80, 160, 240]

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

def stats(arr):
    return {
        "count": int(arr.size),
        "mean": float(np.mean(arr)),
        "std": float(np.std(arr)),
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
        "band_width": float(np.max(arr) - np.min(arr)),
        "band_fraction": float((np.max(arr) - np.min(arr)) / MODULUS),
    }

def main():
    print("=== C5.6.3 Bin Sensitivity ===")

    scalars = load_scalars(LAKE_PATH)
    summary = {"full": stats(scalars), "bins": {}}

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    axes = axes.flatten()

    for i, b in enumerate(BINS):
        ax = axes[i]
        ax.hist(scalars, bins=b, density=True, alpha=0.7, color="steelblue")
        ax.set_title(f"{b} bins")
        ax.set_xlabel("Scalar invariant")
        ax.set_ylabel("Density")
        summary["bins"][str(b)] = stats(scalars)

    plt.tight_layout()
    plt.savefig(OUT_FIG, dpi=300)
    plt.close()

    with OUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))
    print(f"Saved: {OUT_JSON}")
    print(f"Saved: {OUT_FIG}")
    print("=== C5.6.3 COMPLETE ===")

if __name__ == "__main__":
    main()
