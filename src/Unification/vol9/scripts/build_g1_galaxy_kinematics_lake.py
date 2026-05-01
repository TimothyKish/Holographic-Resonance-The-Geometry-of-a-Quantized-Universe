# ==============================================================================
# SCRIPT: build_g1_galaxy_kinematics_lake.py
# SERIES: G-Series / G1_GalaxyKinematics
# DOMAIN: galactic
# SOURCE: SDSS DR16 galaxy velocity dispersions — 1,922,069 galaxies
#         Four sky quadrants: NW/NE/SE/SW — even sky coverage
#         Authentic SDSS spectroscopic data, VizieR catalog V/154
#
# RAW LAKE: G-Series/G1_GalaxyKinematics/lake/g1_galaxy_kinematics_raw.jsonl
#   Source file: S-Series/NS6_7/lake/Master_Galaxy_Vol6_Standard.jsonl
#   Copy to clean location before running this script.
#   Fields: objID, ra, dec, z, vdisp, sector, kish_bin, weight
#   Records: 1,922,069
#
# SCALARIZATION:
#   scalar = log(vdisp + 1) / log(k_geo)
#   vdisp: stellar velocity dispersion in km/s
#   Range (clean): ~70 to 849 km/s -> scalar ~2.59 to 4.07
#   Overlaps with FRB (1.67-5.58) and Gaia (3.08-4.25) ranges.
#
# FILTERING:
#   vdisp <= 0:    exclude (invalid measurement)
#   vdisp >= 850:  exclude (SDSS hard ceiling — not a real measurement)
#   vdisp < 70:    exclude (below SDSS spectral resolution limit)
#
# POLARITY / EGG-CARTON NOTE:
#   Four-quadrant sky coverage means spatial clustering may dominate
#   over kinematic signal. The sector field is preserved.
#   Scramble null will reveal positional clustering effects.
#   Galactic polarity (above/below galactic plane) may show systematic
#   differences — the ra/dec fields allow post-hoc plane correction.
#
# NULL MIRROR: NG1_GalaxyKinematics
#   Chaos null: uniform random over same vdisp range (70-849 km/s)
#   Scramble null: shuffled vdisp values (preserves distribution)
#
# OUTPUT:
#   vol5/lakes/inputs_promoted/g1_galaxy_kinematics_promoted.jsonl
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
G1_DIR       = SCRIPTS_DIR.parent
G_SERIES     = G1_DIR.parent
VOL5_ROOT    = G_SERIES.parent
PROMOTED     = VOL5_ROOT / "lakes" / "inputs_promoted"

RAW_INPUT    = G1_DIR / "lake" / "g1_galaxy_kinematics_raw.jsonl"
OUTPUT_PATH  = PROMOTED / "g1_galaxy_kinematics_promoted.jsonl"

VDISP_MIN    = 70.0    # km/s — SDSS spectral resolution limit
VDISP_MAX    = 849.9   # km/s — exclude 850.0 ceiling values

def compute_scalar(rec):
    """
    scalar = log(vdisp + 1) / log(k_geo)
    Returns float or None if filtered.
    """
    v = rec.get("vdisp")
    if v is None:
        return None
    try:
        vdisp = float(v)
        if vdisp < VDISP_MIN or vdisp >= VDISP_MAX:
            return None
        return math.log(vdisp + 1.0) / LOG_K
    except (TypeError, ValueError):
        return None

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
            f"Copy Master_Galaxy_Vol6_Standard.jsonl to this location first:\n"
            f"  cp S-Series/NS6_7/lake/Master_Galaxy_Vol6_Standard.jsonl "
            f"  G-Series/G1_GalaxyKinematics/lake/g1_galaxy_kinematics_raw.jsonl"
        )

    PROMOTED.mkdir(parents=True, exist_ok=True)
    now_ts   = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    total    = 0
    computed = 0
    filtered = 0
    failed   = 0
    sector_counts  = {}
    ceiling_count  = 0

    with RAW_INPUT.open("r", encoding="utf-8") as fin, \
         OUTPUT_PATH.open("w", encoding="utf-8") as fout:

        for line in fin:
            line = line.strip()
            if not line:
                continue
            total += 1
            raw = json.loads(line)
            v   = raw.get("vdisp")

            # Track ceiling values specifically
            if v is not None and float(v) >= 850.0:
                ceiling_count += 1
                filtered += 1
                continue

            s = compute_scalar(raw)
            if s is None:
                filtered += 1
                continue

            computed += 1
            sector = raw.get("sector", "unknown")
            sector_counts[sector] = sector_counts.get(sector, 0) + 1

            rec = {
                "entity_id":   str(uuid.uuid4()),
                "domain":      "galactic",
                "volume":      5,
                "lake_id":     "g1_galaxy_kinematics",
                "geometry_payload": {
                    "coordinates":    [raw.get("ra", 0), raw.get("dec", 0)],
                    "dimensionality": 2,
                    "geometry_type":  "sky_position",
                },
                "scalar_kls":  s,
                "scalar_klc":  s,
                "meta": {
                    "source":           "SDSS DR16 — galaxy velocity dispersions (VizieR V/154)",
                    "ingest_timestamp": now_ts,
                    "sovereign":        True,
                    "audit_status":     "mondy_verified_2026-04",
                    "scalarization":    "log(vdisp + 1) / log(k_geo)",
                    "sector":           sector,
                    "redshift_z":       raw.get("z"),
                    "polarity_note":    (
                        "Four-quadrant sky coverage. Galactic plane polarity "
                        "may produce egg-carton clustering effect. "
                        "Sector and ra/dec preserved for normalization."
                    ),
                },
                "_raw_payload": raw,
            }
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")

            if total % 500000 == 0:
                print(f"  Progress: {total:,} read, {computed:,} promoted...")

    print(f"total={total:,}  computed={computed:,}  "
          f"filtered={filtered:,}  failed={failed:,}")
    print(f"Ceiling values (vdisp=850) removed: {ceiling_count:,}")
    print(f"Sector distribution: {sector_counts}")
    print(f"-> {OUTPUT_PATH.name}")
    print()
    print("Next: add g1_galaxy_kinematics to configs/volumes.json")
    print("      domain: galactic, scale_rank: 4")
    print("      Run build_chaos_nulls.py — watch for egg-carton effect")
    print("      If scramble matches real: spatial clustering detected")

if __name__ == "__main__":
    main()