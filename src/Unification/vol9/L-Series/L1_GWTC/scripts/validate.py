"""
validate.py -- L1_GWTC
"""
import json, os, math, sys

PI = math.pi; K_GEO = 16/PI
TARGET_16 = 16/PI  # scalar = 5.0930
TARGET_21 = 21/PI  # scalar = 6.6845

SCALARIZED_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "lakes",
                                "unified", "l1_gwtc_scalarized.jsonl")

def validate():
    if not os.path.exists(SCALARIZED_PATH):
        print(f"[L1_GWTC] VALIDATE FAILED: file not found")
        sys.exit(1)
    records = []
    with open(SCALARIZED_PATH, encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line.strip()))

    errors = []
    for i, r in enumerate(records):
        if "kish_scalar" not in r: errors.append(f"row {i+1}: missing kish_scalar")
        if r.get("domain") != "gravitational_wave": errors.append(f"row {i+1}: domain mismatch")
    if errors:
        print("[L1_GWTC] VALIDATE FAILED:")
        for e in errors: print(f"  {e}")
        sys.exit(1)

    scalars = [r["kish_scalar"] for r in records]
    n_vals  = [r["n_approx"] for r in records]

    near_21 = [r for r in records if abs(r["n_approx"] - 21) < 1.0]
    near_16 = [r for r in records if abs(r["n_approx"] - 16) < 1.0]

    print(f"[L1_GWTC] VALIDATE PASSED")
    print(f"  Records:   {len(records)}")
    print(f"  N range:   {min(n_vals):.2f} - {max(n_vals):.2f}")
    print(f"  Scalar range: {min(scalars):.4f} - {max(scalars):.4f}")
    print()
    print(f"  P19 target check:")
    print(f"    Near 21/pi (N=21, f~107Hz, pre-registered): {len(near_21)} events")
    for r in sorted(near_21, key=lambda x: x["f_ring_hz"]):
        print(f"      {r['event_name']:<25} f={r['f_ring_hz']:>6.1f} Hz  N~{r['n_approx']:.2f}")
    print(f"    Near 16/pi (N=16, kinematic primary): {len(near_16)} events")
    for r in sorted(near_16, key=lambda x: x["f_ring_hz"]):
        print(f"      {r['event_name']:<25} f={r['f_ring_hz']:>6.1f} Hz  N~{r['n_approx']:.2f}")
    print()
    print(f"  [READY FOR PIPELINE] domain: gravitational_wave")

if __name__ == "__main__":
    validate()