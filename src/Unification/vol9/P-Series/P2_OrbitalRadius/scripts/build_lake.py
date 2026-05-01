# ==============================================================================
# SCRIPT: build_lake.py
# SERIES: P-Series / P2_OrbitalRadius
# LAKE:   p2_orbital_radius
# STEP:   1 of 4  (build_lake → promote → scalarize → validate)
#
# PURPOSE
# -------
# Download orbital semi-major axis data from the NASA Exoplanet Archive
# and write a clean raw JSONL lake.
# No scalarization. No sovereign schema. Just clean, typed records.
#
# Each Series branch is sovereign and self-contained.
# This script assumes no dependency on any other lake or Series.
#
# INPUT
# -----
# NASA Exoplanet Archive — Planetary Systems Composite Parameters table
# Direct CSV download (no account required):
#
#   https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=
#   SELECT+pl_name,hostname,pl_orbsmax,pl_orbsmaxerr1,pl_orbsmaxerr2,
#   sy_dist,disc_facility
#   +FROM+pscomppars
#   +WHERE+pl_orbsmax+IS+NOT+NULL+AND+pl_orbsmax+%3E+0
#   &format=csv
#
# Or use the convenience function below which builds and fetches the URL.
#
# Save CSV as:   lake/p2_orbital_radius_source.csv
# (The script will also attempt a direct download if the CSV is absent.)
#
# OUTPUT
# ------
#   lake/p2_orbital_radius_raw.jsonl
#
# SAME-OBJECT CONTEXT
# -------------------
# P1 (orbital period)   → orbital → 22/π (z=43)  ← confirmed
# P2 (orbital radius)   → orbital → register unknown  ← this lake
# P3 (planet mass)      → orbital → register unknown  ← next lake
#
# All three lakes use the same ~13,500 confirmed exoplanets.
#
# PHYSICAL QUESTION THIS LAKE ANSWERS
# ------------------------------------
# P1 orbital period locks to 22/π — the derivation bridge modulus.
# Does orbital RADIUS lock to the same 22/π register as period?
# Kepler's third law couples period² ∝ radius³, so they are mathematically
# related. If both land at 22/π: the lattice sees Keplerian geometry as one.
# If radius lands at a different register: the lattice distinguishes between
# the TIMING of an orbit and the GEOMETRY of an orbit — the kinematic
# principle operating at planetary scale.
# ==============================================================================

import csv
import json
import urllib.request
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
LAKE_DIR   = SCRIPT_DIR.parent / "lake"
CSV_IN     = LAKE_DIR / "p2_orbital_radius_source.csv"
JSONL_OUT  = LAKE_DIR / "p2_orbital_radius_raw.jsonl"

NASA_URL = (
    "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?"
    "query=SELECT+pl_name,hostname,pl_orbsmax,pl_orbsmaxerr1,"
    "pl_orbsmaxerr2,sy_dist,disc_facility"
    "+FROM+pscomppars"
    "+WHERE+pl_orbsmax+IS+NOT+NULL+AND+pl_orbsmax+%3E+0"
    "&format=csv"
)

REQUIRED_FIELDS = ["pl_name", "pl_orbsmax"]


def download_csv():
    """Attempt direct download from NASA Exoplanet Archive."""
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
        print("  Manual download instructions:")
        print("  Open this URL in your browser and save as CSV:")
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
                smax = row.get("pl_orbsmax", "").strip()
                if not smax:
                    n_skipped += 1
                    continue

                rec = {
                    "pl_name":       str(row["pl_name"]).strip(),
                    "hostname":      str(row.get("hostname", "")).strip(),
                    "pl_orbsmax":    float(smax),           # AU
                    "pl_orbsmaxerr1": float(row["pl_orbsmaxerr1"])
                                      if row.get("pl_orbsmaxerr1", "").strip()
                                      else None,
                    "pl_orbsmaxerr2": float(row["pl_orbsmaxerr2"])
                                      if row.get("pl_orbsmaxerr2", "").strip()
                                      else None,
                    "sy_dist":       float(row["sy_dist"])
                                      if row.get("sy_dist", "").strip()
                                      else None,             # parsecs
                    "disc_facility": str(row.get("disc_facility", "")).strip(),
                }

                if rec["pl_orbsmax"] <= 0:
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
    if n_skipped > 0:
        print(f"  Note: {n_skipped:,} records skipped.")
        print("  Skipped records have missing or zero pl_orbsmax values.")
        print("  This is expected — not all confirmed exoplanets have a")
        print("  measured semi-major axis. Skips are documented, not errors.")
    print()
    print("Next step: python promote.py")


if __name__ == "__main__":
    build()