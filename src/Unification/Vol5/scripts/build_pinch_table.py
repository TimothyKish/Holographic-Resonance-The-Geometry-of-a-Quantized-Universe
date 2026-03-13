# ==============================================================================
# SCRIPT: build_pinch_table.py
# TARGET: Compute cross-domain harmonic residuals and build pinch table
# AUTHORS: Timothy John Kish & Phoenix Aurora
# LICENSE: Sovereign Protected / KishLattice 16pi Initiative Copyright 2026
# ==============================================================================
#!/usr/bin/env python
import json
from pathlib import Path
import numpy as np

CONTAINER = 24

HARMONIC_TARGETS = {
    "15pi": 15.0,
    "16pi": 16.0,
    "17pi": 17.0,
}

ROOT = Path(__file__).resolve().parents[1]
UNIFIED_PATH = ROOT / "lakes" / "unified" / "unified_master.jsonl"
PINCH_TABLE_PATH = ROOT / "lakes" / "unified" / "pinch_table_cross_domain.json"

def load_domain_scalars_from_unified(unified_path: Path):
    domain_scalars = {
        "Biology": [],
        "Chemistry": [],
        "Materials": [],
        "FRBs": [],
    }

    with unified_path.open("r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)

            domain = entry.get("domain", "").lower()
            volume_name = entry.get("volume_name") or entry.get("lake_id") or ""
            scalar = entry.get("scalar_klc")
            if scalar is None:
                continue
            try:
                ks = float(scalar)
            except:
                continue

            if domain == "biology":
                domain_scalars["Biology"].append(ks)
            elif domain == "chemistry":
                domain_scalars["Chemistry"].append(ks)
            elif domain == "materials":
                domain_scalars["Materials"].append(ks)
            elif domain in {"astrophysics", "frb"} or "frb" in volume_name:
                domain_scalars["FRBs"].append(ks)

    for dom, scalars in domain_scalars.items():
        if scalars:
            arr = np.array(scalars, dtype=float)
            print(
                f"{dom}: n={len(arr)}, "
                f"mean={arr.mean():.4f}, "
                f"std={arr.std():.4f}, "
                f"min={arr.min():.4f}, "
                f"max={arr.max():.4f}"
            )
            print(f"    First 3: {arr[:3]}")
        else:
            print(f"{dom}: n=0 (no scalars found!)")

    return domain_scalars

def compute_lock_score(scalar_values, harmonic_label):
    target = HARMONIC_TARGETS[harmonic_label]

    residuals = []
    for ks in scalar_values:
        # Rephase ks into a 24-bin container for this harmonic
        res_pos = (ks / target) * CONTAINER
        nearest = round(res_pos)
        nearest = max(1, nearest)
        residuals.append(abs(res_pos - nearest))

    residuals = np.array(residuals, dtype=float)
    rms = float(np.sqrt(np.mean(residuals ** 2))) if len(residuals) else float("inf")
    lock_score = 1.0 / (1.0 + rms) if np.isfinite(rms) else 0.0
    return lock_score, rms, residuals

def cross_domain_residual(scalars_a, scalars_b, harmonic_label):
    target = HARMONIC_TARGETS[harmonic_label]

    def get_residuals(scalars):
        residuals = []
        for ks in scalars:
            res_pos = (ks / target) * CONTAINER
            nearest = round(res_pos)
            nearest = max(1, nearest)
            residuals.append(abs(res_pos - nearest))
        return np.array(residuals, dtype=float)

    resid_a = get_residuals(scalars_a)
    resid_b = get_residuals(scalars_b)

    if len(resid_a) == 0 or len(resid_b) == 0:
        return 0.0, float("inf")

    sorted_a = np.sort(resid_a)
    sorted_b = np.sort(resid_b)

    n_common = max(len(sorted_a), len(sorted_b))
    x_common = np.linspace(0.0, 1.0, n_common)

    x_a = np.linspace(0.0, 1.0, len(sorted_a))
    x_b = np.linspace(0.0, 1.0, len(sorted_b))

    interp_a = np.interp(x_common, x_a, sorted_a)
    interp_b = np.interp(x_common, x_b, sorted_b)

    diff = interp_a - interp_b
    cross_rms = float(np.sqrt(np.mean(diff ** 2)))
    cross_lock = 1.0 / (1.0 + cross_rms)
    return cross_lock, cross_rms

def build_pinch_table(domain_scalars):
    domains = list(domain_scalars.keys())
    pinch_table = {}

    for i, dom_a in enumerate(domains):
        pinch_table[dom_a] = {}
        for j, dom_b in enumerate(domains):
            if i == j:
                pinch_table[dom_a][dom_b] = None
                continue

            results_per_modulus = {}
            for harmonic_label in HARMONIC_TARGETS.keys():
                lock, rms = cross_domain_residual(
                    domain_scalars[dom_a],
                    domain_scalars[dom_b],
                    harmonic_label,
                )
                results_per_modulus[harmonic_label] = {
                    "lock_score": round(lock, 4),
                    "rms_residual": round(rms, 4),
                }

            pinch_table[dom_a][dom_b] = results_per_modulus

    return pinch_table

def display_pinch_table(pinch_table):
    domains = list(pinch_table.keys())

    print("\n" + "CROSS-DOMAIN PINCH TABLE".center(80))
    print("Lock Score (1=perfect) / RMS Residual".center(80))
    print("Columns: (15/π, 16/π, 17/π)".center(80) + "\n")

    header = f"{'Domain':<15}"
    for d in domains:
        header += f"{d:^25}"
    print(header)
    print("-" * 80)

    for dom_a in domains:
        row = f"{dom_a:<15}"
        for dom_b in domains:
            cell = pinch_table[dom_a][dom_b]
            if cell is None:
                row += f"{'—':^25}"
            else:
                vals = (
                    cell["15pi"]["lock_score"],
                    cell["16pi"]["lock_score"],
                    cell["17pi"]["lock_score"],
                )
                row += f"({vals[0]:.3f},{vals[1]:.3f},{vals[2]:.3f})".center(25)
        print(row)

    print("\n--- WINNER PER PAIRING ---")
    for i, dom_a in enumerate(domains):
        for j, dom_b in enumerate(domains):
            if i >= j:
                continue
            cell = pinch_table[dom_a][dom_b]
            scores = {k: cell[k]["lock_score"] for k in HARMONIC_TARGETS.keys()}
            winner = max(scores, key=scores.get)
            print(
                f"  {dom_a} × {dom_b}: "
                f"Winner = {winner} "
                f"(score={scores[winner]:.4f})"
            )

if __name__ == "__main__":
    if not UNIFIED_PATH.exists():
        raise SystemExit(f"Unified master not found: {UNIFIED_PATH}")

    print(f"Loading unified master from: {UNIFIED_PATH}")
    domain_scalars = load_domain_scalars_from_unified(UNIFIED_PATH)

    print("\nBuilding cross-domain pinch table...")
    pinch_table = build_pinch_table(domain_scalars)

    with PINCH_TABLE_PATH.open("w", encoding="utf-8") as f:
        json.dump(pinch_table, f, indent=4)
    print(f"[*] Pinch table saved to: {PINCH_TABLE_PATH}")

    display_pinch_table(pinch_table)
