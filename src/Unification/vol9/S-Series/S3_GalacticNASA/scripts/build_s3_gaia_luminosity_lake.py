# ==============================================================================
# SCRIPT: build_s3_gaia_luminosity_lake.py
# SERIES: S-Series / S3_GalacticNASA
# LAKE:   s3_gaia_luminosity
# DOMAIN: stellar
#
# PURPOSE
# -------
# Build a sovereign lake of Gaia DR3 absolute G-band luminosity (magnitude)
# for the same 1.81 million stars already in S1 (parallax) and S2 (kinematics).
#
# SAME-OBJECT SCIENCE
# -------------------
# S1 measures WHERE the star is      → stellar domain → 24/π (z=22)
# S2 measures HOW FAST the star moves → stellar_kinematic → 16/π (z=103)
# S3 measures HOW BRIGHT the star is  → stellar domain → register UNKNOWN
#
# If S3 lands on a different register from both S1 and S2, that is the
# same-object harmonic map: three measurements of the same object, three
# different registers of the same N/π family.
# "The register you hear depends on the question you ask."
#
# SCALARIZATION
# -------------
# Absolute G magnitude requires apparent magnitude + parallax:
#   M_G = G_app + 5 * log10(parallax_arcsec / 1000) + 5
#   (parallax in mas → divide by 1000 to get arcsec)
#
# Then map to scalar:
#   scalar = log(1 + abs(M_G - M_G_median)) / log(k_geo)
#
# Physical motivation:
#   M_G ranges from about -8 (supergiants) to +16 (brown dwarfs).
#   The distribution is NOT uniform — it clusters near the main sequence
#   (M_G ≈ 4-6 for sun-like stars, M_G ≈ 9-14 for M dwarfs).
#   Using the median-offset ensures natural clustering is preserved
#   and the scalar is NOT uniformly distributed.
#
# LITMUS CHECK before full build:
#   stdev/span should be < 0.25 on first 1000 records
#   If > 0.28: the luminosity distribution may be unexpectedly uniform
#              in your specific Gaia query — try log(1 + 10^(-0.4*M_G)) instead
#
# DATA SOURCE
# -----------
# Gaia DR3 via ADQL TAP query — same query as S2, add one column:
#   phot_g_mean_mag   (apparent G magnitude)
# parallax is already present from the S1/S2 query.
#
# GAIA TAP ENDPOINT
# -----------------
# https://gea.esac.esa.int/tap-server/tap/sync
#
# ADQL QUERY (add to your existing Gaia query):
#   SELECT source_id, ra, dec, parallax, parallax_error,
#          pmra, pmdec, phot_g_mean_mag, ruwe
#   FROM gaiadr3.gaia_source
#   WHERE parallax > 0
#     AND parallax_over_error > 10
#     AND ruwe < 1.4
#     AND phot_g_mean_mag IS NOT NULL
#   LIMIT 2000000
#
# AUTHORS: Timothy John Kish & Mondy
# AUDIT STATUS: vol8_template_v1
# ==============================================================================

import json
import math
import statistics
import uuid
from datetime import datetime, timezone
from pathlib import Path

PI    = math.pi
K_GEO = 16.0 / PI   # 5.092958178940651

SCRIPT_DIR  = Path(__file__).resolve().parent
SERIES_ROOT = SCRIPT_DIR.parent
RAW_INPUT   = SERIES_ROOT / "lake" / "s3_gaia_luminosity_raw.jsonl"
RAW_PROMOTED = SERIES_ROOT / "lake" / "s3_gaia_luminosity_promoted.jsonl"
PIPELINE_OUT = Path(__file__).resolve().parents[4] / \
               "lakes" / "inputs_promoted" / "s3_gaia_luminosity_promoted.jsonl"


# ==============================================================================
# SCALARIZATION FORMULA
# ==============================================================================

def absolute_magnitude(g_apparent: float, parallax_mas: float) -> float | None:
    """
    Convert apparent Gaia G magnitude + parallax to absolute magnitude M_G.
    parallax_mas: parallax in milliarcseconds (as stored in Gaia DR3)
    Returns None if parallax is invalid.
    """
    if parallax_mas <= 0:
        return None
    distance_pc = 1000.0 / parallax_mas          # parsecs
    dist_modulus = 5.0 * math.log10(distance_pc) - 5.0
    return g_apparent - dist_modulus


