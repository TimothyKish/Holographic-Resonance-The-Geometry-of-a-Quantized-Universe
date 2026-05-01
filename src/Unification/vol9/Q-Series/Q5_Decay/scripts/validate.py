"""validate.py -- Q5_Decay"""
import json, os, math, sys

PI = math.pi; K_GEO = 16/PI
BEAT_8_PI = 8/PI  # sub-lattice beat candidate

SCALARIZED_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "lakes",
                                "unified", "q5_decay_scalarized.jsonl")

def validate():
    if not os.path.exists(SCALARIZED_PATH):
        print("[Q5_Decay] VALIDATE FAILED: file not found"); sys.exit(1)
    records = []
    with open(SCALARIZED_PATH, encoding="utf-8") as f:
        for line in f: records.append(json.loads(line.strip()))
    errors = []
    for i, r in enumerate(records):
        if "kish_scalar" not in r: errors.append(f"row {i+1}: missing kish_scalar")
        if r.get("domain") != "nuclear_decay": errors.append(f"row {i+1}: domain mismatch")
    if errors:
        print("[Q5_Decay] VALIDATE FAILED:"); [print(f"  {e}") for e in errors[:5]]; sys.exit(1)
    scalars = [r["kish_scalar"] for r in records]
    unstable = [r for r in records if not r.get("stable", False)]
    print(f"[Q5_Decay] VALIDATE PASSED")
    print(f"  Records: {len(records)} ({len(unstable)} unstable, "
          f"{len(records)-len(unstable)} stable/treated)")
    print(f"  Scalar range: {min(scalars):.4f} - {max(scalars):.4f}")
    print(f"  P27 sub-test: looking for clustering near 8/pi={BEAT_8_PI:.4f} nodes")
    near_beat = sum(1 for r in records if abs(r.get("n_approx",0) % 1) < 0.15)
    print(f"  Records within 0.15 of any integer N: {near_beat} ({near_beat/len(records)*100:.1f}%)")
    print(f"  [READY FOR PIPELINE] domain: nuclear_decay")

if __name__ == "__main__":
    validate()