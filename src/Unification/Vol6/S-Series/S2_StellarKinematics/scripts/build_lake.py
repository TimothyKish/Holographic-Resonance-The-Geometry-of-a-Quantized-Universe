# ==============================================================================
# SCRIPT: build_s2_stellar_kinematics_lake.py
# SERIES: S-Series / S2_StellarKinematics
# DOMAIN: stellar_kinematic
# SOURCE: Gaia DR3 transverse velocity (v_perp), derived from astrometry
#         1,999,814 stars in 4 sky quadrants (NW/NE/SE/SW)
#
# RAW LAKE: S-Series/S2_StellarKinematics/lake/s2_stellar_kinematics_raw.jsonl
#   Copy from: S-Series/NS6_7/lake/Master_Stellar_Gaia_PHYSICAL.jsonl
#   Field used: val = v_perp (transverse velocity in km/s)
#   Formula: v_perp = 4.74047 * sqrt(mu_a*^2 + mu_d^2) / parallax
#   This was computed by the prior pipeline from Gaia proper motion + parallax.
#   It is NOT a raw Gaia column — it is a derived physical observable.
#   It was NOT computed to fit a hypothesis — it preceded the hypothesis test.
#   (Phoenix confirmed provenance: PHYSICAL lake was built before mixture audit)
#
# WHY v_perp INSTEAD OF dist_pc (S1):
#   S1 GaiaParallax used stellar DISTANCE. Distance is not a resonant quantity
#   — it measures where a star is, not how it moves. Distance showed z=+3.
#
#   v_perp measures how fast each star is moving transversely through space.
#   This is a KINEMATIC quantity, same class as galaxy velocity dispersion.
#   Galaxy vdisp (G1) showed z=+37 — the strongest signal in the framework.
#   The hypothesis: velocity resonates; position does not.
#
# THE 5-NODE MIXTURE STRUCTURE:
#   A prior mixture audit (Phoenix pipeline) found 5 velocity populations:
#     Node 1: 15.61 km/s (local halo/slow disk)
#     Node 2: 27.14 km/s (thin disk)
#     Node 3: 42.79 km/s
#     Node 4: 68.96 km/s
#     Node 5: 108.10 km/s (thick disk / halo)
#   These are NOT confirmed by our pipeline yet. They are a prior observation
#   that will be tested when this lake enters the cross-domain pinch table.
#
# SCALARIZATION:
#   scalar = log(v_perp + 1) / log(k_geo)
#   Consistent with G1 galaxy kinematics scalarization.
#   Filter: v_perp > 0 and v_perp < 1000 km/s
#   (1000 km/s removes unphysical outliers — halo stars rarely exceed 600)
#
# SECTOR NORMALIZATION:
#   Same two-pass approach as G1 and S1.
#   scalar_norm = scalar - sector_mean + global_mean
#   Removes below-horizon spatial bias while preserving kinematic signal.
#
# SETUP:
#   mkdir S-Series\S2_StellarKinematics\lake
#   mkdir S-Series\S2_StellarKinematics\scripts
#   copy S-Series\NS6_7\lake\Master_Stellar_Gaia_PHYSICAL.jsonl
#        S-Series\S2_StellarKinematics\lake\s2_stellar_kinematics_raw.jsonl
#   copy scripts\build_s2_stellar_kinematics_lake.py
#        S-Series\S2_StellarKinematics\scripts\build_lake.py
#
# OUTPUT:
#   vol5/lakes/inputs_promoted/s2_stellar_kinematics_promoted.jsonl
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

# Paths — script lives at S-Series/S2_StellarKinematics/scripts/
SCRIPTS_DIR = Path(__file__).resolve().parent
S2_DIR      = SCRIPTS_DIR.parent
S_SERIES    = S2_DIR.parent
VOL5_ROOT   = S_SERIES.parent
PROMOTED    = VOL5_ROOT / "lakes" / "inputs_promoted"

RAW_INPUT   = S2_DIR / "lake" / "s2_stellar_kinematics_raw.jsonl"
OUTPUT_PATH = PROMOTED / "s2_stellar_kinematics_promoted.jsonl"

VPERP_MIN   = 0.0
VPERP_MAX   = 1000.0   # km/s — halo stars rarely exceed 600