def luminosity_scalar(M_G: float, M_G_median: float) -> float:
    """
    Map absolute magnitude to scalar_klc.
    Uses offset from median to capture the luminosity DISTRIBUTION shape,
    not the absolute value (which would need careful normalisation).

    scalar = log(1 + abs(M_G - M_G_median)) / log(k_geo)

    Range: 0 (at median) → ~1.5 (for stars 5 mag from median)
    Clustering: peaks at solar-like stars (M_G ≈ 4-6)
    """
    offset = abs(M_G - M_G_median)
    return math.log(1.0 + offset) / math.log(K_GEO)


# ==============================================================================
# BUILD FUNCTIONS
# ==============================================================================

def compute_median_absolute_magnitude(raw_path: Path,
                                       sample: int = 50000) -> float:
    """
    Compute M_G median from the first `sample` valid records.
    Used to anchor the scalarization.
    """
    magnitudes = []
    with raw_path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= sample:
                break
            try:
                rec = json.loads(line.strip())
                g_app = rec.get("phot_g_mean_mag")
                plx   = rec.get("parallax")
                if g_app is not None and plx is not None:
                    M_G = absolute_magnitude(float(g_app), float(plx))
                    if M_G is not None and -10 < M_G < 20:
                        magnitudes.append(M_G)
            except (json.JSONDecodeError, ValueError, KeyError):
                continue
    if not magnitudes:
        raise ValueError("No valid records to compute median M_G")
    median = statistics.median(magnitudes)
    print(f"  M_G median computed from {len(magnitudes):,} records: {median:.3f}")
    return median


def build_lake(raw_path: Path, output_path: Path,
               M_G_median: float, limit: int | None = None):
    """
    Build the promoted sovereign lake from raw Gaia records.
    """
    now_ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    n_written = n_skipped = 0
    scalars = []

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with raw_path.open("r", encoding="utf-8") as fin, \
         output_path.open("w", encoding="utf-8") as fout:

        for i, line in enumerate(fin):
            if limit and i >= limit:
                break
            line = line.strip()
            if not line:
                continue
            try:
                raw = json.loads(line)
            except json.JSONDecodeError:
                n_skipped += 1
                continue

            g_app = raw.get("phot_g_mean_mag")
            plx   = raw.get("parallax")
            sid   = raw.get("source_id", f"GAIA_S3_{i:08d}")

            if g_app is None or plx is None:
                n_skipped += 1
                continue

            M_G = absolute_magnitude(float(g_app), float(plx))
            if M_G is None or not (-10 < M_G < 20):
                n_skipped += 1
                continue

            scalar = luminosity_scalar(M_G, M_G_median)
            scalars.append(scalar)

            record = {
                "entity_id":    str(uuid.uuid5(uuid.NAMESPACE_DNS,
                                   f"s3_gaia_{sid}")),
                "domain":       "stellar",
                "volume":       8,
                "lake_id":      "s3_gaia_luminosity",
                "scalar_kls":   scalar,
                "scalar_klc":   scalar,
                "geometry_payload": {
                    "coordinates":  [],
                    "dimensionality": 0,
                    "geometry_type": "luminosity"
                },
                "meta": {
                    "source": "Gaia DR3 phot_g_mean_mag + parallax",
                    "ingest_timestamp": now_ts,
                    "sovereign": True,
                    "scalarization": (
                        "M_G = g_app - 5*log10(1000/plx) + 5; "
                        f"scalar = log(1 + abs(M_G - {M_G_median:.4f})) / log(k_geo)"
                    ),
                    "same_object_lakes": ["s1_gaia_parallax", "s2_stellar_kinematics"],
                    "source_row": {
                        "_raw_payload": raw
                    }
                }
            }
            fout.write(json.dumps(record) + "\n")
            n_written += 1

    return n_written, n_skipped, scalars


# ==============================================================================
# LITMUS TEST
# ==============================================================================

