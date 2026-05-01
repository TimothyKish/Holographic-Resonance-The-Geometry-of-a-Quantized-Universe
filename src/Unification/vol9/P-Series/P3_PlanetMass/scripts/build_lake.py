# ==============================================================================
# SCRIPT: build_lake.py
# SERIES: P-Series / P3_PlanetMass
# LAKE:   p3_planet_mass
# STEP:   1 of 4  (build_lake → promote → scalarize → validate)
#
# PURPOSE
# -------
# Download planet mass data from the NASA Exoplanet Archive and write
# a clean raw JSONL lake. No scalarization. No sovereign schema.
#
# Each Series branch is sovereign and self-contained.
# This script assumes no dependency on any other lake or Series.
#
# INPUT
# -----
# NASA Exoplanet Archive — Planetary Systems Composite Parameters table.
# Direct CSV download (no account required). Script auto-downloads.
#
# OUTPUT
# ------
#   lake/p3_planet_mass_raw.jsonl
#
# SAME-OBJECT CONTEXT
# -------------------
# P1 (orbital period)  → orbital → 22/π (z=43)  ← confirmed
# P2 (orbital radius)  → orbital → register unknown
# P3 (planet mass)     → orbital → register unknown  ← this lake
#
# PHYSICAL QUESTION THIS LAKE ANSWERS
# ------------------------------------
# P1 period and P2 radius are both orbital geometry — they describe HOW
# the planet moves. Mass describes WHAT the planet is.
# Does the lattice distinguish between the geometry of an orbit and the
# mass of the object following it? If mass lands at a different register
# from period and radius: the lattice sees dynamics and matter separately.
# If mass lands at the same register: mass, period, and radius are all
# expressions of the same orbital harmonic.
# ==============================================================================

import csv
import json
import urllib.request
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
LAKE_DIR   = SCRIPT_DIR.parent / "lake"
CSV_IN     = LAKE_DIR / "p3_planet_mass_source.csv"
JSONL_OUT  = LAKE_DIR / "p3_planet_mass_raw.jsonl"

NASA_URL = (
    "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?"
    "query=SELECT+pl_name,hostname,pl_bmassj,pl_bmassjerr1,"
    "pl_bmassjerr2,pl_bmassprov,sy_dist,disc_facility"
    "+FROM+pscomppars"
    "+WHERE+pl_bmassj+IS+NOT+NULL+AND+pl_bmassj+%3E+0"
    "&format=csv"
)

REQUIRED_FIELDS = ["pl_name", "pl_bmassj"]


def download_csv():
    print("Downloading from NASA Exoplanet Archive...")
    print(f"  URL: {NASA_URL[:80]}...")
    try:
        LAKE_DIR.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(NASA_URL, CSV_IN)
        print(f"  Saved: {CSV_IN}")
        return True
    except Exception as e:
        print(f"  Download failed: {e}")
        print()
        print("  Manual download: open this URL in your browser and save as CSV:")
        print(f"  {NASA_URL}")
        print(f"  Save as: {CSV_IN}")
        return False


def build():
    if not CSV_IN.exists():
        print(f"CSV not found: {CSV_IN}")
        print()
        ok = download_csv()
        if not ok:
            return
        print()

    print(f"Reading: {CSV_IN}")
    n_written = n_skipped = 0

    LAKE_DIR.mkdir(parents=True, exist_ok=True)

    with open(CSV_IN, newline="", encoding="utf-8") as fin, \
         open(JSONL_OUT, "w", encoding="utf-8") as fout:

        reader = csv.DictReader(fin)

        missing = [f for f in REQUIRED_FIELDS if f not in reader.fieldnames]
        if missing:
            print(f"MISSING FIELDS in CSV: {missing}")
            print("Check the NASA Archive query includes all required columns.")
            return

        for row in reader:
            try:
                mass = row.get("pl_bmassj", "").strip()
                if not mass:
                    n_skipped += 1
                    continue

                rec = {
                    "pl_name":      str(row["pl_name"]).strip(),
                    "hostname":     str(row.get("hostname", "")).strip(),
                    "pl_bmassj":    float(mass),          # Jupiter masses
                    "pl_bmassjerr1": float(row["pl_bmassjerr1"])
                                     if row.get("pl_bmassjerr1","").strip()
                                     else None,
                    "pl_bmassjerr2": float(row["pl_bmassjerr2"])
                                     if row.get("pl_bmassjerr2","").strip()
                                     else None,
                    "pl_bmassprov": str(row.get("pl_bmassprov","")).strip(),
                    "sy_dist":      float(row["sy_dist"])
                                     if row.get("sy_dist","").strip()
                                     else None,
                    "disc_facility": str(row.get("disc_facility","")).strip(),
                }

                if rec["pl_bmassj"] <= 0:
                    n_skipped += 1
                    continue

                fout.write(json.dumps(rec) + "\n")
                n_written += 1

            except (ValueError, KeyError):
                n_skipped += 1
                continue

    print(f"Written: {n_written:,}  Skipped: {n_skipped:,}")
    print()
    if n_skipped > 0:
        print(f"  Note: {n_skipped:,} records skipped.")
        print("  Skipped records are missing pl_bmassj measurements.")
        print("  Many confirmed exoplanets have no measured mass — this is")
        print("  expected. Transit-only planets often have radius but not mass.")
    print()
    print(f"Output:  {JSONL_OUT}")
    print()
    print("Next step: python promote.py")


if __name__ == "__main__":
    build()