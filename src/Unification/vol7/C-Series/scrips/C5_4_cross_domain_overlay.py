import json
import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent

# Adjust these two paths to match your materials lake
CHEM_PATH = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant" / "zinc_kish_invariant.jsonl"
MATS_PATH = BASE_DIR / ".." / "lakes" / "materials_kish_invariant" / "materials_kish_invariant.jsonl"

OUT_JSON = BASE_DIR / ".." / "lakes" / "cross_domain" / "C5_4_cross_domain_summary.json"
OUT_FIG = BASE_DIR / ".." / "lakes" / "cross_domain" / "C5_4_cross_domain_overlay.png"

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

def load_scalars(path: Path):
    vals = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            s = obj.get("scalar_invariant", None)
            if s is not None:
                vals.append(float(s))
    return np.array(vals, dtype=float)

def stats(arr: np.ndarray):
    return {
        "count": int(arr.size),
        "mean": float(np.mean(arr)),
        "std": float(np.std(arr)),
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
    }

def main():
    print("=== C5.4 Cross-domain Scalar Overlay ===")

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    chem = load_scalars(CHEM_PATH)
    mats = load_scalars(MATS_PATH)

    chem_stats = stats(chem)
    mats_stats = stats(mats)

    summary = {
        "modulus": MODULUS,
        "chemistry": chem_stats,
        "materials": mats_stats,
    }

    with OUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))

    # Overlay histograms
    plt.figure(figsize=(8, 5))
    bins = 120

    plt.hist(chem, bins=bins, density=True, alpha=0.6, color="steelblue", label="Chemistry")
    plt.hist(mats, bins=bins, density=True, alpha=0.4, color="orange", label="Materials")

    ymin, ymax = plt.ylim()
    for name, val in HARMONICS.items():
        plt.axvline(val, color="red", linestyle="--", linewidth=1.0, alpha=0.7)

    plt.title("C5.4 Cross-domain Scalar Distribution (Chemistry vs Materials)")
    plt.xlabel("Scalar invariant")
    plt.ylabel("Density")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT_FIG, dpi=300)
    plt.close()

    print(f"Saved: {OUT_JSON}")
    print(f"Saved: {OUT_FIG}")
    print("=== C5.4 COMPLETE ===")

if __name__ == "__main__":
    main()
