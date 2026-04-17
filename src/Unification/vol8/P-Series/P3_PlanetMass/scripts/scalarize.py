# ==============================================================================
# SCRIPT: scalarize.py
# SERIES: P-Series / P3_PlanetMass
# LAKE:   p3_planet_mass
# STEP:   3 of 4  (build_lake → promote → scalarize → validate)
#
# FORMULA
# -------
#   scalar = log(1 + pl_bmassj) / log(k_geo)
#
# where pl_bmassj is the planet mass in Jupiter masses (Mj).
#
# Physical motivation:
#   Planet masses in the confirmed catalog span roughly:
#     0.001 Mj  — super-Earths and Neptune-class (lower detection limit)
#     0.05  Mj  — Saturn-class
#     0.3   Mj  — sub-Jovian
#     1.0   Mj  — Jupiter analog
#     3-13  Mj  — super-Jupiters
#     >13   Mj  — brown dwarf boundary
#
#   The distribution clusters at detection biases: hot Jupiters (1-3 Mj)
#   are over-represented in radial velocity surveys. This non-uniform
#   clustering ensures the chaos null test will detect genuine structure.
#
#   log(1 + pl_bmassj) maps:
#     0.001 Mj  → scalar ≈ 0.001
#     0.1   Mj  → scalar ≈ 0.057
#     1.0   Mj  → scalar ≈ 0.416
#     10    Mj  → scalar ≈ 0.927
#     40    Mj  → scalar ≈ 1.239
#
# INPUT:  lake/p3_planet_mass_promoted.jsonl  (updated in-place)
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
PROMOTED_IN = LAKE_DIR / "p3_planet_mass_promoted.jsonl"


def mass_scalar(pl_bmassj: float) -> float:
    """scalar = log(1 + pl_bmassj) / log(k_geo)"""
    return math.log(1.0 + pl_bmassj) / math.log(K_GEO)


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
                raw  = rec["meta"]["source_row"]["_raw_payload"]
                mass = float(raw["pl_bmassj"])

                if mass <= 0:
                    n_skipped += 1
                    continue

                scalar = mass_scalar(mass)
                rec["scalar_kls"] = scalar
                rec["scalar_klc"] = scalar
                rec["meta"]["source_row"]["scalar_kls"] = scalar
                rec["meta"]["source_row"]["scalar_klc"] = scalar
                rec["meta"]["scalarization_formula"] = (
                    "scalar = log(1 + pl_bmassj_Mj) / log(k_geo)"
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