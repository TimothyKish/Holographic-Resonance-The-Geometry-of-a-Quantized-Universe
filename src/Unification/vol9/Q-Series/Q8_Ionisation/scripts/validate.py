"""validate.py -- Q8_Ionisation"""
import json, os, math, sys
from collections import Counter

PI = math.pi; K_GEO = 16/PI

SCALARIZED_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "lakes",
                                "unified", "q8_ionisation_scalarized.jsonl")

def validate():
    if not os.path.exists(SCALARIZED_PATH):
        print("[Q8_Ionisation] VALIDATE FAILED: file not found"); sys.exit(1)
    records = []
    with open(SCALARIZED_PATH, encoding="utf-8") as f:
        for line in f: records.append(json.loads(line.strip()))
    errors = []
    for i, r in enumerate(records):
        if "kish_scalar" not in r: errors.append(f"row {i+1}: missing kish_scalar")
        if r.get("domain") != "atomic_ionisation": errors.append(f"row {i+1}: domain mismatch")
    if errors:
        print("[Q8_Ionisation] VALIDATE FAILED:"); [print(f"  {e}") for e in errors]; sys.exit(1)
    scalars = [r["kish_scalar"] for r in records]
    nearest_counts = Counter(r["nearest_n"] for r in records)
    print(f"[Q8_Ionisation] VALIDATE PASSED")
    print(f"  Records:      {len(records)} / 118 elements")
    print(f"  Scalar range: {min(scalars):.4f} - {max(scalars):.4f}")
    print(f"  N distribution (top 5): {nearest_counts.most_common(5)}")
    # Noble gas check — should be highest IE values
    noble = [r for r in records if r["symbol"] in ["He","Ne","Ar","Kr","Xe","Rn"]]
    print(f"  Noble gases (highest IE expected):")
    for r in sorted(noble, key=lambda x: -x["ionisation_energy_eV"]):
        print(f"    {r['symbol']:>3}  IE={r['ionisation_energy_eV']:>6.3f} eV  "
              f"scalar={r['kish_scalar']:.4f}  N~{r['n_approx']:.2f}")
    print(f"  [READY FOR PIPELINE] domain: atomic_ionisation")

if __name__ == "__main__":
    validate()