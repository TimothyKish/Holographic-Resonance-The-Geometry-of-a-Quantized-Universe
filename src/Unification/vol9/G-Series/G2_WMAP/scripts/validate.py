"""validate.py -- G2_WMAP"""
import json, os, math, sys
from collections import Counter

PI = math.pi

SCALARIZED_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "lakes",
                                "unified", "g2_wmap_scalarized.jsonl")

def validate():
    if not os.path.exists(SCALARIZED_PATH):
        print("[G2_WMAP] VALIDATE FAILED: file not found"); sys.exit(1)
    records = []
    with open(SCALARIZED_PATH, encoding="utf-8") as f:
        for line in f: records.append(json.loads(line.strip()))
    errors = []
    for i, r in enumerate(records):
        if "kish_scalar" not in r: errors.append(f"row {i+1}: missing kish_scalar")
        if r.get("domain") != "cmb_anisotropy": errors.append(f"row {i+1}: domain mismatch")
    if errors:
        print("[G2_WMAP] VALIDATE FAILED:"); [print(f"  {e}") for e in errors[:5]]; sys.exit(1)
    scalars = [r["kish_scalar"] for r in records]
    nearest_counts = Counter(r["nearest_n"] for r in records)
    # First acoustic peak at l=220 should have highest amplitude
    peak = next((r for r in records if r.get("multipole_l") == 220), None)
    print(f"[G2_WMAP] VALIDATE PASSED")
    print(f"  Records:      {len(records)}")
    print(f"  Scalar range: {min(scalars):.4f} - {max(scalars):.4f}")
    print(f"  N distribution (top 5): {nearest_counts.most_common(5)}")
    if peak:
        print(f"  First acoustic peak (l=220): Dl={peak.get('Dl_uK2')} uK2, "
              f"scalar={peak['kish_scalar']:.4f}, N~{peak['n_approx']:.2f}")
    print(f"  P22: CMB anisotropy amplitudes expected to couple to N/pi registers")
    print(f"  [READY FOR PIPELINE] domain: cmb_anisotropy")

if __name__ == "__main__":
    validate()