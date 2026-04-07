# ==============================================================================
# SCRIPT: build_chaos_nulls.py
# TARGET: Generate chaos and scramble null lakes for each active domain
#
# MODULUS VALUES — EXACT (matches build_pinch_table.py):
#   15/pi = 4.774648292756860
#   16/pi = 5.092958178940651  <- k_geo
#   17/pi = 5.411268065124442
#
# NULL LAKE TYPES:
#
#   1. CHAOS NULL (chaos_null_{domain}.jsonl)
#      Uniform random over same scalar range as real domain.
#      Destroys both distribution shape and assignment.
#      Absolute noise floor — real signal must beat this.
#      If real score == chaos: no non-trivial modular structure.
#
#   2. SCRAMBLE NULL (scramble_null_{domain}.jsonl)
#      Shuffles scalar values across records.
#      Preserves exact value distribution, destroys assignment.
#      If real signal SURVIVES this scramble:
#        -> positional/clustering geometry drives the result
#        -> "where you are matters more than what you are"
#        -> IMPORTANT SCIENCE — preserve and document, not a failure
#        -> Examples: asteroid belt clustering, Oort cloud objects,
#           galactic polarity below horizon (egg-carton effect)
#
# NORMALIZATION NOTE:
#   For domains with known polarity asymmetry (galactic, planetary),
#   check for below-horizon systematic before interpreting scramble results.
#   The egg-carton effect survives scramble because it is positional.
#
# OUTPUT: lakes/synthetic/
#
# AUTHORS: Timothy John Kish & Mondy
# AUDIT STATUS: mondy_verified_2026-04
# ==============================================================================

import json
import math
import random
import uuid
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

PI    = math.pi
K_GEO = 16.0 / PI

HARMONIC_TARGETS = {
    "15/pi": 15.0 / PI,
    "16/pi": 16.0 / PI,
    "17/pi": 17.0 / PI,
}

CONTAINER      = 24
LOCK_THRESHOLD = 0.05

ROOT      = Path(__file__).resolve().parents[1]
UNIFIED   = ROOT / "lakes" / "unified" / "unified_master.jsonl"
SYNTHETIC = ROOT / "lakes" / "synthetic"
SYNTHETIC.mkdir(parents=True, exist_ok=True)

# Biology sub-domain resolution
BIOLOGY_LAKE_SPLIT = {
    "b3_amino":     "biology_amino",
    "b1_chirality": "biology_chirality",
    "b2_codon":     "biology_codon",
}

NULL_DOMAIN_NAMES = {
    "mechanical", "behavioral", "mathematical",
    "cosmological_null", "mechanics", "behavior", "mathematics",
}

# --------------------------------------------------------------------
# Load unified master
# --------------------------------------------------------------------

def load_domain_scalars():
    domains = {}
    with UNIFIED.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec    = json.loads(line)
            domain = (rec.get("domain") or "").lower()
            lake_id = (rec.get("lake_id") or rec.get("_volume_name") or "").lower()
            scalar = rec.get("scalar_klc")
            if scalar is None:
                continue
            try:
                s = float(scalar)
            except (TypeError, ValueError):
                continue

            if domain == "biology":
                label = None
                for key, slot in BIOLOGY_LAKE_SPLIT.items():
                    if key in lake_id:
                        label = slot
                        break
                label = label or "biology_other"
            elif domain in NULL_DOMAIN_NAMES:
                label = f"null_{domain}"
            elif domain == "astrophysics":
                label = "frb"
            elif domain == "cosmology":
                label = "null_cosmological" if ("n4" in lake_id or "null" in lake_id) else "cosmology"
            else:
                label = domain

            domains.setdefault(label, []).append(s)

    return domains


# --------------------------------------------------------------------
# Lock rate (node-relative, matches build_pinch_table)
# --------------------------------------------------------------------

def lock_rate(scalars, harmonic_label, threshold=LOCK_THRESHOLD):
    if not scalars:
        return 0.0
    target = HARMONIC_TARGETS[harmonic_label]
    locked = 0
    for s in scalars:
        rp      = (s / target) * CONTAINER
        nearest = max(1, round(rp))
        if abs(rp - nearest) < threshold:
            locked += 1
    return locked / len(scalars)


# --------------------------------------------------------------------
# Null lake builders
# --------------------------------------------------------------------

