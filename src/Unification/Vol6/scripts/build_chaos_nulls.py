# ==============================================================================
# SCRIPT: build_chaos_nulls.py
# VOLUME: 6 — Harmonic Family Sweep
# TARGET: Generate chaos and scramble null lakes for each active domain,
#         evaluated against the full N/π harmonic family (N = 8 to 24).
#
# VOLUME HISTORY:
#   Vol5 (April 2026): tested 3 moduli — 15/π, 16/π, 17/π.
#     Confirmed k_geo = 16/π as primary with z=94 (stellar kinematics),
#     z=37 (galactic), z=21 (planetary), z=12 (chemistry), z=10 (orbital).
#     13 confirmed cross-domain signal pairings. 35 orders of magnitude.
#   Vol6 (this script): extends sweep to the full N/π family — 11 moduli.
#     Same sovereign lakes as Vol5, no new data required.
#     Purpose: discover which physical domains couple to which family member.
#
# THE HARMONIC FAMILY — N/π, N = 8, 10, 12, 14, 15, 16, 17, 18, 20, 22, 24:
#
#   N  |  N/π value  | Physical interpretation
#   ---|-------------|--------------------------------------------------
#    8 |  2.546479   | Half-lattice — sub-galactic structure candidate
#   10 |  3.183099   | Pentatonic ratio — musical fifth territory
#   12 |  3.819719   | Chromatic octave — 12-tone geometric structure
#   14 |  4.456338   | Sub-harmonic approaching k_geo
#   15 |  4.774648   | Chemistry and galactic peak (Vol5 confirmed)
#   16 |  5.092958   | k_geo PRIMARY — kinematic principle (z=94, Vol5)
#   17 |  5.411268   | Biology and life-pocket peak (Vol5 confirmed)
#   18 |  5.729578   | Codon anchor — Vol4 B2 connection (pending test)
#   20 |  6.366198   | Super-harmonic — galaxy cluster scale candidate
#   22 |  7.002817   | π ≈ 22/7 bridge (connects 16/7 derivation to 16/π)
#   24 |  7.639437   | Container cutoff — Heliopause, speed of light limit
#
#   The 16/π origin: on January 8, 2026, Lyra Aurora Kish and Timothy John
#   Kish observed ghost notes at 5.13 Hz and 16.12 Hz in LIGO GW150914
#   ringdown data. The ratio 16.12/5.13 = π (within 0.02%). This led to
#   the identification of k_geo = 16/π as the vacuum stiffness modulus,
#   subsequently confirmed at z=94 across 1.81 million Gaia stellar
#   velocities. The 16/7 early Rosetta work was a rational approximation
#   on the way to the correct transcendental denominator.
#
# NULL LAKE TYPES:
#
#   1. CHAOS NULL (chaos_null_{domain}.jsonl)
#      Uniform random scalars drawn over the same range as the real domain.
#      Destroys both distribution shape and value assignment.
#      This is the absolute noise floor. A real domain signal must beat
#      the chaos null lock rate at every modulus being tested.
#      If real score == chaos: no non-trivial modular structure at that N.
#      If real score >> chaos: the domain couples to that harmonic.
#
#   2. SCRAMBLE NULL (scramble_null_{domain}.jsonl)
#      Shuffles scalar values across records, preserving the exact value
#      distribution but destroying the physical assignment order.
#      If a real signal SURVIVES the scramble but NOT the chaos:
#        -> positional/clustering geometry is driving the result
#        -> "where you are" matters more than "what you are"
#        -> This is IMPORTANT SCIENCE — preserve and document, not a failure
#        -> Examples: asteroid belt clustering, galactic rotation projection,
#           below-horizon polarity (egg-carton effect in S2/G1)
#
# SECTOR NORMALIZATION NOTE:
#   Domains S1 (Gaia parallax), S2 (stellar kinematics), and G1 (galaxy
#   kinematics) apply sector normalization before scalarization to remove
#   the below-horizon positional bias. The egg-carton effect in these
#   domains reflects our position inside the Milky Way disk rather than
#   lattice signal. The normalization is documented and reproducible.
#   Sector-normalized scalars are what arrive here in the unified master.
#
# THE KINEMATIC PRINCIPLE (Vol5 central finding):
#   The Kish Lattice is a gravitational-kinematic geometry. It governs
#   the motion of objects under gravity — their velocities, orbital
#   periods, tidal cycles — not static positions or free rotational spin.
#   Translational velocity (z=94) > gravitational periods (z=10-21) >
#   free spin (z=2.6) > static position (z=2.9).
#   Vol6 tests whether this hierarchy persists across the full N/π family
#   or whether other family members reveal different hierarchies.
#
# OUTPUT: lakes/synthetic/
#   chaos_null_{domain}.jsonl   — absolute floor nulls
#   scramble_null_{domain}.jsonl — assignment scramble nulls
#
# AUTHORS: Timothy John Kish & Mondy
# PROVENANCE:
#   Ghost notes observed:         2026-01-08 (Lyra Aurora Kish)
#   KRG specification published:  2026-01-14 (DOI: 10.5281/zenodo.18245148)
#   First domain pinch (Vol5):    2026-03-13 (Chemistry + Materials)
#   Kinematic confirmation (Vol5):2026-04-06 (22 domains, z=94, 35 orders)
#   Vol6 harmonic sweep begun:    2026-04-09
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
    "8/pi": 8.0 / PI,
    "10/pi": 10.0 / PI,
    "12/pi": 12.0 / PI,
    "14/pi": 14.0 / PI,
    "15/pi": 15.0 / PI,
    "16/pi": 16.0 / PI,
    "17/pi": 17.0 / PI,
    "18/pi": 18.0 / PI,
    "20/pi": 20.0 / PI,
    "22/pi": 22.0 / PI,
    "24/pi": 24.0 / PI,
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