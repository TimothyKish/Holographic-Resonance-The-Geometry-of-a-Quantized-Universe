import json
import math
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
LAKE_PATH = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant" / "zinc_kish_invariant.jsonl"
OUT_JSON = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant" / "C5_2_harmonic_shelves.json"
OUT_FIG = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant" / "C5_2_harmonic_shelves.png"

MODULUS = 16.0 / math.pi

HARMONICS = {
    "pi/30": math.pi / 30.0,
    "pi/24": math.pi / 24.0,
    "pi/18": math.pi / 18.0,
    "pi/12": math.pi / 12.0,
    "pi/9":  math.pi / 9.0,
    "pi/6":  math.pi / 6.0,
    "pi/3":  math.pi / 3.0,
}

WINDOWS = [0.005, 0.01, 0.02]

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
    print("=== C5.2 Chemistry Harmonic Shelf Analysis ===")

    scalars = load_scalars(LAKE_PATH)
    n = scalars.size
    mean_scalar = float(np.mean(scalars))

    harmonic_distances = {
        name: abs(mean_scalar - val) for name, val in HARMONICS.items()
    }

    harmonic_affinity = {}
    for name, val in HARMONICS.items():
        affinity = {}
        for w in WINDOWS:
            mask = np.abs(scalars - val) <= w
            affinity[f"within_{w}"] = float(np.sum(mask)) / n
        harmonic_affinity[name] = affinity

    summary = {
        "count": n,
        "mean_scalar": mean_scalar,
        "harmonic_distances": harmonic_distances,
        "harmonic_affinity": harmonic_affinity,
        "modulus": MODULUS,
    }

    with OUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))

    plt.figure(figsize=(8, 5))
    bins = 120
    plt.hist(scalars, bins=bins, density=True, alpha=0.6, color="steelblue")

    ymin, ymax = plt.ylim()
    for name, val in HARMONICS.items():
        plt.axvline(val, color="red", linestyle="--", linewidth=1.0)
        plt.text(val, ymax * 0.9, name, rotation=90, ha="center", va="top", fontsize=7, color="red")

    plt.title("C5.2 Chemistry Harmonic Shelf Alignment")
    plt.xlabel("Scalar invariant")
    plt.ylabel("Density")
    plt.tight_layout()
    plt.savefig(OUT_FIG, dpi=300)
    plt.close()

    print(f"Saved: {OUT_JSON}")
    print(f"Saved: {OUT_FIG}")
    print("=== C5.2 COMPLETE ===")

if __name__ == "__main__":
    main()
