# patch_b3_histidine.py
# Zero out Histidine records (angle > 115 deg) in b3_amino_promoted.jsonl
# Run from: vol5/scripts/
# The Ca identification picked an imidazole carbon instead of the true alpha carbon.
# True Histidine backbone angle is ~106-107 deg. These records are flagged and zeroed
# so unify.py excludes them via the all-zeros filter.

import json
import math
from pathlib import Path

# Script lives at vol5/scripts/ so parent is vol5 root
ROOT     = Path(__file__).resolve().parent.parent
PROMOTED = ROOT / "lakes" / "inputs_promoted" / "b3_amino_promoted.jsonl"

print(f"Looking for: {PROMOTED}")

if not PROMOTED.exists():
    raise SystemExit(f"Not found: {PROMOTED}")

records      = []
his_count    = 0
normal_count = 0

with PROMOTED.open("r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        rec       = json.loads(line)
        angle_deg = math.degrees(rec.get("scalar_kls", 0))

        if angle_deg > 115.0:
            rec["meta"]["histidine_flag"] = (
                "Ca misidentified due to imidazole ring. "
                "True backbone angle ~106-107 deg. Excluded from scalar."
            )
            rec["scalar_kls"] = 0.0
            rec["scalar_klc"] = 0.0
            his_count += 1
        else:
            normal_count += 1

        records.append(rec)

with PROMOTED.open("w", encoding="utf-8") as f:
    for rec in records:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

print(f"Patched successfully:")
print(f"  Normal records kept:        {normal_count}")
print(f"  Histidine zeroed (flagged): {his_count}")
print(f"  Total:                      {normal_count + his_count}")

scalars = [rec["scalar_kls"] for rec in records if rec["scalar_kls"] > 0]
degs    = [math.degrees(s) for s in scalars]
print(f"  Active scalar range: {min(degs):.2f} to {max(degs):.2f} degrees")
print(f"  ({min(scalars):.4f} to {max(scalars):.4f} rad)")
print(f"  Mean: {sum(degs)/len(degs):.2f} degrees")
print()

seen = {}
for rec in records:
    aa = rec.get("meta", {}).get("amino_acid", "?")
    s  = rec["scalar_kls"]
    if aa not in seen and s > 0:
        seen[aa] = math.degrees(s)

print("Active amino acid angles:")
for aa, deg in sorted(seen.items(), key=lambda x: x[1]):
    print(f"  {aa:<15} {deg:.3f} deg  ({math.radians(deg):.4f} rad)")