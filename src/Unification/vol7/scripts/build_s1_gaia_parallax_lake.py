# ==============================================================================
# SCRIPT: build_s1_gaia_parallax_lake.py
# SERIES: S-Series / S1_GaiaParallax
# DOMAIN: stellar
# SOURCE: Gaia DR3 stellar parallax — 2,000,000 stars in 4 sky quadrants
#         Extracted from SDSS footprint, even sky coverage NW/NE/SE/SW
#
# RAW LAKE: S-Series/S1_GaiaParallax/lake/s1_gaia_parallax_raw.jsonl
#   Source file: S-Series/NS6_7/lake/Master_Stellar_Gaia_Standard.jsonl
#   Copy relevant fields to clean lake before running this script.
#   Fields: source_id, ra, dec, dist_pc, sector, kish_bin
#   Records: 2,000,000
#
# SCALARIZATION:
#   scalar = log(dist_pc + 1) / log(k_geo)
#   dist_pc: stellar distance in parsecs (from Gaia parallax inversion)
#   Range in sample: ~150 to 1009 pc -> scalar ~3.08 to 4.25
#   Overlaps with FRB and cosmological scalar ranges — comparable scale
#
# POLARITY / EGG-CARTON NOTE:
#   Four-quadrant sky coverage (NW/NE/SE/SW) means below-horizon objects
#   may show systematic polarity effects in clustering.
#   The sector field is preserved in _raw_payload for post-hoc normalization.
#   The scramble null will reveal if signal is position-driven.
#
# NULL MIRROR: NS1_GaiaParallax
#   Chaos null: uniform random over same distance range
#   Scramble null: shuffled distances (preserves distribution)
#   If scramble matches real: positional/spatial clustering drives signal.
#   Document, do not discard.
#
# FILTERING:
#   dist_pc <= 0: exclude (invalid parallax)
#   dist_pc > 100000: exclude (unphysical distance, likely error)
#
# OUTPUT:
#   vol5/lakes/inputs_promoted/s1_gaia_parallax_promoted.jsonl
#
# AUTHORS: Timothy John Kish & Mondy
# AUDIT STATUS: mondy_verified_2026-04
# ==============================================================================

import json
import math
import uuid
from datetime import datetime, timezone
from pathlib import Path

PI    = math.pi
K_GEO = 16.0 / PI
LOG_K = math.log(K_GEO)

SCRIPTS_DIR  = Path(__file__).resolve().parent
S1_DIR       = SCRIPTS_DIR.parent
S_SERIES     = S1_DIR.parent
VOL5_ROOT    = S_SERIES.parent
PROMOTED     = VOL5_ROOT / "lakes" / "inputs_promoted"

RAW_INPUT    = S1_DIR / "lake" / "s1_gaia_parallax_raw.jsonl"
OUTPUT_PATH  = PROMOTED / "s1_gaia_parallax_promoted.jsonl"

DIST_MAX     = 100000.0   # parsecs — hard upper filter

def compute_scalar(rec):
    """
    scalar = log(dist_pc + 1) / log(k_geo)
    Returns float or None if invalid.
    """
    d = rec.get("dist_pc")
    if d is None:
        return None
    try:
        dist = float(d)
        if dist <= 0 or dist > DIST_MAX:
            return None
        return math.log(dist + 1.0) / LOG_K
    except (TypeError, ValueError):
        return None

def main():
    print("=" * 60)
    print("S1 Gaia Parallax Lake Builder")
    print("=" * 60)
    print(f"k_geo = {K_GEO:.10f}")
    print(f"Input:  {RAW_INPUT}")
    print(f"Output: {OUTPUT_PATH}")
    print(f"Filter: dist_pc > 0 and dist_pc <= {DIST_MAX:.0f}")
    print()

    if not RAW_INPUT.exists():
        raise SystemExit(
            f"Raw lake not found: {RAW_INPUT}\n"
            f"Copy Master_Stellar_Gaia_Standard.jsonl to this location first:\n"
            f"  cp S-Series/NS6_7/lake/Master_Stellar_Gaia_Standard.jsonl "
            f"  S-Series/S1_GaiaParallax/lake/s1_gaia_parallax_raw.jsonl"
        )

    PROMOTED.mkdir(parents=True, exist_ok=True)
    now_ts   = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    total    = 0
    computed = 0
    filtered = 0
    failed   = 0

    sector_counts = {}

    with RAW_INPUT.open("r", encoding="utf-8") as fin, \
         OUTPUT_PATH.open("w", encoding="utf-8") as fout:

        for line in fin:
            line = line.strip()
            if not line:
                continue
            total += 1
            raw = json.loads(line)
            s   = compute_scalar(raw)

            if s is None:
                # Check if filtered vs failed
                d = raw.get("dist_pc")
                if d is not None:
                    filtered += 1
                else:
                    failed += 1
                continue

            computed += 1
            sector = raw.get("sector", "unknown")
            sector_counts[sector] = sector_counts.get(sector, 0) + 1

            rec = {
                "entity_id":   str(uuid.uuid4()),
                "domain":      "stellar",
                "volume":      5,
                "lake_id":     "s1_gaia_parallax",
                "geometry_payload": {
                    "coordinates":    [raw.get("ra", 0), raw.get("dec", 0)],
                    "dimensionality": 2,
                    "geometry_type":  "sky_position",
                },
                "scalar_kls":  s,
                "scalar_klc":  s,
                "meta": {
                    "source":           "Gaia DR3 — stellar parallax distances",
                    "ingest_timestamp": now_ts,
                    "sovereign":        True,
                    "audit_status":     "mondy_verified_2026-04",
                    "scalarization":    "log(dist_pc + 1) / log(k_geo)",
                    "sector":           sector,
                    "polarity_note":    (
                        "Four-quadrant sky coverage. Sector field preserved "
                        "for polarity/egg-carton normalization if needed."
                    ),
                },
                "_raw_payload": raw,
            }
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")

            # Progress report every 500k
            if total % 500000 == 0:
                print(f"  Progress: {total:,} read, {computed:,} promoted...")

    print(f"total={total:,}  computed={computed:,}  "
          f"filtered={filtered:,}  failed={failed:,}")
    print(f"Sector distribution: {sector_counts}")
    print(f"-> {OUTPUT_PATH.name}")
    print()
    print("Next: add s1_gaia_parallax to configs/volumes.json")
    print("      domain: stellar, scale_rank: 3")
    print("      Run build_chaos_nulls.py after wiring in")
    print("      Watch scramble null — polarity effects expected")

if __name__ == "__main__":
    main()