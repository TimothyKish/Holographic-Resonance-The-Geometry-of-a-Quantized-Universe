"""
validate.py -- Q9_C60
Final validation of the scalarized lake.
Checks structural integrity, scalar range, and reports
proximity of modes to the predicted quantum register (12/pi).

Reads: ../../lakes/unified/q9_c60_scalarized.jsonl
"""

import json, os, math, sys

PI    = math.pi
K_GEO = 16.0 / PI
QUANTUM_REGISTER = 12.0 / PI   # scalar = 3.8197, predicted register for P17

SCALARIZED_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "lakes", "unified",
    "q9_c60_scalarized.jsonl"
)

REQUIRED_FIELDS = [
    "id", "molecule", "irrep", "mode_index", "frequency_cm1",
    "activity", "domain", "kish_scalar", "nearest_n"
]


def validate():
    if not os.path.exists(SCALARIZED_PATH):
        print(f"[Q9_C60] VALIDATE FAILED: {SCALARIZED_PATH} not found")
        sys.exit(1)

    records = []
    with open(SCALARIZED_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))

    errors = []

    # Structural checks
    for i, r in enumerate(records):
        for field in REQUIRED_FIELDS:
            if field not in r:
                errors.append(f"  row {i+1}: missing field '{field}'")
        if r.get("domain") != "molecular_c60":
            errors.append(f"  row {i+1}: domain mismatch")
        scalar = r.get("kish_scalar", 0)
        if not (1.0 < scalar < 7.0):
            errors.append(f"  row {i+1}: scalar {scalar} out of expected range")

    # Count records
    if len(records) != 46:
        errors.append(f"  Expected 46 records, found {len(records)}")

    if errors:
        print("[Q9_C60] VALIDATE FAILED:")
        for e in errors:
            print(e)
        sys.exit(1)

    # Register proximity report
    near_12 = [r for r in records if abs(r["n_approx"] - 12.0) < 0.5]
    near_13 = [r for r in records if abs(r["n_approx"] - 13.0) < 0.5]
    near_11 = [r for r in records if abs(r["n_approx"] - 11.0) < 0.5]

    print(f"[Q9_C60] VALIDATE PASSED")
    print(f"  Total records:        {len(records)}")
    print(f"  Quantum register prediction (P17): 12/pi = {QUANTUM_REGISTER:.4f}")
    print()
    print(f"  Modes near N=12 (quantum register): {len(near_12)}")
    for r in sorted(near_12, key=lambda x: abs(x["n_approx"] - 12)):
        print(f"    {r['irrep']}({r['mode_index']:<2}) "
              f"{r['frequency_cm1']:>5} cm-1  "
              f"scalar={r['kish_scalar']:.4f}  "
              f"N~{r['n_approx']:.3f}  "
              f"dev={r['scalar_deviation']:.4f}  "
              f"{r['description'][:40]}")
    print()
    print(f"  Modes near N=11:  {len(near_11)}")
    print(f"  Modes near N=13:  {len(near_13)}")
    print()

    # Key prediction check
    breathing_mode = next(
        (r for r in records if r["irrep"] == "Ag" and r["mode_index"] == 1), None
    )
    if breathing_mode:
        dev_from_12 = abs(breathing_mode["n_approx"] - 12.0)
        print(f"  KEY MODE — Ag(1) Breathing Mode (P17 primary candidate):")
        print(f"    frequency_cm1 = {breathing_mode['frequency_cm1']}")
        print(f"    kish_scalar   = {breathing_mode['kish_scalar']:.6f}")
        print(f"    N_approx      = {breathing_mode['n_approx']:.4f}")
        print(f"    Deviation from N=12: {dev_from_12:.4f} ({dev_from_12*100:.2f}% of unit)")
        print(f"    Quantum register (12/pi): {QUANTUM_REGISTER:.6f}")
        print(f"    Scalar deviation: {abs(breathing_mode['kish_scalar'] - QUANTUM_REGISTER):.6f}")
    print()
    print(f"  [READY FOR PIPELINE] Copy q9_c60_promoted.jsonl to")
    print(f"  vol9/lakes/inputs_promoted/ and add entry to volumes.json")
    print(f"  domain: molecular_c60")


if __name__ == "__main__":
    validate()