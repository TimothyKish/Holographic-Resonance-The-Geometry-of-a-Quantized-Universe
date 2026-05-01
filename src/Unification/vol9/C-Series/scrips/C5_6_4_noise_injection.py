import json
import math
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
LAKE_PATH = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant" / "zinc_kish_invariant.jsonl"

OUT_JSON = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant" / "C5_6_4_noise_injection_summary.json"
OUT_FIG = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant" / "C5_6_4_noise_injection.png"

MODULUS = 16.0 / math.pi
NOISE_LEVELS = [0.01, 0.02, 0.03]  # 1%, 2%, 3%

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
    print("=== C5.6.4 Noise Injection ===")

    scalars = load_scalars(LAKE_PATH)
    summary = {"full": stats(scalars), "noise_levels": {}}

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    bins = 120

    for i, nl in enumerate(NOISE_LEVELS):
        noise = np.random.normal(loc=0.0, scale=nl, size=scalars.size)
        perturbed = scalars * (1.0 + noise)

        summary["noise_levels"][f"{int(nl*100)}pct"] = stats(perturbed)

        ax = axes[i]
        ax.hist(perturbed, bins=bins, density=True, alpha=0.7, color="steelblue")
        ax.set_title(f"{int(nl*100)}% noise")
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
    print("=== C5.6.4 COMPLETE ===")

if __name__ == "__main__":
    main()
