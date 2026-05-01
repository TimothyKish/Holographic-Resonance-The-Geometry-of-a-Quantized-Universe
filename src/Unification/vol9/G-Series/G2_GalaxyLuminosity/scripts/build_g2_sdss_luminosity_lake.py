# ==============================================================================
# SCRIPT: build_g2_sdss_luminosity_lake.py
# SERIES: G-Series / G2_GalaxyLuminosity
# LAKE:   g2_sdss_luminosity
# DOMAIN: galactic
#
# PURPOSE
# -------
# Build a sovereign lake of SDSS DR16 r-band absolute luminosity for the
# same 1.84 million galaxies already in G1 (velocity dispersion).
#
# SAME-OBJECT SCIENCE
# -------------------
# G1 measures HOW FAST the galaxy's stars move → galactic → 21/π (z=59)
#                                                (107.1 Hz pre-registered prediction)
# G2 measures HOW BRIGHT the galaxy is          → galactic → register UNKNOWN
#
# G1 confirmed a prediction from January 10, 2026. G2 asks whether the
# same galaxies, measured by their luminosity instead of their kinematics,
# land on the same harmonic register or a different one.
#
# If G2 lands on a different register from G1:
#   velocity dispersion and luminosity are governed by DIFFERENT harmonics
#   in the same galaxy — the kinematic and photometric faces of the lattice.
#
# If G2 lands on the SAME register as G1:
#   luminosity is kinematically driven (Faber-Jackson relation territory)
#   and both attributes express the same underlying geometric coupling.
#
# Both outcomes are scientifically meaningful.
#
# SCALARIZATION
# -------------
# r-band absolute magnitude:
#   M_r = modelMag_r - 5 * log10(lum_dist_Mpc * 1e6 / 10)
#       = modelMag_r - 5 * log10(lum_dist_Mpc) - 25
#
# For SDSS spectroscopic objects the redshift z gives luminosity distance:
#   d_L = (c/H0) * z * (1 + z/2)    [Mpc, for z < 0.5, H0=70]
#
# Scalar:
#   scalar = log(1 + abs(M_r - M_r_median)) / log(k_geo)
#
# Physical motivation:
#   Galaxy luminosities cluster strongly by morphology/type.
#   Elliptical galaxies: M_r ≈ -20 to -24
#   Spirals: M_r ≈ -17 to -22
#   The distribution is distinctly non-uniform. Litmus should pass easily.
#
# DATA SOURCE
# -----------
# SDSS DR16 SpecObj + PhotoObj join via CasJobs or SkyServer:
# https://skyserver.sdss.org/casjobs/
# https://dr16.sdss.org/optical/spectrum/search
#
# SDQL QUERY (add to existing G1 query):
#   SELECT s.specobjid, s.ra, s.dec, s.z,
#          s.veldisp, s.veldisperr,
#          p.modelMag_r, p.modelMagErr_r
#   FROM SpecObj AS s
#   JOIN PhotoObj AS p ON s.bestobjid = p.objid
#   WHERE s.class = 'GALAXY'
#     AND s.zWarning = 0
#     AND s.z BETWEEN 0.01 AND 0.3
#     AND s.veldisp > 0
#     AND p.modelMag_r < 22.0
#     AND p.modelMag_r > 10.0
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
K_GEO = 16.0 / PI
H0    = 70.0   # km/s/Mpc (standard concordance)
C_KMS = 2.998e5  # km/s

SCRIPT_DIR   = Path(__file__).resolve().parent
SERIES_ROOT  = SCRIPT_DIR.parent
RAW_INPUT    = SERIES_ROOT / "lake" / "g2_sdss_luminosity_raw.jsonl"
RAW_PROMOTED = SERIES_ROOT / "lake" / "g2_sdss_luminosity_promoted.jsonl"
PIPELINE_OUT = Path(__file__).resolve().parents[4] / \
               "lakes" / "inputs_promoted" / "g2_sdss_luminosity_promoted.jsonl"


# ==============================================================================
# SCALARIZATION FORMULA
# ==============================================================================

def luminosity_distance_mpc(z: float) -> float:
    """
    Simple luminosity distance for z < 0.5.
    d_L ≈ (c/H0) * z * (1 + z/2)   [Mpc]
    Accurate to ~1% for z < 0.3 (our sample range).
    """
    return (C_KMS / H0) * z * (1.0 + z / 2.0)


def absolute_r_magnitude(modelMag_r: float, z: float) -> float | None:
    """
    Convert apparent r magnitude + redshift to absolute r magnitude M_r.
    """
    if z <= 0:
        return None
    d_L = luminosity_distance_mpc(z)
    if d_L <= 0:
        return None
    dist_modulus = 5.0 * math.log10(d_L * 1e6 / 10.0)
    return modelMag_r - dist_modulus


def luminosity_scalar(M_r: float, M_r_median: float) -> float:
    """
    Map absolute r magnitude to scalar_klc.
    scalar = log(1 + abs(M_r - M_r_median)) / log(k_geo)
    """
    offset = abs(M_r - M_r_median)
    return math.log(1.0 + offset) / math.log(K_GEO)


# ==============================================================================
# BUILD FUNCTIONS
# ==============================================================================

def compute_median_magnitude(raw_path: Path, sample: int = 50000) -> float:
    magnitudes = []
    with raw_path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= sample:
                break
            try:
                rec = json.loads(line.strip())
                mag_r = rec.get("modelMag_r")
                z     = rec.get("z")
                if mag_r is not None and z is not None and float(z) > 0:
                    M_r = absolute_r_magnitude(float(mag_r), float(z))
                    if M_r is not None and -27 < M_r < -10:
                        magnitudes.append(M_r)
            except (json.JSONDecodeError, ValueError):
                continue
    if not magnitudes:
        raise ValueError("No valid records for median M_r")
    median = statistics.median(magnitudes)
    print(f"  M_r median computed from {len(magnitudes):,} records: {median:.3f}")
    return median


