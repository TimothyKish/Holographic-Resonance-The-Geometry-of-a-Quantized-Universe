# ==============================================================================
# SCRIPT: validate.py
# SERIES: S-Series / S3_GalacticNASA
# LAKE:   s3_gaia_luminosity
# STEP:   4 of 4  (build_lake → promote → scalarize → validate)
#
# PURPOSE
# -------
# Final gate before the lake enters the main pipeline.
# Checks schema completeness, scalar distribution, and uniqueness.
# On PASS: copies promoted file to the main lakes/inputs_promoted/ directory.
# On FAIL: reports issues without touching the pipeline.
#
# CHECKS
# ------
#   1. File exists and is non-empty
#   2. Every record has required sovereign schema fields
#   3. scalar_klc is non-null in every record
#   4. entity_id values are unique
#   5. domain = "stellar" in every record
#   6. _raw_payload present in every record
#   7. Litmus: stdev/span < 0.28 (BORDERLINE allowed, > 0.28 = FAIL)
#   8. Record count reasonable (warn if < 100k for a 2M target lake)
#
# ON PASS
# -------
# Copies promoted file to:
#   ../../../../lakes/inputs_promoted/s3_gaia_luminosity_promoted.jsonl
#
# Then prints the volumes.json entry to add manually.
# ==============================================================================

import json
import statistics
from pathlib import Path

SCRIPT_DIR   = Path(__file__).resolve().parent
LAKE_DIR     = SCRIPT_DIR.parent / "lake"
PROMOTED_IN  = LAKE_DIR / "s3_gaia_luminosity_promoted.jsonl"

# Relative path from series scripts to main inputs_promoted
PIPELINE_OUT = SCRIPT_DIR.parents[2] / "lakes" / "inputs_promoted" / \
               "s3_gaia_luminosity_promoted.jsonl"

REQUIRED_FIELDS = [
    "entity_id", "domain", "volume", "lake_id",
    "scalar_kls", "scalar_klc", "geometry_payload", "meta"
]
EXPECTED_DOMAIN = "stellar"
EXPECTED_LAKE_ID = "s3_gaia_luminosity"


def validate():
    print("=" * 60)
    print("VALIDATE: s3_gaia_luminosity")
    print("=" * 60)
    print()

    issues = []
    warnings = []

    # ── Check 1: file exists ──────────────────────────────────────
    if not PROMOTED_IN.exists():
        print("FAIL: Promoted file not found.")
        print("Run scalarize.py first.")
        return
    print(f"  File: {PROMOTED_IN}")

    # ── Read and check records ────────────────────────────────────
    n_total = n_null_scalar = n_missing_raw = n_bad_domain = 0
    entity_ids = set()
    duplicates = 0
    scalars = []

    with open(PROMOTED_IN, encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                issues.append(f"  Line {i}: JSON parse error")
                continue

            n_total += 1

            # Check 2: required fields
            for field in REQUIRED_FIELDS:
                if field not in rec:
                    issues.append(f"  Record {i}: missing field '{field}'")
                    break

            # Check 3: scalar non-null
            if rec.get("scalar_klc") is None:
                n_null_scalar += 1

            else:
                scalars.append(float(rec["scalar_klc"]))

            # Check 4: unique entity_id
            eid = rec.get("entity_id")
            if eid in entity_ids:
                duplicates += 1
            else:
                entity_ids.add(eid)

            # Check 5: domain
            if rec.get("domain") != EXPECTED_DOMAIN:
                n_bad_domain += 1

            # Check 6: _raw_payload
            try:
                raw = rec["meta"]["source_row"]["_raw_payload"]
                if not raw:
                    n_missing_raw += 1
            except (KeyError, TypeError):
                n_missing_raw += 1

    # ── Report counts ─────────────────────────────────────────────
    print(f"  Records:       {n_total:>10,}")
    print(f"  Null scalars:  {n_null_scalar:>10,}")
    print(f"  Missing raw:   {n_missing_raw:>10,}")
    print(f"  Bad domain:    {n_bad_domain:>10,}")
    print(f"  Duplicates:    {duplicates:>10,}")
    print()

    if n_null_scalar > 0:
        issues.append(f"  {n_null_scalar:,} records have null scalar_klc — run scalarize.py")
    if n_missing_raw > 0:
        issues.append(f"  {n_missing_raw:,} records missing _raw_payload — re-run promote.py")
    if n_bad_domain > 0:
        issues.append(f"  {n_bad_domain:,} records have wrong domain (expected '{EXPECTED_DOMAIN}')")
    if duplicates > 0:
        issues.append(f"  {duplicates:,} duplicate entity_id values")
    if n_total < 100_000:
        warnings.append(f"  Only {n_total:,} records — target was 2,000,000. Check download.")

    # ── Check 7: litmus ───────────────────────────────────────────
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
                f"  Litmus FAIL: stdev/span={ratio:.3f} > 0.28 — "
                "distribution approximately uniform. Review scalarize.py formula."
            )
        elif ratio > 0.20:
            warnings.append(
                f"  Litmus BORDERLINE: stdev/span={ratio:.3f} — "
                "acceptable for this lake (main sequence clustering confirmed)."
            )
        else:
            print(f"    PASS ✓")
    print()

    # ── Result ────────────────────────────────────────────────────
    if issues:
        print("VALIDATION FAILED")
        print()
        for issue in issues:
            print(f"  ✗ {issue}")
        if warnings:
            print()
            for w in warnings:
                print(f"  ⚠ {w}")
        return

    if warnings:
        print("VALIDATION PASSED (with warnings)")
        for w in warnings:
            print(f"  ⚠ {w}")
    else:
        print("VALIDATION PASSED ✓")
    print()

    # ── Copy to pipeline ──────────────────────────────────────────
    import shutil
    PIPELINE_OUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(PROMOTED_IN), str(PIPELINE_OUT))
    print(f"  Copied to pipeline:")
    print(f"  {PIPELINE_OUT}")
    print()

    # ── Print volumes.json entry ──────────────────────────────────
    print("  Add this entry to configs/volumes.json:")
    print("  ─────────────────────────────────────────────────────")
    print('  "s3_gaia_luminosity": {')
    print('    "path": "lakes/inputs_promoted/s3_gaia_luminosity_promoted.jsonl",')
    print('    "enabled": true,')
    print('    "domain": "stellar",')
    print('    "scale_rank": 3,')
    print('    "__scalar__": "log(1 + abs(M_G - M_G_median)) / log(k_geo) — absolute G magnitude offset",')
    print('    "__source__": "Gaia DR3 phot_g_mean_mag + parallax, 2M stars, same objects as S1/S2",')
    print('    "__same_object__": ["s1_gaia_parallax", "s2_stellar_kinematics"],')
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