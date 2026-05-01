"""
scalarize.py -- L1_GWTC
Scalar: log(f_ring_hz + 1) / log(k_geo)
"""
import json, os, math

PI = math.pi; K_GEO = 16/PI; LOG_K = math.log(K_GEO)

PROMOTED_PATH   = os.path.join(os.path.dirname(__file__), "..", "..", "..", "lakes",
                                "inputs_promoted", "l1_gwtc_promoted.jsonl")
SCALARIZED_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "lakes",
                                "unified", "l1_gwtc_scalarized.jsonl")
os.makedirs(os.path.dirname(SCALARIZED_PATH), exist_ok=True)

def scalarize():
    records = []
    with open(PROMOTED_PATH, encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line.strip()))
    out = []
    for r in records:
        freq = float(r["f_ring_hz"])
        scalar = math.log(freq + 1.0) / LOG_K
        n_approx = scalar * PI
        s = dict(r)
        s["kish_scalar"] = round(scalar, 8)
        s["k_geo"] = round(K_GEO, 10)
        s["n_approx"] = round(n_approx, 4)
        s["nearest_n"] = round(n_approx)
        out.append(s)
    with open(SCALARIZED_PATH, "w", encoding="utf-8") as f:
        for s in out:
            f.write(json.dumps(s) + "\n")
    print(f"[L1_GWTC] scalarize complete — {len(out)} records")
    print(f"  Prediction P19 targets: 16/pi=N~16 (scalar=5.093) or 21/pi=N~21 (scalar=6.685)")
    print(f"  f_ring range maps to N range:")
    print(f"    50 Hz  -> N~{math.log(51)/LOG_K*PI:.2f}")
    print(f"    107 Hz -> N~{math.log(108)/LOG_K*PI:.2f}  <-- 21/pi target")
    print(f"    250 Hz -> N~{math.log(251)/LOG_K*PI:.2f}")
    print(f"    650 Hz -> N~{math.log(651)/LOG_K*PI:.2f}")
    print(f"  Output: {SCALARIZED_PATH}")

if __name__ == "__main__":
    scalarize()