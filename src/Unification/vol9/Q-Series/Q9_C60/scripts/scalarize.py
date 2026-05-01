"""
scalarize.py -- Q9_C60
Computes Kish Lattice scalar for each C60 vibrational mode.

Scalar formula (consistent with Q3 molecular vibration lake):
    kish_scalar = log(frequency_cm1 + 1) / log(k_geo)
    k_geo = 16 / pi

Reads:  ../../lakes/inputs_promoted/q9_c60_promoted.jsonl
Writes: ../../lakes/unified/q9_c60_scalarized.jsonl
"""

import json, os, math

PI    = math.pi
K_GEO = 16.0 / PI
LOG_K = math.log(K_GEO)

PROMOTED_PATH   = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "lakes", "inputs_promoted",
    "q9_c60_promoted.jsonl"
)
SCALARIZED_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "lakes", "unified",
    "q9_c60_scalarized.jsonl"
)
os.makedirs(os.path.dirname(SCALARIZED_PATH), exist_ok=True)


def scalarize():
    records = []
    with open(PROMOTED_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))

    scalarized = []
    for r in records:
        freq = float(r["frequency_cm1"])
        scalar = math.log(freq + 1.0) / LOG_K
        # Nearest N/pi register
        n_approx = scalar * PI
        nearest_n = round(n_approx)
        nearest_scalar = nearest_n / PI
        deviation = abs(scalar - nearest_scalar)

        s = dict(r)
        s["kish_scalar"]   = round(scalar, 8)
        s["k_geo"]         = round(K_GEO, 10)
        s["n_approx"]      = round(n_approx, 4)
        s["nearest_n"]     = nearest_n
        s["nearest_scalar"]= round(nearest_scalar, 8)
        s["scalar_deviation"] = round(deviation, 8)
        scalarized.append(s)

    with open(SCALARIZED_PATH, "w", encoding="utf-8") as f:
        for s in scalarized:
            f.write(json.dumps(s) + "\n")

    # Summary
    print(f"[Q9_C60] scalarize complete")
    print(f"  Records scalarized: {len(scalarized)}")
    print(f"  k_geo = 16/pi = {K_GEO:.8f}")
    print(f"  Scalar formula: log(freq_cm1 + 1) / log(k_geo)")
    print(f"  Output: {SCALARIZED_PATH}")
    print()
    print(f"  {'Mode':<10} {'freq':>6}  {'scalar':>8}  {'N~':>7}  {'dev':>8}  notes")
    print(f"  {'-'*60}")
    for s in scalarized:
        note = ""
        if abs(s["n_approx"] - 12) < 0.15:
            note = "<-- QUANTUM REG"
        elif abs(s["n_approx"] - 13) < 0.1:
            note = "<-- shelf 13"
        label = f"{s['irrep']}({s['mode_index']})"
        print(f"  {label:<10} {s['frequency_cm1']:>6}  "
              f"{s['kish_scalar']:>8.4f}  {s['n_approx']:>7.3f}  "
              f"{s['scalar_deviation']:>8.4f}  {note}")


if __name__ == "__main__":
    scalarize()