def compute_scalar(val):
    """
    scalar = log(v_perp + 1) / log(k_geo)
    val: transverse velocity in km/s (the 'val' field from PHYSICAL lake)
    """
    if val is None:
        return None
    try:
        v = float(val)
        if v <= VPERP_MIN or v > VPERP_MAX:
            return None
        return math.log(v + 1.0) / LOG_K
    except (TypeError, ValueError):
        return None


def main():
    print("=" * 60)
    print("S2 Stellar Kinematics Lake Builder")
    print("=" * 60)
    print(f"k_geo = {K_GEO:.10f}")
    print(f"Input:  {RAW_INPUT}")
    print(f"Output: {OUTPUT_PATH}")
    print(f"Scalar: log(v_perp + 1) / log(k_geo)")
    print(f"Filter: 0 < v_perp <= {VPERP_MAX} km/s")
    print()

    if not RAW_INPUT.exists():
        raise SystemExit(
            f"Raw lake not found: {RAW_INPUT}\n\n"
            f"Setup steps:\n"
            f"  1. mkdir S-Series\\S2_StellarKinematics\\lake\n"
            f"  2. copy S-Series\\NS6_7\\lake\\Master_Stellar_Gaia_PHYSICAL.jsonl\n"
            f"          S-Series\\S2_StellarKinematics\\lake\\s2_stellar_kinematics_raw.jsonl\n"
            f"  3. Run this script from its scripts\\ folder"
        )

    PROMOTED.mkdir(parents=True, exist_ok=True)
    now_ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    # Pass 1: compute raw scalars and sector means
    print("Pass 1: computing raw scalars and sector means...")
    raw_records   = []
    sector_sums   = defaultdict(float)
    sector_counts = defaultdict(int)
    total    = 0
    filtered = 0
    failed   = 0

    with RAW_INPUT.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            rec  = json.loads(line)
            val  = rec.get("val")
            s    = compute_scalar(val)

            if s is None:
                if val is not None:
                    filtered += 1
                else:
                    failed += 1
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
          f"filtered={filtered:,}  failed={failed:,}")
    print(f"Global mean scalar: {global_mean:.4f}")
    print("Sector means (raw scalar, before normalization):")
    for sec, mean in sorted(sector_means.items()):
        n = sector_counts[sec]
        print(f"  {sec}: mean={mean:.4f}  (n={n:,})")

    # Pass 2: apply sector normalization and write
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
                "domain":      "stellar_kinematic",
                "volume":      5,
                "lake_id":     "s2_stellar_kinematics",
                "geometry_payload": {
                    "coordinates":    [
                        rec.get("ra", rec.get("RA", 0)),
                        rec.get("dec", rec.get("DEC", 0))
                    ],
                    "dimensionality": 2,
                    "geometry_type":  "sky_position",
                },
                "scalar_kls":  s_norm,
                "scalar_klc":  s_norm,
                "meta": {
                    "source": (
                        "Gaia DR3 transverse velocity v_perp (km/s), "
                        "derived from proper motion + parallax via "
                        "v_perp = 4.74047 * sqrt(mu_a*^2 + mu_d^2) / parallax"
                    ),
                    "ingest_timestamp":  now_ts,
                    "sovereign":         True,
                    "audit_status":      "mondy_verified_2026-04",
                    "scalarization":     "log(v_perp + 1) / log(k_geo)",
                    "sector_normalized": True,
                    "scalar_raw":        round(s_raw, 6),
                    "sector":            sector,
                    "sector_mean":       round(sector_means.get(sector, global_mean), 6),
                    "global_mean":       round(global_mean, 6),
                    "val_raw_kms":       float(rec.get("val", 0)),
                    "provenance_note": (
                        "val field was computed before hypothesis testing. "
                        "PHYSICAL lake preceded mixture audit per Phoenix audit trail."
                    ),
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
    print("Next steps:")
    print("  1. Add s2_stellar_kinematics to configs/volumes.json")
    print("     domain: stellar_kinematic, scale_rank: 3")
    print("  2. python scalarize.py")
    print("  3. python unify.py")
    print("  4. python build_chaos_nulls.py")
    print("  5. python build_pinch_table.py")
    print()
    print("Watch for:")
    print("  - s2 z-score vs s1 stellar z-score (expect s2 >> s1)")
    print("  - s2 × g1_galactic cross-domain delta (both kinematic)")
    print("  - s2 × planetary cross-domain delta (velocity vs tidal resonance)")


if __name__ == "__main__":
    main()