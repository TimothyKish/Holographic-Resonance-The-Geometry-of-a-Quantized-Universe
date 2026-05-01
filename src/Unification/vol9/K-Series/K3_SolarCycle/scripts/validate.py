"""validate.py -- K3_SolarCycle"""
import json, os, math, sys

PI = math.pi; K_GEO = 16/PI

SCALARIZED_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "lakes",
                                "unified", "k3_solar_cycle_scalarized.jsonl")

def validate():
    if not os.path.exists(SCALARIZED_PATH):
        print("[K3_SolarCycle] VALIDATE FAILED: file not found"); sys.exit(1)
    records = []
    with open(SCALARIZED_PATH, encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line.strip()))

    intervals = [r for r in records if r.get("measurement_type") == "cycle_interval"]
    annual    = [r for r in records if r.get("measurement_type") == "annual_mean"]

    if not records:
        print("[K3_SolarCycle] VALIDATE FAILED: no records"); sys.exit(1)

    errors = []
    for i, r in enumerate(records):
        if "kish_scalar" not in r: errors.append(f"row {i+1}: missing kish_scalar")
        if r.get("domain") != "stellar_cycle": errors.append(f"row {i+1}: domain mismatch")
    if errors:
        print("[K3_SolarCycle] VALIDATE FAILED:")
        [print(f"  {e}") for e in errors[:5]]; sys.exit(1)

    print(f"[K3_SolarCycle] VALIDATE PASSED")
    print(f"  Total records:   {len(records)}")
    print(f"  Annual means:    {len(annual)}")
    print(f"  Cycle intervals: {len(intervals)}")
    if intervals:
        iv_scalars = [r["kish_scalar"] for r in intervals]
        iv_n       = [r["n_approx"] for r in intervals]
        print(f"  Interval scalar range: {min(iv_scalars):.4f} - {max(iv_scalars):.4f}")
        print(f"  Interval N range:      {min(iv_n):.2f} - {max(iv_n):.2f}")
        # Report the most common N
        from collections import Counter
        nearest_counts = Counter(r["nearest_n"] for r in intervals)
        print(f"  Most common nearest_n: {nearest_counts.most_common(5)}")
    print(f"  [READY FOR PIPELINE] domain: stellar_cycle")

if __name__ == "__main__":
    validate()