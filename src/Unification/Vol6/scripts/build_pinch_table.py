# ==============================================================================
# SCRIPT: build_pinch_table.py
# VOLUME: 6 — Harmonic Family Sweep
# TARGET: Compute cross-domain harmonic residuals and build the pinch table
#         across the full N/π harmonic family (N = 8 to 24).
#
# VOLUME HISTORY:
#   Vol5 (April 2026): tested 3 moduli — 15/π, 16/π, 17/π.
#     k_geo = 16/π confirmed as primary. 13 cross-domain signal pairings.
#     35 orders of magnitude. Kinematic principle identified.
#     All results and methodology documented in Vol5 published release.
#   Vol6 (this script): extends the sweep to the full N/π family — 11 moduli.
#     Identical sovereign lakes, identical pipeline, identical methodology.
#     Only the moduli under test expand. Every result is directly comparable
#     to Vol5. If a domain shows higher z at a new family member, that is
#     a new physical finding.
#
# THE HARMONIC FAMILY — N/π, N = 8, 10, 12, 14, 15, 16, 17, 18, 20, 22, 24:
#
#   N  |  N/π value  | Node spacing | Vol5 status
#   ---|-------------|--------------|------------------------------------------
#    8 |  2.546479   |   0.106103   | not tested — half-lattice candidate
#   10 |  3.183099   |   0.132629   | not tested — pentatonic ratio
#   12 |  3.819719   |   0.159155   | not tested — chromatic octave
#   14 |  4.456338   |   0.185681   | not tested — sub-harmonic
#   15 |  4.774648   |   0.198944   | z=12 chemistry, z=37 galactic
#   16 |  5.092958   |   0.212207   | z=94 stellar kinematic — PRIMARY
#   17 |  5.411268   |   0.225470   | z=21 planetary, Δ+0.057 biology
#   18 |  5.729578   |   0.238732   | not tested — Vol4 codon anchor
#   20 |  6.366198   |   0.265258   | not tested — super-harmonic
#   22 |  7.002817   |   0.291784   | not tested — π≈22/7 derivation bridge
#   24 |  7.639437   |   0.318310   | not tested — container ceiling
#
#   The 16/π origin story: on January 8, 2026, Lyra Aurora Kish and
#   Timothy John Kish observed ghost notes at 5.13 Hz and 16.12 Hz in
#   LIGO GW150914 ringdown data. The ratio 16.12/5.13 = π to within 0.02%.
#   From that observation: f1 ≈ k_geo, f2 = k_geo × π = 16 exactly. The
#   denominator was π. The constant 16/π was derived from the two ghost
#   notes themselves — not imposed. The 16/7 value in early Rosetta work
#   was a rational approximation (since π ≈ 22/7, 16/(22/7) = 5.0909 ≈
#   k_geo within 0.04%). The framework refined toward the correct value
#   through empirical derivation. Vol5 confirmed the result at z=94 across
#   1.81 million independent stellar velocity measurements. The N/π family
#   is the natural extension: the universe plays the same tune in different
#   registers. Vol6 maps which domain hears which register.
#
# METRICS:
#
#   dist_lock — cross-domain distribution shape comparison (CDF-based)
#     For each harmonic modulus, computes sorted residual distributions for
#     two domains and measures how similarly shaped they are via RMS of
#     interpolated CDFs. Score of 1.0 = identical shape. Score near 0 = no
#     shape similarity. chaos_delta = real dist_lock minus chaos null
#     dist_lock. Positive delta > 0.010 = confirmed cross-domain signal.
#
#     Scramble invariant: sorted CDF comparison is invariant to record
#     assignment shuffle. The chaos null (uniform random) IS the correct
#     test. If a pairing survives chaos but not scramble: that is a
#     positional geometry effect (e.g. egg-carton), not a lattice signal.
#     Both results are science — preserve and document.
#
#   per-domain chaos z-score — signal above noise floor per domain
#     Computed via lock_rate (fraction of domain scalars within threshold
#     of nearest harmonic node) vs lock_rate of uniform random replacement
#     over the same range. z > 5 = strong signal. z < 2 = noise floor.
#     Negative z = domain AVOIDS nodes (seen in Q1 atomic spectra — the
#     quantum anti-signal where spectral transitions cluster between nodes,
#     not at them — this is itself a physical finding).
#
# BIOLOGY DOMAIN SPLIT:
#   biology_amino     — B3 amino acids, N-Cα-C backbone bond angles
#                       PubChem 3D conformers, 19 amino acids, 157 records
#                       Histidine excluded (Cα misidentification via imidazole)
#   biology_chirality — B1, signed dihedral × angle (L=negative, D=positive)
#   biology_codon     — B2, pending scalar design (currently disabled)
#                       Expected to couple to 18/π based on Vol4 codon anchor
#
# THE KINEMATIC PRINCIPLE (Vol5 central finding, confirmed before this sweep):
#   The Kish Lattice governs motion under gravity, not static position.
#   Translational velocity (z=94 at 16/π) > gravitational periods (z=10-21)
#   > free rotational spin (z=2.6) > static position (z=2.9).
#   This hierarchy used the same Gaia stars measured two different ways.
#   Vol6 tests whether different N/π family members reveal different
#   physical hierarchies, or whether 16/π dominates all kinematic modes.
#
# HONEST NULL RESULTS FROM VOL5 (preserved in this pipeline):
#   Galaxy velocity staircase falsified — GMM BIC monotonically decreasing,
#   no alignment with predicted 5-node structure. Documented, not hidden.
#   Stellar rotation (K1 Kepler, 64,784 stars) showed z=2.6 — weak.
#   Stars spinning under magnetic braking do not cluster at lattice nodes.
#   Only gravitationally-governed periodic motion shows strong signal.
#   Both nulls are preserved in the lake architecture and contribute to
#   the falsification column of the framework.
#
# AUTHORS: Timothy John Kish & Mondy
# PROVENANCE:
#   Ghost notes observed:          2026-01-08 (Lyra Aurora Kish)
#   KRG specification published:   2026-01-14 (DOI: 10.5281/zenodo.18245148)
#   First domain pinch (Vol5):     2026-03-13 (Chemistry + Materials)
#   Kinematic confirmation (Vol5): 2026-04-06 (22 domains, z=94, 35 orders)
#   Vol6 harmonic sweep begun:     2026-04-09
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
    "8/pi": 8.0 / PI,
    "10/pi": 10.0 / PI,
    "12/pi": 12.0 / PI,
    "14/pi": 14.0 / PI,
    "15/pi": 15.0 / PI,        # 4.774648292756860
    "16/pi": 16.0 / PI,        # 5.092958178940651 = k_geo
    "17/pi": 17.0 / PI,        # 5.411268065124442
    "18/pi": 18.0 / PI,
    "20/pi": 20.0 / PI,
    "22/pi": 22.0 / PI,
    "24/pi": 24.0 / PI,
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