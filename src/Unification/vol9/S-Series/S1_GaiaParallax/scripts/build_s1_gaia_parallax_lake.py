# ==============================================================================
# SCRIPT: build_s1_gaia_parallax_lake.py
# SERIES: S-Series / S1_GaiaParallax
# DOMAIN: stellar
# SOURCE: Gaia DR3 stellar parallax distances
#         2,000,000 stars in 4 sky quadrants (NW/NE/SE/SW)
#
# RAW LAKE: S-Series/S1_GaiaParallax/lake/s1_gaia_parallax_raw.jsonl
#   Copy from: S-Series/NS6_7/lake/Master_Stellar_Gaia_Standard.jsonl
#   Fields: source_id, ra, dec, dist_pc, sector, kish_bin
#
# SCALARIZATION:
#   scalar = log(dist_pc + 1) / log(k_geo)
#   Range: ~2.42 (50pc) to ~5.66 (10000pc)
#   Overlaps with FRB, cosmology, biology_amino
#
# SECTOR NORMALIZATION:
#   Four-quadrant coverage (NW/NE/SE/SW) introduces spatial bias.
#   Below-horizon polarity and galactic plane effects can create
#   systematic scalar offsets per sector (egg-carton effect).
#   Fix: scalar_norm = scalar - sector_mean + global_mean
#   This preserves kinematic structure, removes spatial offset.
#   Both raw and normalized scalars are stored for comparison.
#
# FILTERING:
#   dist_pc <= 0: exclude
#   dist_pc > 100000: exclude (unphysical)
#
# NULL MIRROR: NS1_GaiaParallax
#   Chaos null: uniform random over same distance range
#
# AUTHORS: Timothy John Kish & Mondy
# AUDIT STATUS: mondy_verified_2026-04
# ==============================================================================

import json
import math
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

PI    = math.pi
K_GEO = 16.0 / PI
LOG_K = math.log(K_GEO)

SCRIPTS_DIR = Path(__file__).resolve().parent
S1_DIR      = SCRIPTS_DIR.parent
S_SERIES    = S1_DIR.parent
VOL5_ROOT   = S_SERIES.parent
PROMOTED    = VOL5_ROOT / "lakes" / "inputs_promoted"

RAW_INPUT   = S1_DIR / "lake" / "s1_gaia_parallax_raw.jsonl"
OUTPUT_PATH = PROMOTED / "s1_gaia_parallax_promoted.jsonl"

DIST_MAX    = 100000.0

def compute_scalar(dist_pc):
    if dist_pc is None or dist_pc <= 0 or dist_pc > DIST_MAX:
        return None
    return math.log(float(dist_pc) + 1.0) / LOG_K

def main():
    print("=" * 60)
    print("S1 Gaia Parallax Lake Builder")
    print("=" * 60)
    print(f"k_geo = {K_GEO:.10f}")
    print(f"Input:  {RAW_INPUT}")
    print(f"Output: {OUTPUT_PATH}")
    print()

    if not RAW_INPUT.exists():
        raise SystemExit(
            f"Raw lake not found: {RAW_INPUT}\n"
            f"Run from vol5 root:\n"
            f"  copy S-Series\\NS6_7\\lake\\Master_Stellar_Gaia_Standard.jsonl "
            f"S-Series\\S1_GaiaParallax\\lake\\s1_gaia_parallax_raw.jsonl"
        )

    PROMOTED.mkdir(parents=True, exist_ok=True)
    now_ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    # Pass 1: compute raw scalars and sector means
    print("Pass 1: computing raw scalars and sector means...")
    raw_records = []
    sector_sums   = defaultdict(float)
    sector_counts = defaultdict(int)
    total = filtered = failed = 0

    with RAW_INPUT.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            rec  = json.loads(line)
            dist = rec.get("dist_pc")
            s    = compute_scalar(dist)

            if s is None:
                filtered += 1
                continue

            sector = rec.get("sector", "unknown")
            sector_sums[sector]   += s
            sector_counts[sector] += 1
            raw_records.append((rec, s, sector))

            if total % 500000 == 0:
                print(f"  Pass 1: {total:,} read, {len(raw_records):,} kept...")

    computed = len(raw_records)
    global_mean = sum(sector_sums.values()) / max(1, computed)
    sector_means = {
        sec: sector_sums[sec] / sector_counts[sec]
        for sec in sector_counts
    }

    print(f"Pass 1 done: total={total:,}  computed={computed:,}  filtered={filtered:,}")
    print(f"Global mean scalar: {global_mean:.4f}")
    print("Sector means (raw):")
    for sec, mean in sorted(sector_means.items()):
        print(f"  {sec}: {mean:.4f}  (n={sector_counts[sec]:,})")

    # Pass 2: apply normalization and write
    print()
    print("Pass 2: applying sector normalization and writing...")

    scalars_raw  = []
    scalars_norm = []

    with OUTPUT_PATH.open("w", encoding="utf-8") as fout:
        for rec, s_raw, sector in raw_records:
            s_norm = s_raw - sector_means.get(sector, global_mean) + global_mean

            scalars_raw.append(s_raw)
            scalars_norm.append(s_norm)

            out = {
                "entity_id":   str(uuid.uuid4()),
                "domain":      "stellar",
                "volume":      5,
                "lake_id":     "s1_gaia_parallax",
                "geometry_payload": {
                    "coordinates":    [rec.get("ra", 0), rec.get("dec", 0)],
                    "dimensionality": 2,
                    "geometry_type":  "sky_position",
                },
                "scalar_kls":  s_norm,
                "scalar_klc":  s_norm,
                "meta": {
                    "source":            "Gaia DR3 stellar parallax distances",
                    "ingest_timestamp":  now_ts,
                    "sovereign":         True,
                    "audit_status":      "mondy_verified_2026-04",
                    "scalarization":     "log(dist_pc + 1) / log(k_geo)",
                    "sector_normalized": True,
                    "scalar_raw":        round(s_raw, 6),
                    "sector":            sector,
                    "sector_mean":       round(sector_means.get(sector, global_mean), 6),
                    "global_mean":       round(global_mean, 6),
                },
                "_raw_payload": rec,
            }
            fout.write(json.dumps(out, ensure_ascii=False) + "\n")

    print(f"Written: {computed:,} records -> {OUTPUT_PATH.name}")
    print()
    print("Raw scalar range (before normalization):")
    print(f"  min={min(scalars_raw):.4f}  max={max(scalars_raw):.4f}  "
          f"mean={sum(scalars_raw)/len(scalars_raw):.4f}")
    print("Normalized scalar range (after sector normalization):")
    print(f"  min={min(scalars_norm):.4f}  max={max(scalars_norm):.4f}  "
          f"mean={sum(scalars_norm)/len(scalars_norm):.4f}")
    print()
    print("Next:")
    print("  1. Set s1_gaia_parallax enabled:true in configs/volumes.json")
    print("  2. python scalarize.py && python unify.py")
    print("  3. python build_chaos_nulls.py && python build_pinch_table.py")
    print("  Watch: stellar domain joining the cross-domain table")

if __name__ == "__main__":
    main()