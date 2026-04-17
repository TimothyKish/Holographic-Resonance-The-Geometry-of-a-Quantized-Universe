# ==============================================================================
# SCRIPT: unwrap_t_series.py
# TARGET: Unwrap double-promoted T-series lakes and compute scalar_kls/klc
#
# PROBLEM BEING FIXED:
#   T-series promoted files were promoted twice (double-wrapped).
#   The real data sits at: record -> meta.source_row -> meta.source_row -> raw_payload
#   The outer scalar_kls/klc are 0.0 because scalarize.py looks at _raw_payload
#   which is empty {} in all T-series records.
#
# SERIES HANDLED:
#   T1 Biological  — Spellman 1998 yeast cell cycle
#     field:  log_dt (ln of interval in minutes, already log-normalized)
#     scalar: log_dt directly
#     range:  ~1.79-2.99 (ln of 6-20 min cadences)
#
#   T2 Planetary   — NOAA CO-OPS tide intervals, San Francisco
#     field:  interval_hours (high/low tide half-cycle duration)
#     scalar: log(interval_hours + 1) / log(k_geo)
#     range:  ~0.85-1.41 (3-9 hour tide intervals)
#     note:   Tidal cycle is lunar-gravitational — planetary temporal domain
#
#   T4 Cosmological — SDSS DR16 authentic redshift + distance proxy
#     field:  d_proxy (comoving distance in Mpc)
#     scalar: log(d_proxy + 1) / log(k_geo)
#     range:  ~2.32-4.92 (z=0.01 to z=0.70)
#     note:   Directly comparable to FRB scalars (both log-distance proxies)
#
#   N4 Cosmological — Scrambled authentic temporal data (null mirror for T4)
#     field:  d_proxy_scrambled (real z, shuffled distances)
#     scalar: log(d_proxy_scrambled + 1) / log(k_geo)
#     note:   This IS a null lake — signal should be flat vs T4
#             Keep same scalarization as T4 for direct comparison
#
# T3 STELLAR — HELD, NOT PROCESSED:
#   T3 is labeled 'stellar' but source is 'CHIME/FRB temporal intervals'
#   First record shows period_days = 0.0 which indicates unmeasured periods
#   Requires inspection of full lake before scalarization can be designed
#   See: lakes/inputs_promoted/t3_stellar_promoted.jsonl
#
# OUTPUT:
#   Overwrites the promoted files in lakes/inputs_promoted/ with
#   correct scalar_kls and scalar_klc values.
#   The scalarize.py passthrough will then preserve these values.
#
# AUTHORS: Timothy John Kish & Mondy
# AUDIT STATUS: mondy_verified_2026-04
# ==============================================================================

import json
import math
import uuid
from datetime import datetime, timezone
from pathlib import Path

# --------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------

PI    = math.pi
K_GEO = 16.0 / PI       # 5.092958...
LOG_K = math.log(K_GEO)

ROOT       = Path(__file__).resolve().parents[1]
PROMOTED   = ROOT / "lakes" / "inputs_promoted"

# --------------------------------------------------------------------
# Navigation helper — unwrap double-promoted record
# --------------------------------------------------------------------

def get_inner_payload(rec):
    """
    Navigate the double-wrap structure to the actual data.
    Path: record -> meta.source_row -> meta.source_row -> raw_payload
    Returns the innermost source_row dict, or None if structure absent.
    """
    try:
        layer1 = rec.get("meta", {}).get("source_row", {})
        layer2 = layer1.get("meta", {}).get("source_row", {})
        return layer2
    except (AttributeError, TypeError):
        return None


def get_raw_payload(inner):
    """Extract raw_payload from inner source_row."""
    if inner is None:
        return {}
    return inner.get("raw_payload") or inner.get("_raw_payload") or {}


# --------------------------------------------------------------------
# Scalar functions — one per series
# --------------------------------------------------------------------

def scalar_t1(inner):
    """
    T1 Biological: log_dt is ln(cell cycle interval in minutes).
    Already log-normalized. Use directly.
    """
    log_dt = inner.get("log_dt")
    if log_dt is None:
        return None
    try:
        return float(log_dt)
    except (TypeError, ValueError):
        return None


def scalar_t2(inner):
    """
    T2 Planetary: tide interval in hours.
    scalar = log(interval_hours + 1) / log(k_geo)
    Consistent with FRB log-k_geo scalarization.
    """
    raw = get_raw_payload(inner)
    hours = raw.get("interval_hours")
    if hours is None:
        return None
    try:
        h = float(hours)
        if h <= 0:
            return None
        return math.log(h + 1.0) / LOG_K
    except (TypeError, ValueError):
        return None


