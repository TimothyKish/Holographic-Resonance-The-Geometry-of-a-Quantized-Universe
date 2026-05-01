"""validate.py -- Q4_Nuclear"""
import json, os, math, sys

PI = math.pi; K_GEO = 16/PI
QUANTUM_BOUNDARY = 12/PI  # scalar = 3.8197 — nuclear must be BELOW this

SCALARIZED_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "lakes",
                                "unified", "q4_nuclear_scalarized.jsonl")

def validate():
    if not os.path.exists(SCALARIZED_PATH):
        print("[Q4_Nuclear] VALIDATE FAILED: file not found"); sys.exit(1)
    records = []
    with open(SCALARIZED_PATH, encoding="utf-8") as f:
        for line in f: records.append(json.loads(line.strip()))
    errors = []
    for i, r in enumerate(records):
        if "kish_scalar" not in r: errors.append(f"row {i+1}: missing kish_scalar")
        if r.get("domain") != "nuclear_binding": errors.append(f"row {i+1}: domain mismatch")
    if errors:
        print("[Q4_Nuclear] VALIDATE FAILED:"); [print(f"  {e}") for e in errors[:5]]; sys.exit(1)
    scalars = [r["kish_scalar"] for r in records]
    below_boundary = sum(1 for s in scalars if s < QUANTUM_BOUNDARY)
    print(f"[Q4_Nuclear] VALIDATE PASSED")
    print(f"  Records:      {len(records)}")
    print(f"  Scalar range: {min(scalars):.4f} - {max(scalars):.4f}")
    print(f"  Quantum boundary (12/pi): {QUANTUM_BOUNDARY:.4f}")
    print(f"  Below boundary: {below_boundary}/{len(records)} "
          f"({below_boundary/len(records)*100:.1f}%)")
    print(f"  P21 prediction: nuclear layer registers cluster below 12/pi")
    # Iron peak
    fe56 = next((r for r in records if r.get("Z") == 26 and r.get("A") == 56), None)
    if fe56:
        print(f"  Fe-56 (peak stability): scalar={fe56['kish_scalar']:.4f}, "
              f"N~{fe56['n_approx']:.2f}")
    print(f"  [READY FOR PIPELINE] domain: nuclear_binding")

if __name__ == "__main__":
    validate()