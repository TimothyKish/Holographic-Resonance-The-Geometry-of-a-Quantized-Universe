# ==============================================================================
# SCRIPT: promote.py
# SERIES: S-Series / S4_AstroMaster
# LAKE:   s4_gaia_colour
# STEP:   2 of 4  (build_lake → promote → scalarize → validate)
#
# PURPOSE
# -------
# Apply the sovereign lake schema to raw records.
# Preserves all original raw fields in meta._raw_payload.
# Does NOT compute scalar — that is scalarize.py's job.
#
# INPUT:  lake/s4_gaia_colour_raw.jsonl
# OUTPUT: lake/s4_gaia_colour_promoted.jsonl
# ==============================================================================

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR   = Path(__file__).resolve().parent
LAKE_DIR     = SCRIPT_DIR.parent / "lake"
RAW_IN       = LAKE_DIR / "s4_gaia_colour_raw.jsonl"
PROMOTED_OUT = LAKE_DIR / "s4_gaia_colour_promoted.jsonl"

DOMAIN     = "stellar"
LAKE_ID    = "s4_gaia_colour"
VOLUME     = 8
SOURCE_DESC = (
    "Gaia DR3 bp_rp colour index (surface temperature proxy). "
    "Same 1.81M stars as S1 (parallax distance), S2 (transverse velocity), "
    "and S3 (absolute luminosity). "
    "Same-object strategy: S1→24/π, S2→16/π, S3→unknown, S4→unknown."
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

            source_id = str(raw.get("source_id", f"S4_{i:010d}"))
            entity_id = str(uuid.uuid5(uuid.NAMESPACE_DNS,
                                       f"s4_gaia_colour_{source_id}"))

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
                    "geometry_type":  "colour"
                },
                "meta": {
                    "source":           "Gaia DR3",
                    "source_desc":      SOURCE_DESC,
                    "ingest_timestamp": now_ts,
                    "sovereign":        True,
                    "same_object_lakes": [
                        "s1_gaia_parallax",
                        "s2_stellar_kinematics",
                        "s3_gaia_luminosity"
                    ],
                    "source_row": {
                        "entity_id":  entity_id,
                        "domain":     DOMAIN,
                        "volume":     VOLUME,
                        "lake_id":    LAKE_ID,
                        "scalar_kls": None,
                        "scalar_klc": None,
                        "meta": {
                            "source":           "Gaia DR3",
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