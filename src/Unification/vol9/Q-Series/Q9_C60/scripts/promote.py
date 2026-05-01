"""
promote.py -- Q9_C60
Validates q9_c60_raw.jsonl and promotes to
../../lakes/inputs_promoted/q9_c60_promoted.jsonl

Validation rules:
  - frequency_cm1 must be positive float
  - irrep must be known Ih C60 symmetry label
  - mode_index must be positive integer
  - domain must be molecular_c60
  - No duplicate ids
"""

import json, os, sys

RAW_PATH     = os.path.join(os.path.dirname(__file__), "..", "lake", "q9_c60_raw.jsonl")
PROMOTED_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "lakes", "inputs_promoted",
    "q9_c60_promoted.jsonl"
)
os.makedirs(os.path.dirname(PROMOTED_PATH), exist_ok=True)

VALID_IRREPS = {"Ag", "T1g", "T2g", "Gg", "Hg", "Au", "T1u", "T2u", "Gu", "Hu"}


def validate_record(r, idx):
    errors = []
    if not isinstance(r.get("frequency_cm1"), (int, float)) or r["frequency_cm1"] <= 0:
        errors.append(f"  row {idx}: frequency_cm1 invalid ({r.get('frequency_cm1')})")
    if r.get("irrep") not in VALID_IRREPS:
        errors.append(f"  row {idx}: unknown irrep ({r.get('irrep')})")
    if not isinstance(r.get("mode_index"), int) or r["mode_index"] < 1:
        errors.append(f"  row {idx}: mode_index invalid")
    if r.get("domain") != "molecular_c60":
        errors.append(f"  row {idx}: wrong domain ({r.get('domain')})")
    return errors


def promote():
    records = []
    with open(RAW_PATH, encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            records.append((i + 1, json.loads(line)))

    all_errors = []
    seen_ids = set()
    for idx, r in records:
        all_errors.extend(validate_record(r, idx))
        rid = r.get("id")
        if rid in seen_ids:
            all_errors.append(f"  row {idx}: duplicate id {rid}")
        seen_ids.add(rid)

    if all_errors:
        print("[Q9_C60] PROMOTE FAILED — validation errors:")
        for e in all_errors:
            print(e)
        sys.exit(1)

    promoted = []
    for _, r in records:
        p = dict(r)
        p["promoted"] = True
        p["lake_version"] = "vol9"
        promoted.append(p)

    with open(PROMOTED_PATH, "w", encoding="utf-8") as f:
        for p in promoted:
            f.write(json.dumps(p) + "\n")

    print(f"[Q9_C60] promote complete")
    print(f"  Validated:  {len(promoted)} records — 0 errors")
    print(f"  Output:     {PROMOTED_PATH}")


if __name__ == "__main__":
    promote()