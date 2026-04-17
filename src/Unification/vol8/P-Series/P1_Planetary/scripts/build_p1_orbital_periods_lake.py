# ==============================================================================
# SCRIPT: build_p1_orbital_periods_lake.py
# SERIES: P-Series / P1_Planetary
# DOMAIN: orbital
# SOURCE: NASA Exoplanet Archive — 13,521 confirmed exoplanets
#         Accessed via prior P-Series harvest (P1_Planetary/lake/)
#
# PURPOSE:
#   Build a promoted lake using orbital PERIOD as the scalar, not
#   semi-major axis. Period is a kinematic/temporal quantity (one revolution),
#   while semi-major axis is a positional quantity.
#
#   The velocity-resonance principle established by stellar_kinematic (z=107)
#   and galactic (z=37) predicts that kinematic quantities should show
#   stronger lattice signal than positional ones.
#
#   This is directly testable: the existing P-Series also has semi_major_au.
#   We use period_days as the primary scalar.
#
# SCALAR:
#   scalar = log(period_days + 1) / log(k_geo)
#   Range: ~0.43 (1-day hot Jupiters) to ~6.8 (50,000-day wide orbits)
#
# WHY THIS FILLS THE SCALE GAP:
#   Chemistry scalars end at 1.05
#   Biology_amino starts at 1.79
#   Gap: scalar 1.05-1.67 = orbital periods of 4.5 to 14.2 days
#   Many exoplanets fall in this range — gap filled naturally by the data
#
# NULL MIRROR:
#   NP1_2_NormalizedNull already exists with scrambled period assignments
#   Same planet names, different periods = correct null mirror design
#   Build null from NP1_2_NormalizedNull using same formula
#
# KINEMATIC NOTE:
#   Orbital period is revolution (object goes around a star).
#   Compare to Kepler stellar rotation = spin (star rotates on its axis).
#   Testing both gives: does the lattice prefer revolution or spin or both?
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
P1_DIR       = SCRIPTS_DIR.parent
P_SERIES     = P1_DIR.parent
VOL5_ROOT    = P_SERIES.parent
PROMOTED     = VOL5_ROOT / "lakes" / "inputs_promoted"

RAW_REAL     = P1_DIR / "lake" / "p1_planetary_raw.jsonl"
RAW_NULL     = P_SERIES / "NP1_2_NormalizedNull" / "lake" / "np1_2_normalized_null_raw.jsonl"
OUT_REAL     = PROMOTED / "p1_orbital_periods_promoted.jsonl"
OUT_NULL     = PROMOTED / "np1_orbital_periods_promoted.jsonl"

PERIOD_MAX   = 100000.0  # days — exclude unphysical outliers


def compute_scalar(period_days):
    if period_days is None:
        return None
    try:
        p = float(period_days)
        if p <= 0 or p > PERIOD_MAX:
            return None
        return math.log(p + 1.0) / LOG_K
    except (TypeError, ValueError):
        return None


def build_lake(raw_path, output_path, lake_id, domain, label):
    if not raw_path.exists():
        print(f"  [SKIP] Not found: {raw_path}")
        return 0

    now_ts   = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    total    = 0
    computed = 0
    failed   = 0
    scalars  = []

    with raw_path.open("r", encoding="utf-8") as fin, \
         output_path.open("w", encoding="utf-8") as fout:

        for line in fin:
            line = line.strip()
            if not line:
                continue
            total += 1
            raw = json.loads(line)
            s   = compute_scalar(raw.get("period_days"))

            if s is None or not math.isfinite(s):
                failed += 1
                s = 0.0
            else:
                computed += 1
                scalars.append(s)

            rec = {
                "entity_id":   str(uuid.uuid4()),
                "domain":      domain,
                "volume":      5,
                "lake_id":     lake_id,
                "geometry_payload": {
                    "coordinates":    [],
                    "dimensionality": 0,
                    "geometry_type":  "orbital",
                },
                "scalar_kls":  s,
                "scalar_klc":  s,
                "meta": {
                    "source":          "NASA Exoplanet Archive",
                    "ingest_timestamp": now_ts,
                    "sovereign":        True,
                    "audit_status":     "mondy_verified_2026-04",
                    "scalarization":    "log(period_days + 1) / log(k_geo)",
                    "kinematic_type":   "orbital_revolution",
                    "planet_name":      raw.get("name", ""),
                    "semi_major_au":    raw.get("semi_major_au"),
                    "period_days_raw":  raw.get("period_days"),
                },
                "_raw_payload": raw,
            }
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"[{label}] total={total:,}  computed={computed:,}  failed={failed:,}")
    if scalars:
        print(f"  scalar range: {min(scalars):.4f} to {max(scalars):.4f}  "
              f"mean={sum(scalars)/len(scalars):.4f}")
        # Show gap coverage
        gap_count = sum(1 for s in scalars if 1.05 <= s <= 1.67)
        print(f"  Records filling Gap 1 (1.05-1.67): {gap_count:,}")
    print(f"  -> {output_path.name}")
    return computed


def main():
    print("=" * 60)
    print("P1 Orbital Periods Lake Builder")
    print("=" * 60)
    print(f"k_geo = {K_GEO:.10f}")
    print(f"Scalar: log(period_days + 1) / log(k_geo)")
    print()

    PROMOTED.mkdir(parents=True, exist_ok=True)

    # Real lake
    n_real = build_lake(RAW_REAL, OUT_REAL, "p1_orbital_periods", "orbital", "P1 Real")
    print()

    # Null mirror
    n_null = build_lake(RAW_NULL, OUT_NULL, "np1_orbital_periods", "orbital", "NP1 Null")
    print()

    print("=" * 60)
    print(f"Total promoted: {n_real:,} real + {n_null:,} null")
    print()
    print("Add to configs/volumes.json:")
    print("""
  "p1_orbital_periods": {
    "path": "lakes/inputs_promoted/p1_orbital_periods_promoted.jsonl",
    "enabled": true,
    "domain": "orbital",
    "scale_rank": 2,
    "__scalar__": "log(period_days + 1) / log(k_geo)",
    "__source__": "NASA Exoplanet Archive, 13521 confirmed exoplanets",
    "__note__": "Fills scalar gap 1.05-1.67. Kinematic: orbital revolution period.",
    "__audit__": "mondy_verified_2026-04"
  },
  "np1_orbital_periods": {
    "path": "lakes/inputs_promoted/np1_orbital_periods_promoted.jsonl",
    "enabled": true,
    "domain": "orbital",
    "scale_rank": 0,
    "__note__": "Null mirror for P1 — scrambled period assignments, same planets.",
    "__audit__": "mondy_verified_2026-04"
  },""")
    print()
    print("Next:")
    print("  python scalarize.py && python unify.py")
    print("  python build_chaos_nulls.py && python build_pinch_table.py")
    print()
    print("Watch for:")
    print("  - orbital domain z-score at each modulus")
    print("  - orbital vs np1_orbital (real vs null comparison)")
    print("  - orbital x chemistry cross-domain delta (Gap 1 bridged?)")
    print("  - orbital x biology_amino cross-domain delta")
    print("  - orbital x planetary cross-domain delta (T2 tides overlap?)")


if __name__ == "__main__":
    main()