def build_chaos_null(domain_label, scalars):
    """Uniform random over same range. Absolute noise floor."""
    lo      = min(scalars)
    hi      = max(scalars)
    n       = len(scalars)
    now_ts  = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    records = []
    for _ in range(n):
        s = random.uniform(lo, hi)
        records.append({
            "entity_id":   str(uuid.uuid4()),
            "domain":      f"null_{domain_label}",
            "volume":      5,
            "lake_id":     f"chaos_null_{domain_label}",
            "geometry_payload": {
                "coordinates":    [],
                "dimensionality": 0,
                "geometry_type":  "chaos_uniform",
            },
            "scalar_kls": s,
            "scalar_klc": s,
            "meta": {
                "source":           f"Chaos null for {domain_label}",
                "ingest_timestamp": now_ts,
                "sovereign":        False,
                "null_type":        "chaos_uniform",
                "null_range":       [lo, hi],
                "null_n":           n,
                "real_domain":      domain_label,
                "audit_note": (
                    "Absolute floor null. Uniform random over real scalar range. "
                    "Real signal must beat this or no modular structure is present."
                ),
            },
        })
    return records


def build_scramble_null(domain_label, scalars):
    """
    Shuffled assignment null. Preserves distribution, destroys pairing.
    Signal surviving this scramble = positional/clustering geometry.
    Document this finding — do not discard it.
    """
    shuffled = scalars[:]
    random.shuffle(shuffled)
    now_ts   = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    records  = []
    for s in shuffled:
        records.append({
            "entity_id":   str(uuid.uuid4()),
            "domain":      f"null_{domain_label}",
            "volume":      5,
            "lake_id":     f"scramble_null_{domain_label}",
            "geometry_payload": {
                "coordinates":    [],
                "dimensionality": 0,
                "geometry_type":  "scrambled_assignment",
            },
            "scalar_kls": s,
            "scalar_klc": s,
            "meta": {
                "source":           f"Scramble null for {domain_label}",
                "ingest_timestamp": now_ts,
                "sovereign":        False,
                "null_type":        "scramble_assignment",
                "real_domain":      domain_label,
                "audit_note": (
                    "Assignment scramble. Preserves distribution shape, destroys pairing. "
                    "Signal surviving this scramble indicates positional/clustering geometry. "
                    "This is a scientific observation to preserve, not a failure."
                ),
            },
        })
    return records


# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------

def main():
    random.seed(42)
    np.random.seed(42)

    if not UNIFIED.exists():
        raise SystemExit(f"Unified master not found: {UNIFIED}")

    print(f"k_geo = 16/pi = {K_GEO:.10f}")
    print(f"Moduli: " + "  ".join(f"{k}={v:.6f}" for k, v in HARMONIC_TARGETS.items()))
    print()
    print("Loading unified master...")
    domains = load_domain_scalars()

    print(f"\nFound {len(domains)} domain slots:")
    for label in sorted(domains):
        vals = [s for s in domains[label] if s != 0.0]
        if vals:
            print(f"  {label:<28} n={len(vals):6d}  "
                  f"mean={np.mean(vals):.4f}  "
                  f"range=[{min(vals):.4f}, {max(vals):.4f}]")
        else:
            print(f"  {label:<28} n={len(domains[label]):6d}  (all zeros)")

    print()
    print("Building null lakes...")
    print()

    for domain_label in sorted(domains):
        vals = [s for s in domains[domain_label] if s != 0.0]
        if not vals:
            print(f"[SKIP] {domain_label} — all zeros")
            continue

        # Build nulls
        chaos    = build_chaos_null(domain_label, vals)
        scramble = build_scramble_null(domain_label, vals)

        # Write
        chaos_path    = SYNTHETIC / f"chaos_null_{domain_label}.jsonl"
        scramble_path = SYNTHETIC / f"scramble_null_{domain_label}.jsonl"

        with chaos_path.open("w", encoding="utf-8") as f:
            for rec in chaos:
                f.write(json.dumps(rec) + "\n")

        with scramble_path.open("w", encoding="utf-8") as f:
            for rec in scramble:
                f.write(json.dumps(rec) + "\n")

        # Diagnostics with correct moduli
        print(f"[{domain_label}]  n={len(vals)}")
        for hl, target in HARMONIC_TARGETS.items():
            rl = lock_rate(vals, hl)
            cl = lock_rate([r["scalar_klc"] for r in chaos], hl)
            delta = rl - cl
            signal = " ← above chaos" if delta > 0.005 else ""
            print(f"  {hl}: real={rl:.4f}  chaos={cl:.4f}  delta={delta:+.4f}{signal}")
        print(f"  -> {chaos_path.name}")
        print(f"  -> {scramble_path.name}")
        print()

    print(f"All null lakes written to: {SYNTHETIC}")
    print()
    print("Next steps:")
    print("  1. python build_pinch_table.py")
    print("  2. Check chaos_delta column — positive values indicate signal above noise floor")
    print("  3. Any domain where real lock_rate <= chaos floor: no modular structure")
    print("  4. Any domain where scramble matches real but chaos does not:")
    print("     -> positional clustering effect — document in Vol5 methodology")

if __name__ == "__main__":
    main()