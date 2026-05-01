import json
import math
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
LAKE_PATH = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant" / "zinc_kish_invariant.jsonl"

OUT_JSON = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant" / "C5_6_1_subsampling_summary.json"
OUT_FIG = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant" / "C5_6_1_subsampling_stability.png"

MODULUS = 16.0 / math.pi

SUBSAMPLES = {
    "10k": 10_000,
    "20k": 20_000,
    "40k": 40_000,
}

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
    print("=== C5.6.1 Subsampling Stability ===")

    scalars = load_scalars(LAKE_PATH)
    full_stats = stats(scalars)

    summary = {"full": full_stats, "subsamples": {}}

    fig, axes = plt.subplots(3, 1, figsize=(8, 10))
    bins = 120

    for i, (label, size) in enumerate(SUBSAMPLES.items()):
        if size > scalars.size:
            continue

        sub = np.random.choice(scalars, size=size, replace=False)
        summary["subsamples"][label] = stats(sub)

        ax = axes[i]
        ax.hist(sub, bins=bins, density=True, alpha=0.7, color="steelblue")
        ax.set_title(f"{label} subsample")
        ax.set_xlabel("Scalar invariant")
        ax.set_ylabel("Density")

    plt.tight_layout()
    plt.savefig(OUT_FIG, dpi=300)
    plt.close()

    with OUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))
    print(f"Saved: {OUT_JSON}")
    print(f"Saved: {OUT_FIG}")
    print("=== C5.6.1 COMPLETE ===")

if __name__ == "__main__":
    main()
