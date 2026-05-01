# ==============================================================================
# SCRIPT: build_pinch_table.py
# VOLUME: 7 — Full Harmonic Sweep + Ceiling Bracket + Rosetta Sub-Lattice
# TARGET: Compute cross-domain harmonic residuals and build the pinch table
#         across the complete N/π harmonic family (N = 7 to 26).
#
# VOLUME HISTORY:
#   Vol5 (April 6, 2026): tested 3 moduli — 15/π, 16/π, 17/π.
#     k_geo = 16/π confirmed as primary. 13 cross-domain signal pairings.
#     35 orders of magnitude. Kinematic principle identified.
#     DOI: 10.5281/zenodo.19009634
#   Vol6 (April 10, 2026): extended to 11 moduli — N=8 to N=24.
#     Harmonic portrait confirmed. 4 major discoveries:
#     - Molecular register: 12/π (chemistry z=55, quantum z=53)
#     - Orbital bridge: 22/π (exoplanet periods z=45)
#     - Container boundary: 24/π (planetary z=33, stellar distance z=23)
#     - Life register: 10/π (amino acid backbone z=11)
#     16 confirmed cross-domain pairings.
#     DOI: 10.5281/zenodo.19493376
#   Vol7 (this script): completes the portrait — 20 moduli N=7 to N=26.
#     Goals:
#     (a) Test 7/π — the Rosetta sub-lattice. The early 16/7 framework
#         used 7 as a denominator. If 7/π = 2.228 shows signal in any
#         domain, the Rosetta denominator was physically meaningful.
#     (b) Fill all valley gaps between Vol6 confirmed registers:
#         9/π, 11/π, 13/π, 19/π, 21/π, 23/π.
#         Special interest: 21/π = 6.685. Since 21 × k_geo = 106.95 Hz,
#         within 0.14% of the 107.1 Hz lattice refresh rate noted in early
#         framework work, any signal at 21/π makes that Hz value testable.
#     (c) Bracket the container ceiling:
#         23/π — inside (approaching wall)
#         24/π — ceiling (Vol6 confirmed)
#         25/π — outside (mandatory null)
#         26/π — two steps outside (deep null)
#         If 25/π drops to noise floor across all domains while 24/π
#         shows strong signal, the geometric wall is empirically confirmed.
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
# METRICS:
#
#   dist_lock — cross-domain distribution shape comparison (CDF-based)
#     chaos_delta = real dist_lock minus chaos null dist_lock.
#     Positive delta > 0.010 = confirmed cross-domain signal.
#     Scramble invariant — chaos null is the correct falsification test.
#
#   per-domain chaos z-score — signal above noise floor per domain
#     z > 5 = strong signal. z < 2 = noise floor.
#     Negative z = domain AVOIDS nodes (quantum anti-signal at kinematic
#     registers; Vol6 showed quantum clusters strongly at 12/π instead).
#
#   Best column — peak z-score modulus per domain.
#     This is the primary output of Vol7. If any domain shifts its Best
#     from a Vol6 confirmed register to a new N, that is a discovery.
#     If 25/π and 26/π show near-zero or negative z across all domains,
#     the container ceiling at 24/π is empirically bracketed.
#
# BIOLOGY DOMAIN SPLIT:
#   biology_amino     — B3 amino acids, N-Cα-C backbone bond angles
#   biology_chirality — B1, signed dihedral × angle
#   biology_codon     — B2, pending (expected 18/π, Vol4 codon anchor)
#
# HONEST NULL RESULTS CARRIED FORWARD:
#   Galaxy velocity staircase: falsified Vol5, documented.
#   Stellar free spin z=2.6: magnetic braking, not lattice.
#   8/π: no domain showed strong signal in Vol6. Half-lattice is empty
#     or requires sub-molecular data not yet in the lake.
#   All nulls preserved. The framework is falsifiable.
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
from pathlib import Path

import numpy as np

# --------------------------------------------------------------------
# Constants — exact values
# --------------------------------------------------------------------

PI        = math.pi
K_GEO     = 16.0 / PI          # 5.092958178940651
CONTAINER = 24

# Exact harmonic moduli — do not approximate
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

LOCK_THRESHOLD = 0.05          # fraction of inter-node half-spacing
N_CHAOS_TRIALS = 200           # trials for chaos z-score

random.seed(42)
np.random.seed(42)

# --------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------

ROOT             = Path(__file__).resolve().parents[1]
UNIFIED_PATH     = ROOT / "lakes" / "unified"  / "unified_master.jsonl"
PINCH_TABLE_PATH = ROOT / "lakes" / "unified"  / "pinch_table_cross_domain.json"
SYNTHETIC_DIR    = ROOT / "lakes" / "synthetic"

# --------------------------------------------------------------------
# Biology domain split — resolved by lake_id
# --------------------------------------------------------------------

