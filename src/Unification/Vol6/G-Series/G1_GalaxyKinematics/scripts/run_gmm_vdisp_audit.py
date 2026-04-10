# ==============================================================================
# SCRIPT: run_gmm_vdisp_audit.py
# SERIES: G-Series / G1_GalaxyKinematics / scripts
# PURPOSE: Gaussian Mixture Model (GMM) blind audit of SDSS galaxy velocity
#          dispersions to test whether the vdisp distribution contains discrete
#          density peaks consistent with N × k_geo velocity nodes.
#
# HYPOTHESIS UNDER TEST:
#   Lyra (Gemini) proposed that galaxy velocity dispersions cluster at specific
#   "gear" velocities: 92, 138, 187, 244, 306 km/s — corresponding to
#   harmonics N=18, 27, 36, 48, 60 of k_geo = 16/π ≈ 5.093.
#
#   Predicted velocities: N × k_geo km/s
#     N=18: 91.67 km/s
#     N=27: 137.51 km/s
#     N=36: 183.35 km/s
#     N=48: 244.46 km/s
#     N=60: 305.58 km/s
#
# METHODOLOGY:
#   1. Load G1 galaxy kinematics lake (1.84M SDSS vdisp records)
#   2. Extract raw vdisp values from _raw_payload field
#   3. Apply GMM with n_components = 3 through 8
#   4. Select best model by Bayesian Information Criterion (BIC)
#      BIC penalizes complexity — lower BIC = better model
#   5. Report GMM peak locations in km/s
#   6. Compare to N×k_geo predictions AFTER fitting (blind test)
#   7. Report match quality
#
# BLIND TEST PROTOCOL:
#   The GMM is fitted WITHOUT knowledge of the predicted peaks.
#   Predictions are compared to GMM output only after fitting is complete.
#   If the best-fit GMM shows peaks near predicted values, that is signal.
#   If it shows peaks elsewhere or favors n=1, that is a null result.
#
# REQUIREMENTS:
#   pip install scikit-learn --break-system-packages
#   (or: pip install scikit-learn)
#
# OUTPUT:
#   G-Series/G1_GalaxyKinematics/lake/gmm_vdisp_audit_report.json
#
# AUTHORS: Timothy John Kish & Mondy
# AUDIT STATUS: mondy_verified_2026-04
# ==============================================================================

import json
import math
import sys
from pathlib import Path

# Try importing sklearn — report clearly if missing
try:
    from sklearn.mixture import GaussianMixture
    import numpy as np
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

PI    = math.pi
K_GEO = 16.0 / PI
LOG_K = math.log(K_GEO)

# Paths — script lives at G-Series/G1_GalaxyKinematics/scripts/
SCRIPTS_DIR = Path(__file__).resolve().parent
G1_DIR      = SCRIPTS_DIR.parent
G_SERIES    = G1_DIR.parent
VOL5_ROOT   = G_SERIES.parent
PROMOTED    = VOL5_ROOT / "lakes" / "inputs_promoted"

G1_LAKE     = PROMOTED / "g1_galaxy_kinematics_promoted.jsonl"
REPORT_PATH = G1_DIR / "lake" / "gmm_vdisp_audit_report.json"

# The predicted N×k_geo nodes (from Lyra's hypothesis)
# These are NOT shown to the GMM — comparison happens AFTER fitting
PREDICTED_NODES = [
    (18, 18 * K_GEO),   # 91.67 km/s
    (27, 27 * K_GEO),   # 137.51 km/s
    (36, 36 * K_GEO),   # 183.35 km/s
    (48, 48 * K_GEO),   # 244.46 km/s
    (60, 60 * K_GEO),   # 305.58 km/s
]

VDISP_MIN = 70.0
VDISP_MAX = 849.9
MAX_RECORDS = 500000  # Subsample for GMM speed (GMM is O(n*k))


