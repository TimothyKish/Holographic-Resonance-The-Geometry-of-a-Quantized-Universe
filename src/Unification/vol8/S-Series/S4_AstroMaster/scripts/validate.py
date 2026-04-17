# ==============================================================================
# SCRIPT: validate.py
# SERIES: S-Series / S4_AstroMaster
# LAKE:   s4_gaia_colour
# STEP:   4 of 4  (build_lake → promote → scalarize → validate)
#
# On PASS: copies promoted file to lakes/inputs_promoted/
#          and prints the volumes.json entry to add.
# ==============================================================================

import json
import statistics
import shutil
from pathlib import Path

SCRIPT_DIR   = Path(__file__).resolve().parent
LAKE_DIR     = SCRIPT_DIR.parent / "lake"
PROMOTED_IN  = LAKE_DIR / "s4_gaia_colour_promoted.jsonl"
PIPELINE_OUT = SCRIPT_DIR.parents[3] / "lakes" / "inputs_promoted" / \
               "s4_gaia_colour_promoted.jsonl"

EXPECTED_DOMAIN  = "stellar"
EXPECTED_LAKE_ID = "s4_gaia_colour"
REQUIRED_FIELDS  = [
    "entity_id", "domain", "volume", "lake_id",
    "scalar_kls", "scalar_klc", "geometry_payload", "meta"
]


def validate():
    print("=" * 60)
    print("VALIDATE: s4_gaia_colour")
    print("=" * 60)
    print()

    issues = []
    warnings = []

    if not PROMOTED_IN.exists():
        print("FAIL: Promoted file not found. Run scalarize.py first.")
        return

    print(f"  File: {PROMOTED_IN}")

    n_total = n_null = n_missing_raw = n_bad_domain = duplicates = 0
    entity_ids = set()
    scalars = []

    with open(PROMOTED_IN, encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                issues.append(f"Line {i}: JSON parse error")
                continue

            n_total += 1

            if rec.get("scalar_klc") is None:
                n_null += 1
            else:
                scalars.append(float(rec["scalar_klc"]))

            eid = rec.get("entity_id")
            if eid in entity_ids:
                duplicates += 1
            else:
                entity_ids.add(eid)

            if rec.get("domain") != EXPECTED_DOMAIN:
                n_bad_domain += 1

            try:
                raw = rec["meta"]["source_row"]["_raw_payload"]
                if not raw:
                    n_missing_raw += 1
            except (KeyError, TypeError):
                n_missing_raw += 1

    print(f"  Records:       {n_total:>10,}")
    print(f"  Null scalars:  {n_null:>10,}")
    print(f"  Missing raw:   {n_missing_raw:>10,}")
    print(f"  Bad domain:    {n_bad_domain:>10,}")
    print(f"  Duplicates:    {duplicates:>10,}")
    print()

    if n_null > 0:
        issues.append(f"{n_null:,} null scalar_klc — run scalarize.py")
    if n_missing_raw > 0:
        issues.append(f"{n_missing_raw:,} missing _raw_payload — re-run promote.py")
    if n_bad_domain > 0:
        issues.append(f"{n_bad_domain:,} wrong domain (expected '{EXPECTED_DOMAIN}')")
    if duplicates > 0:
        issues.append(f"{duplicates:,} duplicate entity_id values")
    if n_total < 100_000:
        warnings.append(f"Only {n_total:,} records — target was 2,000,000")

    if scalars:
        mean_s  = statistics.mean(scalars)
        stdev_s = statistics.stdev(scalars)
        lo, hi  = min(scalars), max(scalars)
        span    = hi - lo
        ratio   = stdev_s / span if span > 0 else 1.0

        print(f"  Litmus (stdev/span):")
        print(f"    mean={mean_s:.4f}  stdev={stdev_s:.4f}")
        print(f"    range=[{lo:.4f}, {hi:.4f}]  stdev/span={ratio:.3f}")

        if ratio > 0.28:
            issues.append(
                f"Litmus FAIL: stdev/span={ratio:.3f} > 0.28 — "
                "review scalarize.py formula."
            )
        elif ratio > 0.20:
            warnings.append(
                f"Litmus BORDERLINE: stdev/span={ratio:.3f} — "
                "acceptable, main sequence colour clustering confirmed."
            )
        else:
            print("    PASS ✓")
    print()

    if issues:
        print("VALIDATION FAILED")
        for issue in issues:
            print(f"  ✗ {issue}")
        return

    if warnings:
        print("VALIDATION PASSED (with warnings)")
        for w in warnings:
            print(f"  ⚠ {w}")
    else:
        print("VALIDATION PASSED ✓")
    print()

    PIPELINE_OUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(PROMOTED_IN), str(PIPELINE_OUT))
    print(f"  Copied to pipeline:")
    print(f"  {PIPELINE_OUT}")
    print()
    print("  Add this entry to configs/volumes.json:")
    print("  ─────────────────────────────────────────────────────")
    print('  "s4_gaia_colour": {')
    print('    "path": "lakes/inputs_promoted/s4_gaia_colour_promoted.jsonl",')
    print('    "enabled": true,')
    print('    "domain": "stellar",')
    print('    "scale_rank": 3,')
    print('    "__scalar__": "log(1 + max(bp_rp, 0.01)) / log(k_geo) — Gaia colour index",')
    print('    "__source__": "Gaia DR3 bp_rp, 2M stars, same objects as S1/S2/S3",')
    print('    "__same_object__": ["s1_gaia_parallax", "s2_stellar_kinematics", "s3_gaia_luminosity"],')
    print('    "__audit__": "mondy_verified_vol8"')
    print('  }')
    print()
    print("  After updating volumes.json, run from vol8/scripts/:")
    print("    python scalarize.py")
    print("    python unify.py")
    print("    python build_chaos_nulls.py    ← overnight")
    print("    python build_pinch_table.py    ← overnight")


if __name__ == "__main__":
    validate()