BIOLOGY_LAKE_SPLIT = {
    "b3_amino":     "biology_amino",
    "b1_chirality": "biology_chirality",
    "b2_codon":     "biology_codon",
}

NULL_DOMAIN_NAMES = {
    "mechanical", "behavioral", "mathematical",
    "cosmological_null", "mechanics", "behavior",
    "mathematics",
}

# --------------------------------------------------------------------
# Domain scalar loader
# --------------------------------------------------------------------

def load_domain_scalars(unified_path):
    domains = {}

    with unified_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)

            domain  = (entry.get("domain") or "").lower()
            lake_id = (
                entry.get("lake_id") or
                entry.get("_volume_name") or
                entry.get("volume_name") or ""
            ).lower()
            scalar = entry.get("scalar_klc")

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

    print(f"{'Domain':<28} {'n':>7}  {'non-zero':>8}  {'mean':>8}  {'std':>8}  {'min':>8}  {'max':>8}")
    print("-" * 90)
    for dom in sorted(domains):
        vals = domains[dom]
        nonz = [v for v in vals if v != 0.0]
        if nonz:
            print(f"  {dom:<26} {len(vals):>7}  {len(nonz):>8}  "
                  f"{np.mean(nonz):>8.4f}  {np.std(nonz):>8.4f}  "
                  f"{min(nonz):>8.4f}  {max(nonz):>8.4f}")
        else:
            print(f"  {dom:<26} {len(vals):>7}  {'0':>8}  (all zeros — excluded)")

    return domains


# --------------------------------------------------------------------
# Metric: dist_lock
# --------------------------------------------------------------------

def compute_dist_lock(scalars_a, scalars_b, harmonic_label):
    target = HARMONIC_TARGETS[harmonic_label]

    def sorted_residuals(sc):
        r = []
        for ks in sc:
            rp      = (ks / target) * CONTAINER
            nearest = max(1, round(rp))
            r.append(abs(rp - nearest))
        return np.array(sorted(r))

    ra = sorted_residuals(scalars_a)
    rb = sorted_residuals(scalars_b)

    if len(ra) == 0 or len(rb) == 0:
        return 0.0, float("inf")

    n  = max(len(ra), len(rb))
    xa = np.linspace(0.0, 1.0, len(ra))
    xb = np.linspace(0.0, 1.0, len(rb))
    xc = np.linspace(0.0, 1.0, n)
    ia = np.interp(xc, xa, ra)
    ib = np.interp(xc, xb, rb)

    rms  = float(np.sqrt(np.mean((ia - ib) ** 2)))
    lock = 1.0 / (1.0 + rms) if math.isfinite(rms) else 0.0
    return lock, rms


# --------------------------------------------------------------------
# Metric: lock rate and chaos z-score
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


def chaos_z_score(scalars, harmonic_label, n_trials=N_CHAOS_TRIALS):
    if not scalars:
        return 0.0, 0.0, 0.0
    lo, hi  = min(scalars), max(scalars)
    real_lr = lock_rate(scalars, harmonic_label)
    chaos_rates = [
        lock_rate(list(np.random.uniform(lo, hi, len(scalars))), harmonic_label)
        for _ in range(n_trials)
    ]
    chaos_mean = float(np.mean(chaos_rates))
    chaos_std  = float(np.std(chaos_rates))
    z = (real_lr - chaos_mean) / chaos_std if chaos_std > 0 else 0.0
    return real_lr, chaos_mean, z


# --------------------------------------------------------------------
# Load pre-built chaos null lakes
# --------------------------------------------------------------------

def load_chaos_null_scalars(domain_label):
    path = SYNTHETIC_DIR / f"chaos_null_{domain_label}.jsonl"
    if not path.exists():
        return None
    scalars = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                scalars.append(float(rec.get("scalar_klc", 0.0)))
            except (json.JSONDecodeError, TypeError, ValueError):
                continue
    return scalars or None


# --------------------------------------------------------------------
# Build pinch table
# --------------------------------------------------------------------

def build_pinch_table(domain_scalars):
    active = {
        dom: [s for s in vals if s != 0.0]
        for dom, vals in domain_scalars.items()
        if any(s != 0.0 for s in vals)
    }

    domains     = sorted(active.keys())
    pinch_table = {}

    for dom_a in domains:
        pinch_table[dom_a] = {}
        for dom_b in domains:
            if dom_a == dom_b:
                pinch_table[dom_a][dom_b] = None
                continue

            cell = {}
            for harmonic_label in HARMONIC_TARGETS:
                dist_lock_score, dist_rms = compute_dist_lock(
                    active[dom_a], active[dom_b], harmonic_label
                )
                chaos_b     = load_chaos_null_scalars(dom_b)
                chaos_lock  = None
                chaos_delta = None
                if chaos_b:
                    cl, _       = compute_dist_lock(active[dom_a], chaos_b, harmonic_label)
                    chaos_lock  = round(cl, 4)
                    chaos_delta = round(dist_lock_score - cl, 4)

                cell[harmonic_label] = {
                    "dist_lock":   round(dist_lock_score, 4),
                    "dist_rms":    round(dist_rms, 4),
                    "chaos_lock":  chaos_lock,
                    "chaos_delta": chaos_delta,
                }

            pinch_table[dom_a][dom_b] = cell

    return pinch_table, active