def scalar_t4(inner):
    """
    T4 Cosmological: real SDSS distance proxy in Mpc.
    scalar = log(d_proxy + 1) / log(k_geo)
    Directly comparable to FRB DM scalar (both log-distance proxies).
    """
    raw = get_raw_payload(inner)
    d = raw.get("d_proxy")
    if d is None:
        return None
    try:
        d_val = float(d)
        if d_val < 0:
            return None
        return math.log(d_val + 1.0) / LOG_K
    except (TypeError, ValueError):
        return None


def scalar_n4(inner):
    """
    N4 Cosmological null: scrambled distance proxy.
    Same formula as T4 for direct comparison.
    Signal should be flat relative to T4.
    """
    raw = get_raw_payload(inner)
    d = raw.get("d_proxy_scrambled")
    if d is None:
        return None
    try:
        d_val = float(d)
        if d_val < 0:
            return None
        return math.log(d_val + 1.0) / LOG_K
    except (TypeError, ValueError):
        return None


# --------------------------------------------------------------------
# Lake processor
# --------------------------------------------------------------------

def process_lake(filename, scalar_fn, series_label, scalarization_note):
    """
    Read promoted JSONL, compute scalar for each record, write back.
    Preserves all existing fields, updates scalar_kls and scalar_klc.
    """
    input_path  = PROMOTED / filename
    if not input_path.exists():
        print(f"[WARN] Not found, skipping: {input_path}")
        return

    now_ts   = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    records  = []
    total    = 0
    computed = 0
    failed   = 0
    zero_val = 0

    with input_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            rec   = json.loads(line)
            inner = get_inner_payload(rec)
            s     = scalar_fn(inner) if inner else None

            if s is not None and math.isfinite(s):
                rec["scalar_kls"] = s
                rec["scalar_klc"] = s
                # Also stamp into meta for traceability
                rec.setdefault("meta", {})
                rec["meta"]["scalar_computed_by"] = "unwrap_t_series.py"
                rec["meta"]["scalarization"]      = scalarization_note
                rec["meta"]["audit_status"]       = "mondy_verified_2026-04"
                rec["meta"]["unwrap_timestamp"]   = now_ts
                computed += 1
                if s == 0.0:
                    zero_val += 1
            else:
                failed += 1

            records.append(rec)

    # Write back in place
    with input_path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    scalars = [r["scalar_kls"] for r in records if r.get("scalar_kls", 0.0) != 0.0]
    mean_s  = sum(scalars) / len(scalars) if scalars else 0.0
    min_s   = min(scalars) if scalars else 0.0
    max_s   = max(scalars) if scalars else 0.0

    print(f"[{series_label}]  total={total}  computed={computed}  "
          f"failed={failed}  zero_val={zero_val}")
    if scalars:
        print(f"  scalar range: {min_s:.4f} to {max_s:.4f}  mean={mean_s:.4f}")
    print(f"  -> {input_path.name}  (overwritten in place)")


# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------

def main():
    print("=" * 65)
    print("T-Series Unwrap and Scalarization")
    print("=" * 65)
    print(f"k_geo = 16/pi = {K_GEO:.10f}")
    print()

    # T1 Biological — Spellman 1998 yeast cell cycle
    process_lake(
        "t1_biological_promoted.jsonl",
        scalar_t1,
        "T1 Biological",
        "log_dt extracted directly (ln of cell cycle interval in minutes)"
    )
    print()

    # T2 Planetary — NOAA tide intervals
    process_lake(
        "t2_planetary_promoted.jsonl",
        scalar_t2,
        "T2 Planetary",
        "log(interval_hours + 1) / log(k_geo) — NOAA tidal half-cycle duration"
    )
    print()

    # T4 Cosmological — SDSS real distances
    process_lake(
        "t4_cosmological_promoted.jsonl",
        scalar_t4,
        "T4 Cosmological",
        "log(d_proxy + 1) / log(k_geo) — SDSS DR16 comoving distance (Mpc)"
    )
    print()

    # N4 Cosmological null — scrambled distances
    process_lake(
        "n4_cosmological_promoted.jsonl",
        scalar_n4,
        "N4 Cosmological (null)",
        "log(d_proxy_scrambled + 1) / log(k_geo) — same formula as T4, scrambled d"
    )
    print()

    print("=" * 65)
    print("T3 Stellar — HELD, NOT PROCESSED")
    print("  Reason: domain labeled 'stellar' but source is CHIME/FRB temporal data")
    print("  First record shows period_days = 0.0 (unmeasured repeater periods)")
    print("  Action required: inspect full lake before designing scalar")
    print(f"  File: {PROMOTED / 't3_stellar_promoted.jsonl'}")
    print()
    print("Next steps:")
    print("  1. python scalarize.py   (fallback will preserve new scalars)")
    print("  2. python unify.py")
    print("  3. python build_chaos_nulls.py")
    print("  4. python build_pinch_table.py")
    print()
    print("Expected new active domains: planetary, biology(T1), cosmology(T4)")
    print("N4 null should show flat signal vs T4 — validates the scramble design")


if __name__ == "__main__":
    main()