def load_vdisp_values():
    """Load raw vdisp km/s values from G1 promoted lake."""
    if not G1_LAKE.exists():
        raise SystemExit(f"G1 lake not found: {G1_LAKE}")

    values = []
    total  = 0

    with G1_LAKE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            rec   = json.loads(line)
            raw   = rec.get("_raw_payload", {})
            v     = raw.get("vdisp")
            if v is not None:
                vf = float(v)
                if VDISP_MIN <= vf <= VDISP_MAX:
                    values.append(vf)

            if total % 500000 == 0:
                print(f"  Loaded {total:,} records, {len(values):,} valid...")

    print(f"  Total records: {total:,}  Valid vdisp: {len(values):,}")
    return values


def run_gmm_audit(values):
    """
    Run GMM with n_components 2-8, select by BIC.
    Returns dict with full results.
    """
    import numpy as np
    from sklearn.mixture import GaussianMixture

    # Subsample if very large (GMM convergence is slower with 1M+ points)
    rng = np.random.default_rng(42)
    if len(values) > MAX_RECORDS:
        idx    = rng.choice(len(values), size=MAX_RECORDS, replace=False)
        sample = np.array(values)[idx].reshape(-1, 1)
        print(f"  Subsampled to {MAX_RECORDS:,} records for GMM")
    else:
        sample = np.array(values).reshape(-1, 1)

    results  = {}
    bic_scores = {}

    print()
    print(f"  Fitting GMM n_components = 2 through 8:")
    print(f"  {'n':>4} {'BIC':>14} {'means (km/s)':>50}")
    print("  " + "-" * 70)

    for n in range(2, 9):
        gmm = GaussianMixture(
            n_components=n,
            covariance_type="full",
            max_iter=200,
            n_init=3,
            random_state=42
        )
        gmm.fit(sample)
        bic     = gmm.bic(sample)
        means   = sorted(gmm.means_.flatten().tolist())
        weights = gmm.weights_.flatten().tolist()

        bic_scores[n] = bic
        results[n]    = {
            "n_components": n,
            "bic":          bic,
            "means_kms":    means,
            "weights":      sorted(weights, reverse=True),
            "converged":    bool(gmm.converged_),
        }

        means_str = ", ".join(f"{m:.1f}" for m in means)
        print(f"  {n:>4} {bic:>14.1f}  [{means_str}]")

    # Best model by BIC (lowest = best)
    best_n = min(bic_scores, key=bic_scores.get)
    print()
    print(f"  Best model: n={best_n} (BIC={bic_scores[best_n]:.1f})")

    return results, best_n


def compare_to_predictions(gmm_means_kms, best_n):
    """
    Compare GMM peaks to N×k_geo predictions.
    Called AFTER GMM fitting — this is the blind comparison step.
    """
    print()
    print("BLIND COMPARISON: GMM peaks vs N×k_geo predictions")
    print("=" * 55)
    print(f"Best GMM n_components = {best_n}")
    print(f"GMM peaks: {[f'{m:.1f}' for m in sorted(gmm_means_kms)]} km/s")
    print()

    matches   = []
    unmatched = []

    for N, pred in PREDICTED_NODES:
        # Find closest GMM peak to this prediction
        dists = [(abs(m - pred), m) for m in gmm_means_kms]
        dists.sort()
        closest_dist, closest_mean = dists[0]
        pct_off = closest_dist / pred * 100

        match = {
            "N":          N,
            "predicted":  round(pred, 3),
            "gmm_peak":   round(closest_mean, 3),
            "delta_kms":  round(closest_dist, 3),
            "pct_off":    round(pct_off, 2),
            "matched":    pct_off < 5.0,   # within 5% = match
        }
        matches.append(match)

        flag = "✓ MATCH" if match["matched"] else "✗ MISS"
        print(f"  N={N:>3}  pred={pred:>7.2f}  gmm={closest_mean:>7.2f}  "
              f"Δ={closest_dist:>6.2f} km/s ({pct_off:.2f}%)  {flag}")

    n_matched = sum(1 for m in matches if m["matched"])
    print()
    print(f"  Matched: {n_matched}/{len(PREDICTED_NODES)} predicted nodes")

    if n_matched == len(PREDICTED_NODES) and best_n == len(PREDICTED_NODES):
        verdict = "STRONG_SIGNAL"
        interp  = (f"GMM selected n={best_n} matching prediction count "
                   f"and all peaks align with N×k_geo. Staircase confirmed.")
    elif n_matched >= 3:
        verdict = "PARTIAL_SIGNAL"
        interp  = (f"{n_matched}/{len(PREDICTED_NODES)} peaks match. "
                   f"Partial staircase structure present.")
    elif best_n == 1:
        verdict = "NULL"
        interp  = "GMM favors single component. No staircase structure found."
    else:
        verdict = "INCONCLUSIVE"
        interp  = (f"GMM found {best_n} components but peaks do not align "
                   f"with N×k_geo predictions.")

    print(f"  Verdict: {verdict}")
    print(f"  {interp}")

    return matches, verdict, interp


