# ==============================================================================
# SCRIPT: promote.py
# SERIES: S-Series / S3_GalacticNASA
# LAKE:   s3_gaia_luminosity
# STEP:   2 of 4  (build_lake → promote → scalarize → validate)
#
# PURPOSE
# -------
# Apply the sovereign lake schema to raw records.
# Add entity_id, domain, lake_id, volume, ingest timestamp.
# Preserve ALL original raw fields in meta._raw_payload.
# Do NOT compute scalar here — that is scalarize.py's job.
#
# The sovereign guarantee:
#   Every promoted record carries its complete original source data
#   in meta.source_row._raw_payload. Even if the scalarization formula
#   is later found to be wrong, the original data is always recoverable
#   without re-downloading from the source catalog.
#
# INPUT:  lake/s3_gaia_luminosity_raw.jsonl
# OUTPUT: lake/s3_gaia_luminosity_promoted.jsonl
# ==============================================================================

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR  = Path(__file__).resolve().parent
LAKE_DIR    = SCRIPT_DIR.parent / "lake"
RAW_IN      = LAKE_DIR / "s3_gaia_luminosity_raw.jsonl"
PROMOTED_OUT = LAKE_DIR / "s3_gaia_luminosity_promoted.jsonl"

DOMAIN     = "stellar"
LAKE_ID    = "s3_gaia_luminosity"
VOLUME     = 8
SOURCE_DESC = (
    "Gaia DR3 absolute G-band luminosity. "
    "Same 1.81M stars as S1 (parallax distance) and S2 (transverse velocity). "
    "Same-object strategy: S1→24/π, S2→16/π, S3→register unknown."
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

            # Stable entity_id: deterministic UUID from source_id
            source_id = str(raw.get("source_id", f"S3_{i:010d}"))
            entity_id = str(uuid.uuid5(uuid.NAMESPACE_DNS,
                                       f"s3_gaia_luminosity_{source_id}"))

            promoted = {
                "entity_id":   entity_id,
                "domain":      DOMAIN,
                "volume":      VOLUME,
                "lake_id":     LAKE_ID,
                # scalar_kls and scalar_klc are placeholders — filled by scalarize.py
                "scalar_kls":  None,
                "scalar_klc":  None,
                "geometry_payload": {
                    "coordinates":    [],
                    "dimensionality": 0,
                    "geometry_type":  "luminosity"
                },
                "meta": {
                    "source":           "Gaia DR3",
                    "source_desc":      SOURCE_DESC,
                    "ingest_timestamp": now_ts,
                    "sovereign":        True,
                    "same_object_lakes": [
                        "s1_gaia_parallax",
                        "s2_stellar_kinematics"
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
                        "_raw_payload": raw   # ← THE SOVEREIGN GUARANTEE
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