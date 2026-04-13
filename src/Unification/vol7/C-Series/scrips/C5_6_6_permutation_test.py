import json
import math
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
LAKE_PATH = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant" / "zinc_kish_invariant.jsonl"

OUT_JSON = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant" / "C5_6_6_permutation_summary.json"
OUT_FIG = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant" / "C5_6_6_permutation_test.png"

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
    print("=== C5.6.6 Permutation Test ===")

    scalars = load_scalars(LAKE_PATH)

    permuted = np.random.permutation(scalars)

    summary = {
        "real": stats(scalars),
        "permuted": stats(permuted),
        "modulus": MODULUS,
    }

    with OUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    bins = 120

    axes[0].hist(scalars, bins=bins, density=True, alpha=0.7, color="steelblue")
    axes[0].set_title("Real scalar distribution")
    axes[0].set_xlabel("Scalar invariant")
    axes[0].set_ylabel("Density")

    axes[1].hist(permuted, bins=bins, density=True, alpha=0.7, color="orange")
    axes[1].set_title("Permuted scalar distribution")
    axes[1].set_xlabel("Scalar invariant")
    axes[1].set_ylabel("Density")

    plt.tight_layout()
    plt.savefig(OUT_FIG, dpi=300)
    plt.close()

    print(f"Saved: {OUT_JSON}")
    print(f"Saved: {OUT_FIG}")
    print("=== C5.6.6 COMPLETE ===")

if __name__ == "__main__":
    main()
