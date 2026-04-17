# ==============================================================================
# SCRIPT: scalarize.py
# SERIES: S-Series / S4_AstroMaster
# LAKE:   s4_gaia_colour
# STEP:   3 of 4  (build_lake → promote → scalarize → validate)
#
# FORMULA
# -------
#   scalar = log(1 + max(bp_rp, 0.01)) / log(k_geo)
#
# Physical motivation:
#   bp_rp = Gaia blue (B) minus red (R) photometry index.
#   Proxy for stellar surface temperature:
#     bp_rp ≈ -0.5 to +0.0  → hot O/B stars (rare)
#     bp_rp ≈ +0.6 to +0.8  → A stars
#     bp_rp ≈ +0.8 to +1.5  → solar-type F/G/K stars (main sequence peak)
#     bp_rp ≈ +1.5 to +3.0  → cool K/M dwarfs and red giants
#     bp_rp > 3.0            → very cool red stars
#
#   The distribution clusters at the main sequence (bp_rp ≈ 0.8–1.5).
#   log(1 + bp_rp) maps this to scalar ≈ 0.44–0.56 for the main cluster.
#   Giants and dwarfs produce spread above and below.
#
#   The max(bp_rp, 0.01) handles the rare negative values from hot blue
#   stars without distorting the distribution.
#
# PHYSICAL QUESTION
# -----------------
#   S2 (velocity) locks to 16/π. S1 (distance) locks to 24/π.
#   Does surface temperature (colour) lock to the same register as velocity
#   (kinematic coupling) or distance (boundary coupling) or neither?
#   If colour locks at a different register from both: photospheric temperature
#   is governed by a distinct harmonic from kinematic and structural geometry.
#   If colour locks at 12/π (molecular register): temperature may couple to
#   the same geometric family as molecular bond geometry.
#
# INPUT:  lake/s4_gaia_colour_promoted.jsonl  (updated in-place)
# ==============================================================================

import json
import math
import statistics
import shutil
from pathlib import Path

PI    = math.pi
K_GEO = 16.0 / PI

SCRIPT_DIR   = Path(__file__).resolve().parent
LAKE_DIR     = SCRIPT_DIR.parent / "lake"
PROMOTED_IN  = LAKE_DIR / "s4_gaia_colour_promoted.jsonl"


def colour_scalar(bp_rp: float) -> float:
    """
    scalar = log(1 + max(bp_rp, 0.01)) / log(k_geo)
    Handles rare negative bp_rp from hot blue stars.
    """
    return math.log(1.0 + max(bp_rp, 0.01)) / math.log(K_GEO)


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
                raw   = rec["meta"]["source_row"]["_raw_payload"]
                bp_rp = float(raw["bp_rp"])

                scalar = colour_scalar(bp_rp)
                rec["scalar_kls"] = scalar
                rec["scalar_klc"] = scalar
                rec["meta"]["source_row"]["scalar_kls"] = scalar
                rec["meta"]["source_row"]["scalar_klc"] = scalar
                rec["meta"]["scalarization_formula"] = (
                    "scalar = log(1 + max(bp_rp, 0.01)) / log(k_geo)"
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