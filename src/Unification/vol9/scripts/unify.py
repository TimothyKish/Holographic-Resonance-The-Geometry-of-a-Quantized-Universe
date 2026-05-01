# ==============================================================================
# SCRIPT: unify.py  (STREAMING REWRITE — memory-safe)
# PURPOSE: Merge all enabled scalarized lakes into unified_master.jsonl
#
# PROBLEM WITH ORIGINAL:
#   Original loaded every lake entirely into RAM before writing.
#   With 2M + 1.8M + 1.84M records, this caused MemoryError on laptops.
#
# FIX:
#   Streaming approach — one record at a time, never holds full lake in RAM.
#   Each lake is read line-by-line and written directly to the output file.
#   Domain statistics (count, mean, min, max) are tracked during the stream.
#   Memory usage is proportional to ONE record, not the full dataset.
#
# OUTPUT FILES (same as original):
#   lakes/unified/unified_master.jsonl    — all records merged
#   lakes/unified/sweep_results.json      — per-domain scalar statistics
#   lakes/unified/pinch_table.json        — domain summary table
#
# AUTHORS: Timothy John Kish & Mondy
# AUDIT STATUS: mondy_verified_2026-04 (streaming rewrite)
# ==============================================================================

import json
import math
import os
from pathlib import Path

# --------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------
SCRIPT_DIR   = Path(__file__).resolve().parent
VOL5_ROOT    = SCRIPT_DIR.parent
CONFIG_PATH  = VOL5_ROOT / "configs" / "volumes.json"
UNIFIED_DIR  = VOL5_ROOT / "lakes" / "unified"
MASTER_PATH  = UNIFIED_DIR / "unified_master.jsonl"
SWEEP_PATH   = UNIFIED_DIR / "sweep_results.json"
PINCH_PATH   = UNIFIED_DIR / "pinch_table.json"

UNIFIED_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------------------
# Load volumes config
# --------------------------------------------------------------------
def load_volumes():
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        cfg = json.load(f)
    return cfg.get("volumes", {})


