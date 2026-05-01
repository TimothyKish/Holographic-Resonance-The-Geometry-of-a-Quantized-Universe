# ==============================================================================
# SCRIPT: build_lake.py
# SERIES: S-Series / S3_GalacticNASA
# LAKE:   s3_gaia_luminosity
# STEP:   1 of 4  (build_lake → promote → scalarize → validate)
#
# PURPOSE
# -------
# Convert the Gaia DR3 CSV download into a clean raw JSONL lake.
# No scalarization. No sovereign schema. Just clean, typed records.
#
# INPUT
# -----
# Gaia DR3 CSV download from:
#   https://gaia.ari.uni-heidelberg.de/tap.html  (mirror)
#   OR https://gea.esac.esa.int/tap-server/tap   (primary when up)
#
# ADQL query used:
#   SELECT source_id, ra, dec, parallax, parallax_error,
#          pmra, pmdec, phot_g_mean_mag, bp_rp, ruwe
#   FROM gaiadr3.gaia_source
#   WHERE parallax > 0
#     AND parallax_over_error > 10
#     AND ruwe < 1.4
#     AND phot_g_mean_mag IS NOT NULL
#   LIMIT 2000000
#
# Save CSV as:
#   lake/s3_gaia_luminosity_source.csv
#
# OUTPUT
# ------
#   lake/s3_gaia_luminosity_raw.jsonl
#
# SAME-OBJECT CONTEXT
# -------------------
# S1 (parallax distance) → stellar → 24/π (z=22)
# S2 (transverse velocity) → stellar_kinematic → 16/π (z=103)
# S3 (absolute luminosity) → stellar → register UNKNOWN ← this lake
# S4 (colour / temperature) → stellar → register UNKNOWN ← next lake
#
# All four lakes use the same 1.81 million Gaia DR3 stars.
# ==============================================================================

import csv
import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
LAKE_DIR   = SCRIPT_DIR.parent / "lake"
CSV_IN     = LAKE_DIR / "s3_gaia_luminosity_source.csv"
JSONL_OUT  = LAKE_DIR / "s3_gaia_luminosity_raw.jsonl"

REQUIRED_FIELDS = [
    "source_id", "ra", "dec",
    "parallax", "parallax_error",
    "pmra", "pmdec",
    "phot_g_mean_mag", "bp_rp", "ruwe"
]

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
        print("     SELECT source_id, ra, dec, parallax, parallax_error,")
        print("            pmra, pmdec, phot_g_mean_mag, bp_rp, ruwe")
        print("     FROM gaiadr3.gaia_source")
        print("     WHERE parallax > 0")
        print("       AND parallax_over_error > 10")
        print("       AND ruwe < 1.4")
        print("       AND phot_g_mean_mag IS NOT NULL")
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

        # Verify required fields present
        missing = [f for f in REQUIRED_FIELDS if f not in reader.fieldnames]
        if missing:
            print(f"MISSING FIELDS in CSV: {missing}")
            print("Check your ADQL query includes all required columns.")
            return

        for row in reader:
            try:
                # Cast numeric fields — skip rows with nulls
                rec = {
                    "source_id":         str(row["source_id"]).strip(),
                    "ra":                float(row["ra"]),
                    "dec":               float(row["dec"]),
                    "parallax":          float(row["parallax"]),
                    "parallax_error":    float(row["parallax_error"]),
                    "pmra":              float(row["pmra"]) if row["pmra"] else None,
                    "pmdec":             float(row["pmdec"]) if row["pmdec"] else None,
                    "phot_g_mean_mag":   float(row["phot_g_mean_mag"]),
                    "bp_rp":             float(row["bp_rp"]) if row["bp_rp"] else None,
                    "ruwe":              float(row["ruwe"]) if row["ruwe"] else None,
                }
                # Basic sanity filters
                if rec["parallax"] <= 0 or rec["phot_g_mean_mag"] is None:
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