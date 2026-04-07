# ==============================================================================
# SCRIPT: build_pinch_table.py
# TARGET: Compute cross-domain harmonic residuals and build pinch table
#
# MODULUS VALUES — EXACT:
#   15/pi = 4.774648292756860
#   16/pi = 5.092958178940651  <- k_geo (central modulus)
#   17/pi = 5.411268065124442
#
#   IMPORTANT: Previous versions used integers 15, 16, 17 as moduli.
#   This was incorrect. All prior pinch scores computed with integer moduli
#   are superseded by this version. The corrected moduli produce honest results.
#
# METRICS:
#   dist_lock — cross-domain distribution shape comparison (CDF-based)
#     Compares sorted residual distributions between two domains.
#     Scramble invariant: shuffling preserves sorted order.
#     Correct null: chaos replacement (uniform random over same range).
#     chaos_delta = real dist_lock minus chaos dist_lock.
#     Positive delta = real distribution shape is non-trivially structured.
#
#   per-domain chaos z-score — how far above noise floor each domain sits
#     Computed via lock_rate (fraction within threshold of nearest node)
#     vs. lock_rate of uniform random replacement over same range.
#
# BIOLOGY DOMAIN SPLIT:
#   biology_amino     — B3, unsigned backbone bond angles (~1.84-1.96 rad)
#   biology_chirality — B1, signed scalars (~+/-1.88 rad, L neg / D pos)
#   biology_codon     — B2, pending scalar design (excluded until ready)
#
# SCRAMBLE NOTE:
#   dist_lock uses sorted CDF comparison — invariant to assignment shuffle.
#   A simple scramble of records will not change dist_lock scores.
#   The chaos replacement null IS the correct test for this metric.
#   If a domain's signal survives scramble but not chaos, this indicates
#   positional/clustering geometry (where-you-are effect). Document, preserve.
#
# AUTHORS: Timothy John Kish & Mondy
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
    "15/pi": 15.0 / PI,        # 4.774648292756860
    "16/pi": 16.0 / PI,        # 5.092958178940651 = k_geo
    "17/pi": 17.0 / PI,        # 5.411268065124442
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
    print(f"Moduli: 15/pi={15/PI:.6f}  16/pi={16/PI:.6f} (k_geo)  17/pi={17/PI:.6f}".center(115))
    print("dist_lock (1=perfect) | Columns: (15/pi, 16/pi, 17/pi) | Δ = real minus chaos null".center(115))
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
    print(f"  {'Domain':<26} {'15/pi':>8} {'16/pi':>8} {'17/pi':>8}  Interpretation")
    print(f"  {'-'*26} {'-'*8} {'-'*8} {'-'*8}  {'-'*25}")
    for dom, scalars in sorted(active_domains.items()):
        zs = []
        for hl in HARMONIC_TARGETS:
            _, _, z = chaos_z_score(scalars, hl, n_trials=100)
            zs.append(z)
        interp = (
            "STRONG signal" if max(zs) > 3.0 else
            "moderate"      if max(zs) > 1.5 else
            "noise floor"
        )
        print(f"  {dom:<26} {zs[0]:>8.2f} {zs[1]:>8.2f} {zs[2]:>8.2f}  {interp}")

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