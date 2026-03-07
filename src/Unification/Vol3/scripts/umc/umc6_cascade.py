#!/usr/bin/env python3
"""
UMC6 — Harmonic Cascade
Materials ↔ Chemistry

Purpose:
    Compare shelf structure across domains using nonlinear cascade mapping.

Outputs:
    figures/umc/umc6_cascade.png
    reports/umc/umc6_cascade.md
"""

import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
MATERIALS = ROOT / "lakes" / "materials"
CHEMICALS = ROOT / "lakes" / "chemicals"


def load_scalars(path):
    scalars = []
    for file in path.glob("*.jsonl"):
        with open(file) as f:
            for line in f:
                obj = json.loads(line)
                val = obj.get("scalar_kls", obj.get("scalar_invariant"))
                if val is not None:
                    scalars.append(val)
    return scalars


def compute_shelves(arr, bins=200):
    """
    Compute shelf boundaries by histogramming the scalar distribution
    and returning the bin centers weighted by density.
    """
    hist, edges = np.histogram(arr, bins=bins, density=True)
    centers = 0.5 * (edges[:-1] + edges[1:])
    return centers * hist  # shelf-like structure


FIG_OUT = Path("../../figures/umc/umc6_cascade.png")
REPORT_OUT = Path("../../reports/umc/umc6_cascade.md")


def main():
    # Load raw scalars
    m = np.array(load_scalars(MATERIALS))
    c = np.array(load_scalars(CHEMICALS))

    # Compute shelves
    m_shelves = compute_shelves(m)
    c_shelves = compute_shelves(c)

    # Resample shelves to shared length
    N = 5000
    x_m = np.linspace(0, 1, len(m_shelves))
    x_c = np.linspace(0, 1, len(c_shelves))
    x_new = np.linspace(0, 1, N)

    m_resampled = np.interp(x_new, x_m, m_shelves)
    c_resampled = np.interp(x_new, x_c, c_shelves)

    # Plot cascade
    plt.figure(figsize=(6, 4))
    plt.scatter(m_resampled, c_resampled, s=1, alpha=0.3)
    plt.title("UMC6 — Harmonic Cascade")
    plt.xlabel("Materials Shelf Signal")
    plt.ylabel("Chemistry Shelf Signal")
    plt.savefig(FIG_OUT, dpi=300)

    # Report
    with open(REPORT_OUT, "w") as f:
        f.write("# UMC6 — Harmonic Cascade\n")
        f.write("Cascade generated using resampled shelf vectors (N = 5000).\n")


if __name__ == "__main__":
    main()