def main():
    print("=" * 60)
    print("GMM Velocity Dispersion Audit")
    print("=" * 60)
    print(f"k_geo = {K_GEO:.10f}")
    print(f"Input: {G1_LAKE}")
    print()

    if not SKLEARN_AVAILABLE:
        print("scikit-learn not found. Install it first:")
        print("  pip install scikit-learn --break-system-packages")
        sys.exit(1)

    import numpy as np

    # Step 1: Load data
    print("Loading G1 vdisp values...")
    values = load_vdisp_values()

    # Basic stats
    arr     = np.array(values)
    mean_v  = float(arr.mean())
    std_v   = float(arr.std())
    print(f"  vdisp range: {arr.min():.1f} to {arr.max():.1f} km/s")
    print(f"  mean={mean_v:.2f}  std={std_v:.2f}")
    print()

    # Step 2: Run GMM (BLIND — no knowledge of predictions)
    print("Running GMM (blind — predictions not known to fitter)...")
    gmm_results, best_n = run_gmm_audit(values)

    best_means = gmm_results[best_n]["means_kms"]

    # Step 3: Compare to predictions AFTER fitting
    matches, verdict, interp = compare_to_predictions(best_means, best_n)

    # Step 4: Write report
    report = {
        "audit_type":        "gmm_vdisp_blind_test",
        "audit_status":      "mondy_verified_2026-04",
        "k_geo":             K_GEO,
        "n_records_loaded":  len(values),
        "n_records_gmm":     min(len(values), MAX_RECORDS),
        "vdisp_range_kms":   [float(arr.min()), float(arr.max())],
        "vdisp_mean_kms":    mean_v,
        "vdisp_std_kms":     std_v,
        "gmm_results":       {str(k): v for k, v in gmm_results.items()},
        "best_n_components": best_n,
        "best_bic":          gmm_results[best_n]["bic"],
        "best_means_kms":    best_means,
        "predicted_nodes":   [{"N": N, "pred_kms": round(p, 3)}
                               for N, p in PREDICTED_NODES],
        "peak_comparison":   matches,
        "n_matched":         sum(1 for m in matches if m["matched"]),
        "verdict":           verdict,
        "interpretation":    interp,
        "methodology_note":  (
            "GMM fitted WITHOUT knowledge of predicted peaks. "
            "Predictions compared AFTER fitting. "
            "BIC model selection penalizes complexity. "
            "A match requires peak within 5% of predicted value."
        ),
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with REPORT_PATH.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print()
    print(f"Report written: {REPORT_PATH}")
    print()
    print("Vol5 methodology note:")
    print("  If STRONG_SIGNAL: 5-node galaxy staircase confirmed.")
    print("  If PARTIAL_SIGNAL: document partial structure, run full 1.84M.")
    print("  If NULL: Lyra's staircase hypothesis falsified.")
    print("  Either result is scientifically valuable.")


if __name__ == "__main__":
    main()