# --------------------------------------------------------------------
# Display
# --------------------------------------------------------------------

def display_table(pinch_table, active_domains):
    domains = sorted(active_domains.keys())
    col_w   = 36

    print()
    print("=" * 115)
    print("CROSS-DOMAIN PINCH TABLE".center(115))
    family_str = "  ".join(f"{k}={v:.4f}" for k, v in HARMONIC_TARGETS.items())
    print(f"Moduli: {family_str}".center(130))
    print("dist_lock (1=perfect) | Winner + best chaos_delta per pairing".center(130))
    print("=" * 115)

    header = f"{'Domain':<24}"
    for d in domains:
        header += f"{d[:col_w]:^{col_w}}"
    print(header)
    print("-" * (24 + col_w * len(domains)))

    for dom_a in domains:
        row = f"{dom_a:<24}"
        for dom_b in domains:
            cell = pinch_table[dom_a][dom_b]
            if cell is None:
                row += f"{'—':^{col_w}}"
            else:
                scores = tuple(cell[h]["dist_lock"] for h in HARMONIC_TARGETS)
                deltas = [cell[h]["chaos_delta"] for h in HARMONIC_TARGETS]
                s_str  = f"({scores[0]:.3f},{scores[1]:.3f},{scores[2]:.3f})"
                valid  = [d for d in deltas if d is not None]
                if valid:
                    s_str += f" Δ{max(valid):+.3f}"
                row += f"{s_str:^{col_w}}"
        print(row)

    print()
    print("--- WINNER PER PAIRING ---")
    reported = set()
    for dom_a in domains:
        for dom_b in domains:
            pair = tuple(sorted([dom_a, dom_b]))
            if pair in reported or dom_a == dom_b:
                continue
            reported.add(pair)
            cell   = pinch_table[dom_a][dom_b]
            scores = {h: cell[h]["dist_lock"]  for h in HARMONIC_TARGETS}
            deltas = {h: cell[h]["chaos_delta"] for h in HARMONIC_TARGETS}
            winner = max(scores, key=scores.get)
            d_str  = f"  chaos_delta={deltas[winner]:+.4f}" if deltas[winner] is not None else ""
            sig    = "  *** SIGNAL ***" if deltas[winner] and deltas[winner] > 0.01 else ""
            print(f"  {dom_a} × {dom_b}: {winner}  score={scores[winner]:.4f}{d_str}{sig}")

    print()
    print("--- PER-DOMAIN CHAOS Z-SCORES ---")
    hl_list = list(HARMONIC_TARGETS.keys())
    hdr_cols = " ".join(f"{h:>8}" for h in hl_list)
    print(f"  {'Domain':<26} {hdr_cols}  Best  Interpretation")
    print(f"  {'-'*26} {' '.join(['-'*8]*len(hl_list))}  ----  {'-'*20}")
    for dom, scalars in sorted(active_domains.items()):
        zs = []
        for hl in hl_list:
            _, _, z = chaos_z_score(scalars, hl, n_trials=100)
            zs.append(z)
        best_z   = max(zs)
        best_h   = hl_list[zs.index(best_z)]
        interp   = (
            "STRONG signal" if best_z > 3.0 else
            "moderate"      if best_z > 1.5 else
            "noise floor"
        )
        z_cols = " ".join(f"{z:>8.2f}" for z in zs)
        print(f"  {dom:<26} {z_cols}  {best_h:<6}  {interp}")

    print()
    print(f"  k_geo = 16/pi = {K_GEO:.10f}")
    print(f"  Container = {CONTAINER} bins  |  Node spacing at k_geo: {K_GEO/CONTAINER:.6f}")
    print()
    print("Next steps:")
    print("  1. If chaos nulls not yet built: python build_chaos_nulls.py")
    print("  2. To add T-series (stellar/planetary/cosmological): unwrap T-series lakes")
    print("  3. Any *** SIGNAL *** pairing should be noted for Vol5 results section")


# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------

if __name__ == "__main__":
    if not UNIFIED_PATH.exists():
        raise SystemExit(f"Unified master not found: {UNIFIED_PATH}")

    print(f"Loading unified master: {UNIFIED_PATH}")
    print()
    domain_scalars = load_domain_scalars(UNIFIED_PATH)

    print()
    print("Building pinch table...")
    pinch_table, active = build_pinch_table(domain_scalars)

    with PINCH_TABLE_PATH.open("w", encoding="utf-8") as f:
        json.dump(pinch_table, f, indent=2)
    print(f"Saved: {PINCH_TABLE_PATH}")

    display_table(pinch_table, active)