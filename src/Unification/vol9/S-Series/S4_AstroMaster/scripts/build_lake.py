# ==============================================================================
# SCRIPT: build_lake.py
# SERIES: S-Series / S4_AstroMaster
# LAKE:   s4_gaia_colour
# STEP:   1 of 4  (build_lake → promote → scalarize → validate)
#
# PURPOSE
# -------
# Convert the Gaia DR3 CSV download into a clean raw JSONL lake.
# No scalarization. No sovereign schema. Just clean, typed records.
#
# Each Series branch is sovereign and self-contained.
# This script assumes no dependency on any other lake or Series.
# It pulls directly from the Gaia source as if nothing else exists.
#
# INPUT
# -----
# Gaia DR3 CSV download from:
#   https://gaia.ari.uni-heidelberg.de/tap.html  (mirror — recommended)
#   OR https://gea.esac.esa.int/tap-server/tap   (primary when available)
#
# ADQL query:
#   SELECT source_id, ra, dec, parallax, bp_rp
#   FROM gaiadr3.gaia_source
#   WHERE parallax > 0
#     AND parallax_over_error > 10
#     AND ruwe < 1.4
#     AND bp_rp IS NOT NULL
#   LIMIT 2000000
#
# Format:        CSV
# Size limit:    2000000 rows
# Duration:      60 minutes
#
# Save CSV as:
#   lake/s4_gaia_colour_source.csv
#
# OUTPUT
# ------
#   lake/s4_gaia_colour_raw.jsonl
#
# SAME-OBJECT CONTEXT
# -------------------
# S1 (parallax distance)    → stellar          → 24/π (z=22)
# S2 (transverse velocity)  → stellar_kinematic → 16/π (z=103)
# S3 (absolute luminosity)  → stellar          → register unknown
# S4 (colour / temperature) → stellar          → register unknown  ← this lake
#
# All four lakes use the same 1.81 million Gaia DR3 stars.
# bp_rp is the Gaia blue-red photometry index — proxy for stellar
# surface temperature: low bp_rp = hot blue star, high bp_rp = cool red.
#
# PHYSICAL QUESTION THIS LAKE ANSWERS
# ------------------------------------
# S2 velocity locks to 16/π. S1 distance locks to 24/π.
# Does stellar surface temperature lock to the same register as velocity,
# or distance, or a completely different harmonic?
# ==============================================================================

import csv
import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
LAKE_DIR   = SCRIPT_DIR.parent / "lake"
CSV_IN     = LAKE_DIR / "s4_gaia_colour_source.csv"
JSONL_OUT  = LAKE_DIR / "s4_gaia_colour_raw.jsonl"

REQUIRED_FIELDS = ["source_id", "ra", "dec", "parallax", "bp_rp"]


def build():
    if not CSV_IN.exists():
        print(f"CSV not found: {CSV_IN}")
        print()
        print("Download instructions:")
        print("  1. Go to: https://gaia.ari.uni-heidelberg.de/tap.html")
        print("     (or https://gea.esac.esa.int/tap-server/tap when available)")
        print("  2. Format: CSV")
        print("  3. Size limit: 2000000 rows")
        print("  4. Duration limit: 60 minutes")
        print("  5. ADQL query:")
        print("     SELECT source_id, ra, dec, parallax, bp_rp")
        print("     FROM gaiadr3.gaia_source")
        print("     WHERE parallax > 0")
        print("       AND parallax_over_error > 10")
        print("       AND ruwe < 1.4")
        print("       AND bp_rp IS NOT NULL")
        print("     LIMIT 2000000")
        print()
        print(f"  Save as: {CSV_IN}")
        return

    print(f"Reading: {CSV_IN}")
    n_written = n_skipped = 0

    LAKE_DIR.mkdir(parents=True, exist_ok=True)

    with open(CSV_IN, newline="", encoding="utf-8") as fin, \
         open(JSONL_OUT, "w", encoding="utf-8") as fout:

        reader = csv.DictReader(fin)

        missing = [f for f in REQUIRED_FIELDS if f not in reader.fieldnames]
        if missing:
            print(f"MISSING FIELDS in CSV: {missing}")
            print("Check your ADQL query includes all required columns.")
            return

        for row in reader:
            try:
                bp_rp = row.get("bp_rp", "").strip()
                if not bp_rp:
                    n_skipped += 1
                    continue

                rec = {
                    "source_id": str(row["source_id"]).strip(),
                    "ra":        float(row["ra"]),
                    "dec":       float(row["dec"]),
                    "parallax":  float(row["parallax"]),
                    "bp_rp":     float(bp_rp),
                }

                if rec["parallax"] <= 0:
                    n_skipped += 1
                    continue

                fout.write(json.dumps(rec) + "\n")
                n_written += 1

            except (ValueError, KeyError):
                n_skipped += 1
                continue

    print(f"Written: {n_written:,}  Skipped: {n_skipped:,}")
    print(f"Output:  {JSONL_OUT}")
    print()
    print("Next step: python promote.py")


if __name__ == "__main__":
    build()