# ==============================================================================
# SCRIPT: scalarize.py
# SERIES: P-Series / P2_OrbitalRadius
# LAKE:   p2_orbital_radius
# STEP:   3 of 4  (build_lake → promote → scalarize → validate)
#
# FORMULA
# -------
#   scalar = log(1 + pl_orbsmax) / log(k_geo)
#
# where pl_orbsmax is the orbital semi-major axis in Astronomical Units (AU).
#
# Physical motivation:
#   Orbital radii in the confirmed exoplanet catalog span roughly:
#     0.003 AU  — ultra-hot Jupiters (closest measured orbits)
#     0.01-0.1  — hot Jupiters (large cluster, observational bias)
#     0.3-2.0   — warm/temperate zone planets
#     2.0-6.0   — cold gas giants (Jupiter analogs)
#     >6 AU     — wide-orbit planets (sparse, harder to detect)
#
#   The distribution is strongly non-uniform — hot Jupiters form a large
#   cluster at the low end due to transit detection bias. This clustering
#   is physically and observationally real and will produce a clean
#   non-uniform scalar distribution.
#
#   log(1 + pl_orbsmax) maps:
#     0.003 AU  → scalar ≈ 0.002
#     0.05 AU   → scalar ≈ 0.028
#     1 AU      → scalar ≈ 0.416
#     5 AU      → scalar ≈ 1.063
#     30 AU     → scalar ≈ 2.082
#
# PHYSICAL QUESTION
# -----------------
#   P1 orbital period is at 22/π (z=43) — the derivation bridge modulus.
#   Kepler's third law: T² ∝ a³ (period squared ∝ radius cubed).
#   If P2 radius lands at 22/π with P1: the lattice sees Keplerian
#   geometry as unified — period and radius are the same harmonic.
#   If P2 lands at a different register: the lattice distinguishes between
#   the TIMING of an orbit (period) and the GEOMETRY of an orbit (radius).
#   Both outcomes advance the framework.
#
# INPUT:  lake/p2_orbital_radius_promoted.jsonl  (updated in-place)
# ==============================================================================

import json
import math
import statistics
import shutil
from pathlib import Path

PI    = math.pi
K_GEO = 16.0 / PI

SCRIPT_DIR  = Path(__file__).resolve().parent
LAKE_DIR    = SCRIPT_DIR.parent / "lake"
PROMOTED_IN = LAKE_DIR / "p2_orbital_radius_promoted.jsonl"


def radius_scalar(pl_orbsmax_au: float) -> float:
    """
    scalar = log(1 + pl_orbsmax) / log(k_geo)
    pl_orbsmax in AU.
    """
    return math.log(1.0 + pl_orbsmax_au) / math.log(K_GEO)


def scalarize():
    if not PROMOTED_IN.exists():
        print(f"Promoted file not found: {PROMOTED_IN}")
        print("Run promote.py first.")
        return

    print(f"Scalarizing: {PROMOTED_IN}")
    print()

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
                raw    = rec["meta"]["source_row"]["_raw_payload"]
                smax   = float(raw["pl_orbsmax"])

                if smax <= 0:
                    n_skipped += 1
                    continue

                scalar = radius_scalar(smax)
                rec["scalar_kls"] = scalar
                rec["scalar_klc"] = scalar
                rec["meta"]["source_row"]["scalar_kls"] = scalar
                rec["meta"]["source_row"]["scalar_klc"] = scalar
                rec["meta"]["scalarization_formula"] = (
                    "scalar = log(1 + pl_orbsmax_AU) / log(k_geo)"
                )

                fout.write(json.dumps(rec) + "\n")
                scalars.append(scalar)
                n_written += 1

            except (KeyError, ValueError, TypeError):
                n_skipped += 1
                continue

    shutil.move(str(tmp), str(PROMOTED_IN))

    print(f"Written: {n_written:,}  Skipped: {n_skipped:,}")
    print()

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
            print("  FAIL — review formula in scalarize.py")
    print()
    print("Next step: python validate.py")


if __name__ == "__main__":
    scalarize()