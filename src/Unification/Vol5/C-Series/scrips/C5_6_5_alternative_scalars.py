import json
import math
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
LAKE_PATH = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant" / "zinc_kish_invariant.jsonl"

OUT_JSON = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant" / "C5_6_5_alternative_scalars_summary.json"
OUT_FIG = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant" / "C5_6_5_alternative_scalars.png"

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
    print("=== C5.6.5 Alternative Scalar Definitions ===")

    scalars = load_scalars(LAKE_PATH)

    alt_scaled = scalars * 0.9
    alt_squared = scalars ** 2
    alt_log = np.log1p(scalars)

    summary = {
        "full_scalar": stats(scalars),
        "scaled_0.9": stats(alt_scaled),
        "squared": stats(alt_squared),
        "log1p": stats(alt_log),
        "modulus": MODULUS,
    }

    with OUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    bins = 120

    axes[0].hist(alt_scaled, bins=bins, density=True, alpha=0.7, color="steelblue")
    axes[0].set_title("Scaled (0.9 × scalar)")

    axes[1].hist(alt_squared, bins=bins, density=True, alpha=0.7, color="orange")
    axes[1].set_title("Squared scalar")

    axes[2].hist(alt_log, bins=bins, density=True, alpha=0.7, color="green")
    axes[2].set_title("log(1 + scalar)")

    for ax in axes:
        ax.set_xlabel("Value")
        ax.set_ylabel("Density")

    plt.tight_layout()
    plt.savefig(OUT_FIG, dpi=300)
    plt.close()

    print(f"Saved: {OUT_JSON}")
    print(f"Saved: {OUT_FIG}")
    print("=== C5.6.5 COMPLETE ===")

if __name__ == "__main__":
    main()
