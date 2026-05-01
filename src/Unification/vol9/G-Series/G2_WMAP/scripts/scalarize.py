"""scalarize.py -- G2_WMAP"""
import json, os, math

PI = math.pi; K_GEO = 16/PI; LOG_K = math.log(K_GEO)

PROMOTED_PATH   = os.path.join(os.path.dirname(__file__), "..", "..", "..", "lakes",
                                "inputs_promoted", "g2_wmap_promoted.jsonl")
SCALARIZED_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "lakes",
                                "unified", "g2_wmap_scalarized.jsonl")
os.makedirs(os.path.dirname(SCALARIZED_PATH), exist_ok=True)

def scalarize():
    records = []
    with open(PROMOTED_PATH, encoding="utf-8") as f:
        for line in f: records.append(json.loads(line.strip()))
    out = []
    for r in records:
        # Primary scalar: amplitude (sqrt(Dl) = delta_T in uK)
        dt = r.get("delta_T_uK")
        if dt is None and r.get("Dl_uK2", 0) > 0:
            dt = math.sqrt(r["Dl_uK2"])
        if dt is None or dt <= 0:
            dt = 0.01
        scalar = math.log(float(dt) + 1.0) / LOG_K
        s = dict(r)
        s["kish_scalar"] = round(scalar, 8)
        s["scalar_input"] = round(float(dt), 6)
        s["k_geo"] = round(K_GEO, 10)
        s["n_approx"] = round(scalar * PI, 4)
        s["nearest_n"] = round(scalar * PI)
        out.append(s)
    with open(SCALARIZED_PATH, "w", encoding="utf-8") as f:
        for s in out: f.write(json.dumps(s) + "\n")
    scalars = [r["kish_scalar"] for r in out]
    print(f"[G2_WMAP] scalarize complete — {len(out)} records")
    print(f"  Scalar range: {min(scalars):.4f} - {max(scalars):.4f}")
    print(f"  Output: {SCALARIZED_PATH}")

if __name__ == "__main__":
    scalarize()