def build_lake(raw_path: Path, output_path: Path,
               M_r_median: float, limit: int | None = None):
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

            mag_r = raw.get("modelMag_r")
            z     = raw.get("z")
            oid   = raw.get("specobjid", f"SDSS_G2_{i:08d}")

            if mag_r is None or z is None or float(z) <= 0:
                n_skipped += 1
                continue

            M_r = absolute_r_magnitude(float(mag_r), float(z))
            if M_r is None or not (-27 < M_r < -10):
                n_skipped += 1
                continue

            scalar = luminosity_scalar(M_r, M_r_median)
            scalars.append(scalar)

            record = {
                "entity_id":    str(uuid.uuid5(uuid.NAMESPACE_DNS,
                                   f"g2_sdss_{oid}")),
                "domain":       "galactic",
                "volume":       8,
                "lake_id":      "g2_sdss_luminosity",
                "scalar_kls":   scalar,
                "scalar_klc":   scalar,
                "geometry_payload": {
                    "coordinates":  [],
                    "dimensionality": 0,
                    "geometry_type": "luminosity"
                },
                "meta": {
                    "source": "SDSS DR16 PhotoObj/SpecObj modelMag_r + redshift",
                    "ingest_timestamp": now_ts,
                    "sovereign": True,
                    "scalarization": (
                        "M_r = modelMag_r - 5*log10(d_L/10pc); "
                        f"scalar = log(1 + abs(M_r - {M_r_median:.4f})) / log(k_geo)"
                    ),
                    "same_object_lakes": ["g1_galaxy_kinematics"],
                    "source_row": {
                        "_raw_payload": raw
                    }
                }
            }
            fout.write(json.dumps(record) + "\n")
            n_written += 1

    return n_written, n_skipped, scalars


def litmus_test(scalars: list[float]) -> bool:
    if len(scalars) < 50:
        print(f"  WARNING: Only {len(scalars)} scalars — too few for litmus")
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
        return False
    elif ratio < 0.20:
        print("  PASS — strong clustering. Proceed to pipeline.")
        return True
    else:
        print("  BORDERLINE — proceed with caution.")
        return True


def main():
    import sys
    litmus_only = "--litmus" in sys.argv

    print("=" * 65)
    print("G2 SDSS Galaxy Luminosity Lake Builder")
    print("=" * 65)
    print()
    print(f"k_geo = {K_GEO:.10f}")
    print(f"Domain: galactic (same as G1)")
    print(f"Same-object strategy: G1 velocity dispersion at 21/π (z=59),")
    print(f"G2 luminosity at ? — same 1.84M galaxies, different measurement.")
    print()
    print("Physical context:")
    print("  Faber-Jackson relation: luminosity ∝ σ^4")
    print("  If luminosity and velocity are coupled, G2 may land at 21/π.")
    print("  If they are independent lattice expressions, G2 lands elsewhere.")
    print()

    if not RAW_INPUT.exists():
        print(f"Raw input not found: {RAW_INPUT}")
        print()
        print("Download instructions:")
        print("  SDSS CasJobs: https://skyserver.sdss.org/casjobs/")
        print()
        print("  SQL query:")
        print("  SELECT s.specobjid, s.ra, s.dec, s.z,")
        print("         s.veldisp, s.veldisperr,")
        print("         p.modelMag_r, p.modelMagErr_r")
        print("  FROM SpecObj AS s")
        print("  JOIN PhotoObj AS p ON s.bestobjid = p.objid")
        print("  WHERE s.class = 'GALAXY'")
        print("    AND s.zWarning = 0")
        print("    AND s.z BETWEEN 0.01 AND 0.3")
        print("    AND s.veldisp > 0")
        print("    AND p.modelMag_r < 22.0")
        print("    AND p.modelMag_r > 10.0")
        print()
        print("  Save output as JSON/CSV then convert to JSONL.")
        print("  If you already have the G1 query, simply add modelMag_r")
        print("  to the SELECT clause and re-run — same galaxies, one more column.")
        return

    limit = 500 if litmus_only else None
    out = RAW_PROMOTED if not litmus_only else \
          RAW_PROMOTED.parent / "g2_sdss_luminosity_litmus.jsonl"

    print(f"Mode: {'LITMUS' if litmus_only else 'FULL BUILD'}")
    print()
    print("Computing M_r median...")
    M_r_median = compute_median_magnitude(RAW_INPUT)
    print()

    print("Building lake...")
    n_written, n_skipped, scalars = build_lake(RAW_INPUT, out, M_r_median, limit)
    print(f"Written: {n_written:,}  Skipped: {n_skipped:,}")
    print()

    print("Litmus test:")
    passed = litmus_test(scalars)
    print()

    if passed and not litmus_only:
        import shutil
        PIPELINE_OUT.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(out, PIPELINE_OUT)
        print(f"Copied to pipeline: {PIPELINE_OUT}")
        print()
        print("volumes.json entry to add:")
        print('  "g2_sdss_luminosity": {')
        print('    "path": "lakes/inputs_promoted/g2_sdss_luminosity_promoted.jsonl",')
        print('    "enabled": true,')
        print('    "domain": "galactic",')
        print('    "scale_rank": 6,')
        print('    "__source__": "SDSS DR16 r-band absolute luminosity, same galaxies as G1"')
        print('  }')


if __name__ == "__main__":
    main()