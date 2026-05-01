# ==============================================================================
# SCRIPT: promote.py
# SERIES: P-Series / P3_PlanetMass
# LAKE:   p3_planet_mass
# STEP:   2 of 4  (build_lake → promote → scalarize → validate)
#
# INPUT:  lake/p3_planet_mass_raw.jsonl
# OUTPUT: lake/p3_planet_mass_promoted.jsonl
# ==============================================================================

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR   = Path(__file__).resolve().parent
LAKE_DIR     = SCRIPT_DIR.parent / "lake"
RAW_IN       = LAKE_DIR / "p3_planet_mass_raw.jsonl"
PROMOTED_OUT = LAKE_DIR / "p3_planet_mass_promoted.jsonl"

DOMAIN     = "orbital"
LAKE_ID    = "p3_planet_mass"
VOLUME     = 8
SOURCE_DESC = (
    "NASA Exoplanet Archive pscomppars — planet mass in Jupiter masses. "
    "Same confirmed exoplanets as P1 (orbital period) and P2 (orbital radius). "
    "Same-object strategy: P1 period→22/π, P2 radius→unknown, P3 mass→unknown."
)


def promote():
    if not RAW_IN.exists():
        print(f"Raw file not found: {RAW_IN}")
        print("Run build_lake.py first.")
        return

    now_ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    n_written = n_skipped = 0

    print(f"Promoting: {RAW_IN}")

    with open(RAW_IN, encoding="utf-8") as fin, \
         open(PROMOTED_OUT, "w", encoding="utf-8") as fout:

        for i, line in enumerate(fin):
            line = line.strip()
            if not line:
                continue
            try:
                raw = json.loads(line)
            except json.JSONDecodeError:
                n_skipped += 1
                continue

            pl_name   = str(raw.get("pl_name", f"P3_{i:08d}"))
            entity_id = str(uuid.uuid5(uuid.NAMESPACE_DNS,
                                       f"p3_planet_mass_{pl_name}"))

            promoted = {
                "entity_id":   entity_id,
                "domain":      DOMAIN,
                "volume":      VOLUME,
                "lake_id":     LAKE_ID,
                "scalar_kls":  None,
                "scalar_klc":  None,
                "geometry_payload": {
                    "coordinates":    [],
                    "dimensionality": 0,
                    "geometry_type":  "planet_mass"
                },
                "meta": {
                    "source":           "NASA Exoplanet Archive pscomppars",
                    "source_desc":      SOURCE_DESC,
                    "ingest_timestamp": now_ts,
                    "sovereign":        True,
                    "same_object_lakes": [
                        "p1_orbital_periods",
                        "p2_orbital_radius"
                    ],
                    "source_row": {
                        "entity_id":  entity_id,
                        "domain":     DOMAIN,
                        "volume":     VOLUME,
                        "lake_id":    LAKE_ID,
                        "scalar_kls": None,
                        "scalar_klc": None,
                        "meta": {
                            "source":           "NASA Exoplanet Archive",
                            "ingest_timestamp": now_ts,
                            "sovereign":        False,
                        },
                        "_raw_payload": raw
                    }
                }
            }

            fout.write(json.dumps(promoted) + "\n")
            n_written += 1

    print(f"Written: {n_written:,}  Skipped: {n_skipped:,}")
    print(f"Output:  {PROMOTED_OUT}")
    print()
    print("Next step: python scalarize.py")


if __name__ == "__main__":
    promote()