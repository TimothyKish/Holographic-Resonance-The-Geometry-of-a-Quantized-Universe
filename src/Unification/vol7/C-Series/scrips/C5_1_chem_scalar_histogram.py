import json
import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

# Paths
BASE_DIR = Path(__file__).resolve().parent
LAKE_PATH = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant" / "zinc_kish_invariant.jsonl"
OUT_SUMMARY = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant" / "C5_chem_scalar_summary.json"
OUT_FIG = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant" / "C5_chem_scalar_histogram.png"

MODULUS = 16.0 / math.pi

# π-harmonics to overlay
HARMONICS = {
    "pi/30": math.pi / 30.0,
    "pi/24": math.pi / 24.0,
    "pi/18": math.pi / 18.0,
    "pi/12": math.pi / 12.0,
    "pi/9":  math.pi / 9.0,
    "pi/6":  math.pi / 6.0,
    "pi/3":  math.pi / 3.0,
}

def load_scalars(path: Path):
    scalars = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            s = obj.get("scalar_invariant", None)
            if s is not None:
                scalars.append(float(s))
    return np.array(scalars, dtype=float)

def main():
    print("=== C5.1 Chemistry Scalar Histogram ===")
    print(f"Loading invariants from: {LAKE_PATH}")

    scalars = load_scalars(LAKE_PATH)
    n = scalars.size
    if n == 0:
        print("No scalars found. Exiting.")
        return

    mean_scalar = float(np.mean(scalars))
    std_scalar = float(np.std(scalars))
    min_scalar = float(np.min(scalars))
    max_scalar = float(np.max(scalars))

    band_width = max_scalar - min_scalar
    band_fraction = band_width / MODULUS

    # distances to harmonics
    harmonic_distances = {
        name: abs(mean_scalar - val) for name, val in HARMONICS.items()
    }

    summary = {
        "count": n,
        "mean_scalar": mean_scalar,
        "std_scalar": std_scalar,
        "min_scalar": min_scalar,
        "max_scalar": max_scalar,
        "modulus": MODULUS,
        "band_width": band_width,
        "band_fraction_of_modulus": band_fraction,
        "harmonic_distances": harmonic_distances,
    }

    print("Writing summary JSON:")
    print(json.dumps(summary, indent=2))
    with OUT_SUMMARY.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Histogram
    plt.figure(figsize=(8, 5))
    bins = 120  # fine-grained
    plt.hist(scalars, bins=bins, density=True, alpha=0.7, color="steelblue", edgecolor="none")

    # Harmonic overlays
    ymin, ymax = plt.ylim()
    for name, val in HARMONICS.items():
        if min_scalar <= val <= max_scalar:
            plt.axvline(val, color="red", linestyle="--", linewidth=1.0, alpha=0.8)
            plt.text(val, ymax * 0.9, name, rotation=90, va="top", ha="center", fontsize=7, color="red")

    plt.title("C5.1 Chemistry Scalar Distribution (Kish 16/π Modulus)")
    plt.xlabel("Scalar invariant")
    plt.ylabel("Density")

    plt.tight_layout()
    plt.savefig(OUT_FIG, dpi=300)
    plt.close()

    print(f"Histogram saved to: {OUT_FIG}")
    print(f"Summary saved to:   {OUT_SUMMARY}")
    print("=== C5.1 COMPLETE ===")

if __name__ == "__main__":
    main()
