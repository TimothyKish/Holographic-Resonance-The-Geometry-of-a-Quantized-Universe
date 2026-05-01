# ==============================================================================
# SCRIPT: build_g1_galaxy_kinematics_lake.py
# SERIES: G-Series / G1_GalaxyKinematics
# DOMAIN: galactic
# SOURCE: SDSS DR16 galaxy velocity dispersions
#         1,922,069 galaxies in 4 sky quadrants (NW/NE/SE/SW)
#         VizieR catalog V/154, Ahumada+ 2020
#
# RAW LAKE: G-Series/G1_GalaxyKinematics/lake/g1_galaxy_kinematics_raw.jsonl
#   Copy from: S-Series/NS6_7/lake/Master_Galaxy_Vol6_Standard.jsonl
#   Fields: objID, ra, dec, z, vdisp, sector, kish_bin, weight
#
# SCALARIZATION:
#   scalar = log(vdisp + 1) / log(k_geo)
#   Range (clean): ~2.62 (70 km/s) to ~4.14 (849 km/s)
#   Overlaps with FRB (1.67-5.58) and cosmology (2.32-2.60)
#
# FILTERING:
#   vdisp < 70:   exclude (below SDSS spectral resolution)
#   vdisp >= 850: exclude (SDSS hard ceiling, not a real measurement)
#
# SECTOR NORMALIZATION:
#   Four-quadrant sky coverage introduces spatial bias.
#   Below-horizon polarity and galactic plane effects create
#   systematic scalar offsets per sector (egg-carton effect).
#   Fix: scalar_norm = scalar - sector_mean + global_mean
#   Both raw and normalized scalars stored for audit comparison.
#
#   Additional normalization available via redshift z field:
#   Galaxies at different redshifts sample different cosmic epochs.
#   The z field is preserved for post-hoc redshift binning if needed.
#
# NULL MIRROR: NG1_GalaxyKinematics
#   Chaos null: uniform random over same vdisp range (70-849 km/s)
#   Scramble null: shuffled vdisp (preserves distribution, tests position)
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
G1_DIR      = SCRIPTS_DIR.parent
G_SERIES    = G1_DIR.parent
VOL5_ROOT   = G_SERIES.parent
PROMOTED    = VOL5_ROOT / "lakes" / "inputs_promoted"

RAW_INPUT   = G1_DIR / "lake" / "g1_galaxy_kinematics_raw.jsonl"
OUTPUT_PATH = PROMOTED / "g1_galaxy_kinematics_promoted.jsonl"

VDISP_MIN   = 70.0
VDISP_MAX   = 849.9

def compute_scalar(vdisp):
    if vdisp is None:
        return None
    v = float(vdisp)
    if v < VDISP_MIN or v >= VDISP_MAX:
        return None
    return math.log(v + 1.0) / LOG_K

def main():
    print("=" * 60)
    print("G1 Galaxy Kinematics Lake Builder")
    print("=" * 60)
    print(f"k_geo = {K_GEO:.10f}")
    print(f"Input:  {RAW_INPUT}")
    print(f"Output: {OUTPUT_PATH}")
    print(f"Filter: {VDISP_MIN} <= vdisp < {VDISP_MAX} km/s")
    print()

    if not RAW_INPUT.exists():
        raise SystemExit(
            f"Raw lake not found: {RAW_INPUT}\n"
            f"Run from vol5 root:\n"
            f"  copy S-Series\\NS6_7\\lake\\Master_Galaxy_Vol6_Standard.jsonl "
            f"G-Series\\G1_GalaxyKinematics\\lake\\g1_galaxy_kinematics_raw.jsonl"
        )

    PROMOTED.mkdir(parents=True, exist_ok=True)
    now_ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    # Pass 1: compute raw scalars and sector means
    print("Pass 1: computing raw scalars and sector means...")
    raw_records   = []
    sector_sums   = defaultdict(float)
    sector_counts = defaultdict(int)
    ceiling_count = 0
    total = filtered = 0

    with RAW_INPUT.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            rec   = json.loads(line)
            vdisp = rec.get("vdisp")

            if vdisp is not None and float(vdisp) >= 850.0:
                ceiling_count += 1
                filtered += 1
                continue

            s = compute_scalar(vdisp)
            if s is None:
                filtered += 1
                continue

            sector = rec.get("sector", "unknown")
            sector_sums[sector]   += s
            sector_counts[sector] += 1
            raw_records.append((rec, s, sector))

            if total % 500000 == 0:
                print(f"  Pass 1: {total:,} read, {len(raw_records):,} kept...")

    computed    = len(raw_records)
    global_mean = sum(sector_sums.values()) / max(1, computed)
    sector_means = {
        sec: sector_sums[sec] / sector_counts[sec]
        for sec in sector_counts
    }

    print(f"Pass 1 done: total={total:,}  computed={computed:,}  "
          f"filtered={filtered:,}  ceiling={ceiling_count:,}")
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
                "domain":      "galactic",
                "volume":      5,
                "lake_id":     "g1_galaxy_kinematics",
                "geometry_payload": {
                    "coordinates":    [rec.get("ra", 0), rec.get("dec", 0)],
                    "dimensionality": 2,
                    "geometry_type":  "sky_position",
                },
                "scalar_kls":  s_norm,
                "scalar_klc":  s_norm,
                "meta": {
                    "source":            "SDSS DR16 galaxy velocity dispersions (VizieR V/154)",
                    "ingest_timestamp":  now_ts,
                    "sovereign":         True,
                    "audit_status":      "mondy_verified_2026-04",
                    "scalarization":     "log(vdisp + 1) / log(k_geo)",
                    "sector_normalized": True,
                    "scalar_raw":        round(s_raw, 6),
                    "sector":            sector,
                    "sector_mean":       round(sector_means.get(sector, global_mean), 6),
                    "global_mean":       round(global_mean, 6),
                    "redshift_z":        rec.get("z"),
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
    print("  1. Set g1_galaxy_kinematics enabled:true in configs/volumes.json")
    print("  2. python scalarize.py && python unify.py")
    print("  3. python build_chaos_nulls.py && python build_pinch_table.py")
    print("  Watch: galactic domain, sector offset magnitudes,")
    print("  scramble null vs real — egg-carton effect quantified")

if __name__ == "__main__":
    main()