def litmus_test(scalars: list[float]) -> bool:
    """
    Verify the scalar distribution is non-uniform (clustered).
    Broken formula criterion: stdev/span > 0.28
    Passing criterion:        stdev/span < 0.20
    """
    if len(scalars) < 50:
        print(f"  WARNING: Only {len(scalars)} scalars — too few for reliable litmus")
        return True

    mean_s  = statistics.mean(scalars)
    stdev_s = statistics.stdev(scalars)
    lo, hi  = min(scalars), max(scalars)
    span    = hi - lo
    ratio   = stdev_s / span if span > 0 else 1.0

    print(f"  Litmus: n={len(scalars):,}  mean={mean_s:.4f}  stdev={stdev_s:.4f}")
    print(f"  range=[{lo:.4f}, {hi:.4f}]  stdev/span={ratio:.3f}")

    if ratio > 0.28:
        print("  FAIL — distribution approximately uniform. Check scalarization.")
        print("         Try: scalar = log(1 + 10^(-0.4 * M_G)) / log(k_geo)")
        return False
    elif ratio < 0.20:
        print("  PASS — clustering detected. Proceed to pipeline.")
        return True
    else:
        print("  BORDERLINE — proceed with caution. Inspect distribution manually.")
        return True


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    import sys
    litmus_only = "--litmus" in sys.argv

    print("=" * 65)
    print("S3 Gaia Luminosity Lake Builder")
    print("=" * 65)
    print()
    print(f"k_geo = {K_GEO:.10f}")
    print(f"Domain: stellar (same as S1, S2)")
    print(f"Same-object strategy: velocity at 16/π, distance at 24/π,")
    print(f"luminosity at ? — this lake provides the third measurement.")
    print()

    if not RAW_INPUT.exists():
        print(f"Raw input not found: {RAW_INPUT}")
        print()
        print("Download instructions:")
        print("  Gaia DR3 TAP endpoint:")
        print("  https://gea.esac.esa.int/tap-server/tap/sync")
        print()
        print("  ADQL query (save result as s3_gaia_luminosity_raw.jsonl):")
        print("  SELECT source_id, ra, dec, parallax, parallax_error,")
        print("         pmra, pmdec, phot_g_mean_mag, ruwe")
        print("  FROM gaiadr3.gaia_source")
        print("  WHERE parallax > 0")
        print("    AND parallax_over_error > 10")
        print("    AND ruwe < 1.4")
        print("    AND phot_g_mean_mag IS NOT NULL")
        print("  LIMIT 2000000")
        print()
        print("  Alternatively: add phot_g_mean_mag to your existing S2 query")
        print("  and convert output to JSONL.")
        return

    limit = 1000 if litmus_only else None
    tag = "LITMUS (1000 records)" if litmus_only else "FULL BUILD"
    out = RAW_PROMOTED if not litmus_only else \
          RAW_PROMOTED.parent / "s3_gaia_luminosity_litmus.jsonl"

    print(f"Mode: {tag}")
    print(f"Input:  {RAW_INPUT}")
    print(f"Output: {out}")
    print()

    print("Computing M_G median from sample...")
    M_G_median = compute_median_absolute_magnitude(RAW_INPUT)
    print()

    print("Building lake...")
    n_written, n_skipped, scalars = build_lake(RAW_INPUT, out, M_G_median, limit)
    print(f"Written: {n_written:,}  Skipped: {n_skipped:,}")
    print()

    print("Litmus test:")
    passed = litmus_test(scalars)
    print()

    if passed and not litmus_only:
        # Copy to pipeline inputs
        import shutil
        PIPELINE_OUT.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(out, PIPELINE_OUT)
        print(f"Copied to pipeline: {PIPELINE_OUT}")
        print()
        print("Next steps:")
        print("  1. Add 's3_gaia_luminosity' entry to configs/volumes.json")
        print("  2. python scripts/scalarize.py")
        print("  3. python scripts/unify.py")
        print("  4. python scripts/build_chaos_nulls.py")
        print("  5. python scripts/build_pinch_table.py")
        print()
        print("  Watch for z-score at a register DIFFERENT from 16/π (S2)")
        print("  and 24/π (S1). That is the same-object harmonic map.")


if __name__ == "__main__":
    main()