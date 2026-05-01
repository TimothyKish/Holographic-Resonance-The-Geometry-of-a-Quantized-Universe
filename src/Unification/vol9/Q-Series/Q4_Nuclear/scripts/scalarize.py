"""scalarize.py -- Q4_Nuclear"""
import json, os, math

PI = math.pi; K_GEO = 16/PI; LOG_K = math.log(K_GEO)

PROMOTED_PATH   = os.path.join(os.path.dirname(__file__), "..", "..", "..", "lakes",
                                "inputs_promoted", "q4_nuclear_promoted.jsonl")
SCALARIZED_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "lakes",
                                "unified", "q4_nuclear_scalarized.jsonl")
os.makedirs(os.path.dirname(SCALARIZED_PATH), exist_ok=True)

def scalarize():
    records = []
    with open(PROMOTED_PATH, encoding="utf-8") as f:
        for line in f: records.append(json.loads(line.strip()))
    out = []
    for r in records:
        be = float(r["binding_energy_mev_per_A"])
        scalar = math.log(be + 1.0) / LOG_K
        s = dict(r)
        s["kish_scalar"] = round(scalar, 8)
        s["k_geo"] = round(K_GEO, 10)
        s["n_approx"] = round(scalar * PI, 4)
        s["nearest_n"] = round(scalar * PI)
        out.append(s)
    with open(SCALARIZED_PATH, "w", encoding="utf-8") as f:
        for s in out: f.write(json.dumps(s) + "\n")
    scalars = [r["kish_scalar"] for r in out]
    print(f"[Q4_Nuclear] scalarize complete — {len(out)} records")
    print(f"  Scalar range: {min(scalars):.4f} - {max(scalars):.4f}")
    print(f"  12/pi = {12/PI:.4f} — prediction: nuclear scalars cluster BELOW this")
    print(f"  Output: {SCALARIZED_PATH}")

if __name__ == "__main__":
    scalarize()