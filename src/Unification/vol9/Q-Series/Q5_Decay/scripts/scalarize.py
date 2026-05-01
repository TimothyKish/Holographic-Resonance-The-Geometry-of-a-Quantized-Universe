"""
scalarize.py -- Q5_Decay
Double-log scalar for half-lives spanning 30+ orders of magnitude:
    kish_scalar = log(log(half_life_seconds + 1) + 1) / log(k_geo)
"""
import json, os, math

PI = math.pi; K_GEO = 16/PI; LOG_K = math.log(K_GEO)

PROMOTED_PATH   = os.path.join(os.path.dirname(__file__), "..", "..", "..", "lakes",
                                "inputs_promoted", "q5_decay_promoted.jsonl")
SCALARIZED_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "lakes",
                                "unified", "q5_decay_scalarized.jsonl")
os.makedirs(os.path.dirname(SCALARIZED_PATH), exist_ok=True)

def scalarize():
    records = []
    with open(PROMOTED_PATH, encoding="utf-8") as f:
        for line in f: records.append(json.loads(line.strip()))
    out = []
    for r in records:
        hl = float(r["half_life_seconds"])
        # Double log: compress 30 orders of magnitude into useful scalar range
        inner = math.log(hl + 1.0)
        scalar = math.log(inner + 1.0) / LOG_K
        s = dict(r)
        s["kish_scalar"]    = round(scalar, 8)
        s["scalar_method"]  = "log(log(hl_s+1)+1)/log(k_geo)"
        s["k_geo"]          = round(K_GEO, 10)
        s["n_approx"]       = round(scalar * PI, 4)
        s["nearest_n"]      = round(scalar * PI)
        out.append(s)
    with open(SCALARIZED_PATH, "w", encoding="utf-8") as f:
        for s in out: f.write(json.dumps(s) + "\n")
    scalars = [r["kish_scalar"] for r in out]
    print(f"[Q5_Decay] scalarize complete — {len(out)} records")
    print(f"  Scalar range: {min(scalars):.4f} - {max(scalars):.4f}")
    # Show what some key half-lives map to
    examples = [
        ("1 second",     1.0),
        ("1 day",        86400.0),
        ("1 year",       3.156e7),
        ("C-14 5730yr",  1.81e11),
        ("U-238 4.5Gyr", 1.41e17),
        ("Stable",       1e25),
    ]
    print(f"  Key mappings:")
    for label, hl_s in examples:
        sc = math.log(math.log(hl_s+1)+1) / LOG_K
        print(f"    {label:<20} hl={hl_s:.2e}s  scalar={sc:.4f}  N~{sc*PI:.2f}")
    print(f"  Output: {SCALARIZED_PATH}")

if __name__ == "__main__":
    scalarize()