import json
import math
from pathlib import Path
import numpy as np

BASE_DIR = Path(__file__).resolve().parent

# Chemistry scalar lake
CHEM_PATH = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant" / "zinc_kish_invariant.jsonl"

# Materials scalar lake (normalized in C6.1b)
MATS_PATH = BASE_DIR / ".." / ".." / "Lattice_Audit_Materials" / "lakes" / "materials_kish_invariant" / "materials_kish_invariant.jsonl"

OUT_JSON = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant" / "C6_2_cross_domain_comparison.json"

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

def load_jsonl_scalars(path):
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

def harmonic_distances(mean_val):
    return {name: float(abs(mean_val - val)) for name, val in HARMONICS.items()}

def main():
    print("=== C6.2 Cross-Domain Comparison ===")

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    chem = load_jsonl_scalars(CHEM_PATH)
    mats = load_jsonl_scalars(MATS_PATH)

    chem_stats = stats(chem)
    mats_stats = stats(mats)

    comparison = {
        "modulus": MODULUS,
        "chemistry": chem_stats,
        "materials": mats_stats,
        "mean_difference": float(chem_stats["mean"] - mats_stats["mean"]),
        "std_difference": float(chem_stats["std"] - mats_stats["std"]),
        "band_fraction_difference": float(chem_stats["band_fraction"] - mats_stats["band_fraction"]),
        "harmonic_distances": {
            "chemistry": harmonic_distances(chem_stats["mean"]),
            "materials": harmonic_distances(mats_stats["mean"]),
        }
    }

    with OUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(comparison, f, indent=2)

    print(json.dumps(comparison, indent=2))
    print(f"Saved: {OUT_JSON}")
    print("=== C6.2 COMPLETE ===")

if __name__ == "__main__":
    main()
