# ==============================================================================
# SCRIPT: scalarize.py
# SERIES: S-Series / S3_GalacticNASA
# LAKE:   s3_gaia_luminosity
# STEP:   3 of 4  (build_lake → promote → scalarize → validate)
#
# PURPOSE
# -------
# Compute scalar_kls and scalar_klc for every promoted record.
# Update the promoted JSONL in-place.
#
# This script contains THE FORMULA. The formula is the hypothesis.
# If the formula is later found to be wrong, this is where you fix it.
# The raw data is preserved in _raw_payload — no re-download needed.
#
# FORMULA
# -------
# Step 1: Compute absolute G magnitude
#   distance_pc = 1000 / parallax_mas
#   M_G = phot_g_mean_mag - (5 * log10(distance_pc) - 5)
#
# Step 2: Compute scalar
#   scalar = log(1 + abs(M_G - M_G_median)) / log(k_geo)
#
# Physical motivation:
#   M_G ranges from ~-8 (luminous supergiants) to +16 (faint red dwarfs).
#   The distribution clusters at the main sequence (M_G ≈ 4-6 for solar-type).
#   Using offset from the median preserves the natural clustering structure.
#   The chaos null cannot reproduce this clustering → signal detectable.
#
# LITMUS CRITERION
#   stdev/span < 0.20 → PASS (strong clustering)
#   0.20 - 0.28 → BORDERLINE (acceptable, proceed with note)
#   > 0.28 → FAIL (formula likely producing uniform distribution)
#
# KNOWN RESULT ON 2M STAR SAMPLE
#   M_G median: 5.595
#   scalar range: [0.000, 1.630]
#   stdev/span: 0.201 → BORDERLINE/PASS
#   Physical interpretation: main sequence clustering at median,
#   giants and dwarfs spread above and below.
#
# INPUT:  lake/s3_gaia_luminosity_promoted.jsonl
# OUTPUT: lake/s3_gaia_luminosity_promoted.jsonl (updated in-place)
# ==============================================================================

import json
import math
import statistics
import tempfile
import shutil
from pathlib import Path

PI    = math.pi
K_GEO = 16.0 / PI   # 5.092958178940651

SCRIPT_DIR   = Path(__file__).resolve().parent
LAKE_DIR     = SCRIPT_DIR.parent / "lake"
PROMOTED_IN  = LAKE_DIR / "s3_gaia_luminosity_promoted.jsonl"

MEDIAN_SAMPLE = 50_000   # records to sample for M_G median


# ==============================================================================
# THE FORMULA
# ==============================================================================

def absolute_magnitude(g_apparent: float, parallax_mas: float) -> float | None:
    """
    Convert apparent Gaia G magnitude + parallax to absolute magnitude M_G.
    Returns None if parallax is invalid.
    """
    if parallax_mas <= 0:
        return None
    distance_pc = 1000.0 / parallax_mas
    dist_modulus = 5.0 * math.log10(distance_pc) - 5.0
    return g_apparent - dist_modulus


def luminosity_scalar(M_G: float, M_G_median: float) -> float:
    """
    scalar = log(1 + abs(M_G - M_G_median)) / log(k_geo)
    """
    return math.log(1.0 + abs(M_G - M_G_median)) / math.log(K_GEO)


# ==============================================================================
# COMPUTE MEDIAN FROM PROMOTED FILE
# ==============================================================================

def compute_median(path: Path) -> float:
    magnitudes = []
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= MEDIAN_SAMPLE:
                break
            try:
                rec = json.loads(line.strip())
                raw = rec["meta"]["source_row"]["_raw_payload"]
                g   = raw.get("phot_g_mean_mag")
                plx = raw.get("parallax")
                if g and plx:
                    M_G = absolute_magnitude(float(g), float(plx))
                    if M_G is not None and -10 < M_G < 20:
                        magnitudes.append(M_G)
            except (json.JSONDecodeError, KeyError, ValueError):
                continue

    if not magnitudes:
        raise ValueError("No valid records to compute M_G median")

    median = statistics.median(magnitudes)
    print(f"  M_G median (from {len(magnitudes):,} records): {median:.4f}")
    return median


# ==============================================================================
# SCALARIZE IN-PLACE
# ==============================================================================

def scalarize():
    if not PROMOTED_IN.exists():
        print(f"Promoted file not found: {PROMOTED_IN}")
        print("Run promote.py first.")
        return

    print(f"Scalarizing: {PROMOTED_IN}")
    print()
    print("Computing M_G median...")
    M_G_median = compute_median(PROMOTED_IN)
    print()

    # Write to temp file, then replace
    tmp = LAKE_DIR / "_scalarize_tmp.jsonl"
    n_written = n_skipped = 0
    scalars = []

    with open(PROMOTED_IN, encoding="utf-8") as fin, \
         open(tmp, "w", encoding="utf-8") as fout:

        for line in fin:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                n_skipped += 1
                continue

            try:
                raw = rec["meta"]["source_row"]["_raw_payload"]
                g   = float(raw["phot_g_mean_mag"])
                plx = float(raw["parallax"])

                M_G = absolute_magnitude(g, plx)
                if M_G is None or not (-10 < M_G < 20):
                    n_skipped += 1
                    continue

                scalar = luminosity_scalar(M_G, M_G_median)
                rec["scalar_kls"] = scalar
                rec["scalar_klc"] = scalar
                # Also update the source_row scalars
                rec["meta"]["source_row"]["scalar_kls"] = scalar
                rec["meta"]["source_row"]["scalar_klc"] = scalar
                # Document the formula used
                rec["meta"]["scalarization_formula"] = (
                    f"M_G = g_app - 5*log10(1000/parallax_mas) + 5; "
                    f"scalar = log(1 + abs(M_G - {M_G_median:.4f})) / log(k_geo)"
                )
                rec["meta"]["M_G_median"] = M_G_median

                fout.write(json.dumps(rec) + "\n")
                scalars.append(scalar)
                n_written += 1

            except (KeyError, ValueError, TypeError):
                n_skipped += 1
                continue

    # Replace original
    shutil.move(str(tmp), str(PROMOTED_IN))

    print(f"Written: {n_written:,}  Skipped: {n_skipped:,}")
    print()

    # Litmus
    if scalars:
        mean_s  = statistics.mean(scalars)
        stdev_s = statistics.stdev(scalars)
        lo, hi  = min(scalars), max(scalars)
        span    = hi - lo
        ratio   = stdev_s / span if span > 0 else 1.0

        print("Litmus test:")
        print(f"  mean={mean_s:.4f}  stdev={stdev_s:.4f}")
        print(f"  range=[{lo:.4f}, {hi:.4f}]  stdev/span={ratio:.3f}")

        if ratio < 0.20:
            print("  PASS ✓")
        elif ratio < 0.28:
            print("  BORDERLINE — acceptable, proceed. Note in documentation.")
        else:
            print("  FAIL — inspect distribution. Review formula.")
    print()
    print("Next step: python validate.py")


if __name__ == "__main__":
    scalarize()