"""validate.py -- t2g_indian"""
import json, os, math, sys

PI = math.pi; K_GEO = 16/PI

SCALARIZED_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "lakes",
                                "unified", "t2g_indian_scalarized.jsonl")

def validate():
    if not os.path.exists(SCALARIZED_PATH):
        print("[T2g_Indian] VALIDATE FAILED: file not found"); sys.exit(1)
    records = []
    with open(SCALARIZED_PATH, encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line.strip()))
    errors = []
    for i, r in enumerate(records):
        if "kish_scalar" not in r: errors.append(f"row {i+1}: missing kish_scalar")
        if r.get("domain") != "planetary_indian": errors.append(f"row {i+1}: domain mismatch")
    if errors:
        print("[T2g_Indian] VALIDATE FAILED:")
        [print(f"  {e}") for e in errors[:5]]; sys.exit(1)
    scalars = [r["kish_scalar"] for r in records]
    target_19 = 19/PI  # T2g confirmed at 19/pi
    near_19 = sum(1 for r in records if abs(r["n_approx"] - 19) < 0.5)
    print(f"[T2g_Indian] VALIDATE PASSED")
    print(f"  Records:      {len(records)}")
    print(f"  Scalar range: {min(scalars):.4f} - {max(scalars):.4f}")
    print(f"  P18 target 19/pi = {target_19:.4f} (N=19)")
    print(f"  Near N=19: {near_19} records ({near_19/len(records)*100:.1f}%)")
    print(f"  [READY FOR PIPELINE] domain: planetary_indian")

if __name__ == "__main__":
    validate()