# --------------------------------------------------------------------
# Locate scalarized file for a given lake name
# --------------------------------------------------------------------
def find_scalarized(name):
    """Find the scalarized JSONL for a lake name."""
    candidates = [
        UNIFIED_DIR / f"{name}_scalarized.jsonl",
        UNIFIED_DIR / f"{name}.jsonl",
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


# --------------------------------------------------------------------
# Streaming unify — core function
# --------------------------------------------------------------------
def unify_streaming(volumes):
    """
    Stream all enabled lakes to unified_master.jsonl.
    Returns domain_stats dict: {domain: {n, sum, sum_sq, min, max, nonzero}}
    Never loads more than one record into memory at a time.
    """
    domain_stats = {}
    total_written = 0
    lakes_processed = 0

    with MASTER_PATH.open("w", encoding="utf-8") as fout:
        for lake_name, cfg in volumes.items():
            if not cfg.get("enabled", False):
                continue

            scalarized = find_scalarized(lake_name)
            if scalarized is None:
                print(f"  [SKIP] {lake_name} — scalarized file not found")
                continue

            domain = cfg.get("domain", lake_name)
            lake_count = 0
            lake_nonzero = 0

            with scalarized.open("r", encoding="utf-8") as fin:
                for line in fin:
                    line = line.strip()
                    if not line:
                        continue

                    # Parse one record at a time — no accumulation
                    rec = json.loads(line)

                    # Extract scalar — try multiple field names for compatibility
                    scalar = (rec.get("scalar_klc")
                              or rec.get("scalar_kls")
                              or rec.get("scalar_invariant")
                              or 0.0)
                    try:
                        scalar = float(scalar)
                    except (TypeError, ValueError):
                        scalar = 0.0
                    if not math.isfinite(scalar):
                        scalar = 0.0

                    # Stamp domain onto record
                    rec["domain"] = domain

                    # Write directly to output — no accumulation
                    fout.write(json.dumps(rec, ensure_ascii=False) + "\n")

                    # Update domain statistics (running totals only)
                    if domain not in domain_stats:
                        domain_stats[domain] = {
                            "n": 0, "nonzero": 0,
                            "sum": 0.0, "sum_sq": 0.0,
                            "min": float("inf"), "max": float("-inf"),
                            "lake_ids": set(),
                        }
                    ds = domain_stats[domain]
                    ds["n"]        += 1
                    ds["lake_ids"].add(lake_name)
                    if scalar != 0.0:
                        ds["nonzero"] += 1
                        ds["sum"]     += scalar
                        ds["sum_sq"]  += scalar * scalar
                        ds["min"]      = min(ds["min"], scalar)
                        ds["max"]      = max(ds["max"], scalar)

                    lake_count   += 1
                    total_written += 1

            lakes_processed += 1
            nonzero = domain_stats.get(domain, {}).get("nonzero", 0)
            print(f"  [{lake_name}] domain={domain}  n={lake_count:,}  "
                  f"nonzero={nonzero:,}")

    print(f"\nTotal records written: {total_written:,}")
    print(f"Lakes processed: {lakes_processed}")
    return domain_stats


# --------------------------------------------------------------------
# Compute sweep results from running stats
# --------------------------------------------------------------------
def build_sweep_results(domain_stats):
    """Build sweep results dict from running statistics."""
    sweep = {}
    for domain, ds in domain_stats.items():
        n       = ds["n"]
        nonzero = ds["nonzero"]
        if nonzero > 0:
            mean = ds["sum"] / nonzero
            var  = (ds["sum_sq"] / nonzero) - (mean * mean)
            std  = math.sqrt(max(0.0, var))
            dmin = ds["min"]
            dmax = ds["max"]
        else:
            mean = std = dmin = dmax = 0.0

        sweep[domain] = {
            "domain":  domain,
            "n":       n,
            "nonzero": nonzero,
            "mean":    round(mean, 6),
            "std":     round(std, 6),
            "min":     round(dmin, 6),
            "max":     round(dmax, 6),
            "lakes":   sorted(ds["lake_ids"]),
        }
    return sweep


# --------------------------------------------------------------------
# Build pinch table summary
# --------------------------------------------------------------------
def build_pinch_table(sweep_results):
    """Build simple pinch table from sweep results."""
    rows = []
    for domain, stats in sorted(sweep_results.items()):
        rows.append({
            "domain":  domain,
            "n":       stats["n"],
            "nonzero": stats["nonzero"],
            "mean":    stats["mean"],
            "std":     stats["std"],
            "min":     stats["min"],
            "max":     stats["max"],
        })
    return {"domains": rows}


# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------
def main():
    print("=" * 60)
    print("Unify — Streaming Mode (memory-safe)")
    print("=" * 60)
    print(f"Config: {CONFIG_PATH}")
    print(f"Output: {MASTER_PATH}")
    print()

    volumes = load_volumes()
    enabled  = [(n, c) for n, c in volumes.items() if c.get("enabled", False)]
    disabled = [(n, c) for n, c in volumes.items() if not c.get("enabled", False)]
    print(f"Volumes: {len(volumes)} total, {len(enabled)} enabled, "
          f"{len(disabled)} disabled")
    print()

    # Stream all lakes to unified master
    domain_stats = unify_streaming(volumes)

    # Build and write sweep results
    sweep = build_sweep_results(domain_stats)
    with SWEEP_PATH.open("w", encoding="utf-8") as f:
        json.dump(sweep, f, indent=2)

    # Build and write pinch table
    pinch = build_pinch_table(sweep)
    with PINCH_PATH.open("w", encoding="utf-8") as f:
        json.dump(pinch, f, indent=2)

    print(f"\nUnified master written: {MASTER_PATH}")
    print(f"Sweep results written:  {SWEEP_PATH}")
    print(f"Pinch table written:    {PINCH_PATH}")
    print()

    # Print domain summary
    print("Domain summary:")
    print(f"  {'Domain':<22} {'n':>10} {'nonzero':>10} {'mean':>8} {'range'}")
    print("  " + "-" * 65)
    for domain, stats in sorted(sweep.items()):
        n    = stats["n"]
        nz   = stats["nonzero"]
        mean = stats["mean"]
        dmin = stats["min"]
        dmax = stats["max"]
        if nz > 0:
            print(f"  {domain:<22} {n:>10,} {nz:>10,} {mean:>8.4f} "
                  f"[{dmin:.4f}, {dmax:.4f}]")
        else:
            print(f"  {domain:<22} {n:>10,} {'(all zeros)':>20}")

if __name__ == "__main__":
    main()