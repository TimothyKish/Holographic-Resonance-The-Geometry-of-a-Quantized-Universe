import json
import math
from pathlib import Path
import numpy as np

BASE_DIR = Path(__file__).resolve().parent

SRC_JSON = BASE_DIR / "Kish_Lattice_Empirical_Lake.json"

OUT_DIR = BASE_DIR / "lakes" / "materials_kish_invariant"
OUT_LAKE = OUT_DIR / "materials_kish_invariant.jsonl"
OUT_SUMMARY = OUT_DIR / "materials_kish_invariant_summary.json"

MODULUS = 16.0 / math.pi

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
    print("=== C6.1b Materials Scalar Normalization ===")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with SRC_JSON.open("r", encoding="utf-8") as f:
        data = json.load(f)

    scalars = []

    with OUT_LAKE.open("w", encoding="utf-8") as out_f:
        for entry in data:
            ld = entry.get("lattice_deviation", None)
            if ld is None:
                continue

            s = float(ld)  # here we treat lattice_deviation as the Kish scalar
            scalars.append(s)

            obj = {
                "material_id": entry.get("material_id"),
                "formula": entry.get("formula"),
                "scalar_invariant": s,
                "lattice_deviation": ld,
                "volume": entry.get("volume"),
                "nsites": entry.get("nsites"),
                "node_ratio": entry.get("node_ratio"),
            }
            out_f.write(json.dumps(obj) + "\n")

    scalars = np.array(scalars, dtype=float)
    summary = {
        "modulus": MODULUS,
        "scalar_stats": stats(scalars),
    }

    with OUT_SUMMARY.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))
    print(f"Saved lake: {OUT_LAKE}")
    print(f"Saved summary: {OUT_SUMMARY}")
    print("=== C6.1b COMPLETE ===")

if __name__ == "__main__":
    main()
