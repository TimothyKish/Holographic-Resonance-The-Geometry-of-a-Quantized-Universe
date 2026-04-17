# ==============================================================================
# SCRIPT: build_chaos_nulls.py
# VOLUME: 7 — Full Harmonic Sweep + Ceiling Bracket + Rosetta Sub-Lattice
# TARGET: Generate chaos and scramble null lakes for each active domain,
#         evaluated against the complete N/π harmonic family (N = 7 to 26).
#
# VOLUME HISTORY:
#   Vol5 (April 6, 2026): tested 3 moduli — 15/π, 16/π, 17/π.
#     Confirmed k_geo = 16/π as primary: z=94 (stellar kinematics),
#     z=37 (galactic), z=21 (planetary), z=12 (chemistry), z=10 (orbital).
#     13 confirmed cross-domain pairings. 35 orders of magnitude.
#     DOI: 10.5281/zenodo.19009634
#   Vol6 (April 10, 2026): extended to 11 moduli — N=8 to N=24.
#     Four major discoveries: molecular register (12/π, z=55 chemistry,
#     z=53 quantum), orbital bridge (22/π, z=45), container boundary
#     (24/π, z=33 planetary, z=23 stellar distance), life register
#     (10/π, z=11 amino acids). 16 confirmed cross-domain pairings.
#     DOI: 10.5281/zenodo.19493376
#   Vol7 (this script): completes the harmonic portrait — 20 moduli.
#     Three new test groups:
#     (a) SUB-HALF-LATTICE: 7/π — the Rosetta origin register.
#         The early 16/7 framework was approximating 16/π via 7 in the
#         denominator. If the Rosetta work was tracking a real physical
#         register, 7/π = 2.228 should show signal in some domain.
#     (b) VALLEY FILLS: 9/π, 11/π, 13/π, 19/π, 21/π, 23/π.
#         Every gap between confirmed Vol6 registers. The most physically
#         motivated: 21/π = 6.685 ≈ 21 × k_geo / π → 21 × k_geo = 106.95 Hz,
#         within 0.14% of the 107.1 Hz lattice refresh rate identified in
#         early recovered framework work. If any domain shows signal at
#         21/π, the 107.1 Hz connection becomes formally testable.
#     (c) CEILING BRACKET: 25/π and 26/π.
#         If 24/π is the genuine container ceiling of the scalar universe,
#         then 25/π = 7.958 should return near-zero signal across all domains.
#         This is the geometric wall made visible in data. 26/π provides the
#         second step above the ceiling for a clean bracket confirmation.
#         A signal-to-null transition from 24/π to 25/π would be the most
#         significant falsification result in the framework's history.
#
# THE COMPLETE HARMONIC FAMILY — N/π, N = 7 to 26:
#
#   N  |  N/π value  | Node spacing | Vol6 status / Vol7 role
#   ---|-------------|--------------|------------------------------------------
#    7 |  2.228169   |   0.092840   | NEW — Rosetta sub-lattice (16/7 origin)
#    8 |  2.546479   |   0.106103   | Vol6: no signal — half-lattice
#    9 |  2.864789   |   0.119366   | NEW — valley below life register
#   10 |  3.183099   |   0.132629   | Vol6 CONFIRMED: life geometry z=11
#   11 |  3.501409   |   0.145892   | NEW — between life(10) and molecular(12)
#   12 |  3.819719   |   0.159155   | Vol6 CONFIRMED: molecular z=55 chem, z=53 QM
#   13 |  4.138029   |   0.172418   | NEW — between molecular(12) and sub-k(14)
#   14 |  4.456338   |   0.185681   | Vol6: moderate
#   15 |  4.774648   |   0.198944   | Vol6 CONFIRMED: galactic z=35
#   16 |  5.092958   |   0.212207   | Vol6 CONFIRMED: kinematic PRIMARY z=87
#   17 |  5.411268   |   0.225470   | Vol6 CONFIRMED: biological timing
#   18 |  5.729578   |   0.238732   | Vol6 CONFIRMED: stellar position z=13
#   19 |  6.047888   |   0.251995   | NEW — between codon(18) and sub-orbital(20)
#   20 |  6.366198   |   0.265258   | Vol6: moderate
#   21 |  6.684508   |   0.278521   | NEW — 21×k_geo=106.95 Hz ≈ 107.1 Hz test
#   22 |  7.002817   |   0.291784   | Vol6 CONFIRMED: orbital z=45
#   23 |  7.321127   |   0.305047   | NEW — one step below container ceiling
#   24 |  7.639437   |   0.318310   | Vol6 CONFIRMED: boundary z=33 planetary
#   25 |  7.957747   |   0.331573   | NEW — MANDATORY NULL above ceiling
#   26 |  8.276057   |   0.344836   | NEW — DEEP NULL two steps above ceiling
#
#   The 16/π origin: on January 8, 2026, Lyra Aurora Kish and Timothy John
#   Kish observed ghost notes at 5.13 Hz and 16.12 Hz in LIGO GW150914
#   ringdown data. The ratio 16.12/5.13 = π (within 0.02%). This led to
#   k_geo = 16/π. The early 16/7 Rosetta work was a rational approximation
#   (since π ≈ 22/7, 16/(22/7) ≈ k_geo within 0.04%). Vol7 tests whether
#   the denominator 7 itself had physical meaning by testing 7/π directly.
#
# NULL LAKE TYPES:
#
#   1. CHAOS NULL (chaos_null_{domain}.jsonl)
#      Uniform random scalars over the same range as the real domain.
#      Absolute noise floor. Real signal must beat this at every modulus.
#
#   2. SCRAMBLE NULL (scramble_null_{domain}.jsonl)
#      Shuffles scalar values across records. Preserves distribution shape,
#      destroys physical assignment. Signal surviving scramble but not chaos
#      indicates positional/clustering geometry — preserve and document.
#
# THE CEILING BRACKET TEST (Vol7 central falsification):
#   Vol6 showed 24/π as the container ceiling: planetary z=33, stellar z=23,
#   cosmology z=9. If this is a genuine geometric boundary:
#     23/π (inside):  should show some signal — approaching the wall
#     24/π (ceiling): strong signal — confirmed Vol6
#     25/π (outside): near-zero — mandatory null
#     26/π (outside): near-zero — deep null confirmation
#   If 25/π returns signal comparable to 24/π, the "ceiling" interpretation
#   is wrong. If 25/π drops to noise floor, the wall is confirmed.
#
# OUTPUT: lakes/synthetic/
#
# AUTHORS: Timothy John Kish & Mondy
# PROVENANCE:
#   Ghost notes observed:          2026-01-08 (Lyra Aurora Kish)
#   KRG specification published:   2026-01-14 (DOI: 10.5281/zenodo.18245148)
#   First domain pinch (Vol5):     2026-03-13 (Chemistry + Materials)
#   Kinematic confirmation (Vol5): 2026-04-06 (22 domains, z=94, 35 orders)
#   Harmonic portrait (Vol6):      2026-04-10 (11 moduli, 4 discoveries)
#   Full sweep + ceiling bracket:  2026-04-11
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
    # --- Sub-lattice Deep Null (new in Vol7) ---
    "5/pi":  5.0  / PI,   # 1.591549 — Rosetta sub-lattice Deep Null
    # --- Sub-lattice Null (new in Vol7) ---
    "6/pi":  6.0  / PI,   # 1.909859 — Rosetta sub-lattice Null
    # --- Sub-half-lattice (new in Vol7) ---
    "7/pi":  7.0  / PI,   # 2.228169 — Rosetta sub-lattice (16/7 origin)
    # --- Half-lattice ---
    "8/pi":  8.0  / PI,   # 2.546479 — Vol6: no signal; chemistry anti-signal
    # --- Valley below life ---
    "9/pi":  9.0  / PI,   # 2.864789 — NEW valley below life register
    # --- Life register (Vol6 confirmed) ---
    "10/pi": 10.0 / PI,   # 3.183099 — life geometry z=11 (amino backbone)
    # --- Valley between life and molecular ---
    "11/pi": 11.0 / PI,   # 3.501409 — NEW valley
    # --- Molecular register (Vol6 confirmed) ---
    "12/pi": 12.0 / PI,   # 3.819719 — chemistry z=55, quantum z=53
    # --- Valley between molecular and sub-k ---
    "13/pi": 13.0 / PI,   # 4.138029 — NEW valley
    # --- Sub-harmonic ---
    "14/pi": 14.0 / PI,   # 4.456338 — moderate in Vol6
    # --- Galactic register (Vol6 confirmed) ---
    "15/pi": 15.0 / PI,   # 4.774648 — galactic vdisp z=35
    # --- Kinematic PRIMARY (Vol5+Vol6 confirmed) ---
    "16/pi": 16.0 / PI,   # 5.092958 — k_geo, stellar v_perp z=87
    # --- Biological timing (Vol6 confirmed) ---
    "17/pi": 17.0 / PI,   # 5.411268 — biology_other, stellar rotation
    # --- Codon anchor / stellar position (Vol6 confirmed) ---
    "18/pi": 18.0 / PI,   # 5.729578 — stellar distance z=13, FRB hint
    # --- Valley between codon and sub-orbital ---
    "19/pi": 19.0 / PI,   # 6.047888 — NEW valley
    # --- Sub-orbital ---
    "20/pi": 20.0 / PI,   # 6.366198 — moderate in Vol6
    # --- 107.1 Hz test (new in Vol7) ---
    "21/pi": 21.0 / PI,   # 6.684508 — 21 x k_geo = 106.95 Hz ≈ 107.1 Hz
    # --- Orbital bridge (Vol6 confirmed) ---
    "22/pi": 22.0 / PI,   # 7.002817 — exoplanet periods z=45
    # --- One step below container ceiling ---
    "23/pi": 23.0 / PI,   # 7.321127 — NEW: approaching the wall
    # --- Container boundary / ceiling (Vol6 confirmed) ---
    "24/pi": 24.0 / PI,   # 7.639437 — planetary z=33, stellar dist z=23
    # --- MANDATORY NULL — one step above ceiling ---
    "25/pi": 25.0 / PI,   # 7.957747 — EXPECTED NULL: scalar universe ends at 24/pi
    # --- DEEP NULL — two steps above ceiling ---
    "26/pi": 26.0 / PI,   # 8.276057 — EXPECTED NULL: confirms wall sharpness
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