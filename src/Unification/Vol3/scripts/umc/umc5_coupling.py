#!/usr/bin/env python3
"""
UMC5 — Coupling Strength
Materials ↔ Chemistry

Purpose:
    Quantify coupling strength between domains.

Outputs:
    figures/umc/umc5_coupling.png
    reports/umc/umc5_coupling.md
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


FIG_OUT = Path("../../figures/umc/umc5_coupling.png")
REPORT_OUT = Path("../../reports/umc/umc5_coupling.md")


def main():
    # Load raw scalars
    m = np.array(load_scalars(MATERIALS))
    c = np.array(load_scalars(CHEMICALS))

    # Resample both curves to the same length
    N = 5000
    x_m = np.linspace(0, 1, len(m))
    x_c = np.linspace(0, 1, len(c))
    x_new = np.linspace(0, 1, N)

    m_resampled = np.interp(x_new, x_m, m)
    c_resampled = np.interp(x_new, x_c, c)

    # Coupling coefficient
    coupling = np.corrcoef(m_resampled, c_resampled)[0, 1]

    # Plot
    plt.figure(figsize=(6, 4))
    plt.bar(["Coupling"], [coupling])
    plt.title("UMC5 — Coupling Strength")
    plt.savefig(FIG_OUT, dpi=300)

    # Report
    with open(REPORT_OUT, "w") as f:
        f.write("# UMC5 — Coupling Strength\n")
        f.write(f"Coupling coefficient: {coupling}\n")


if __name__ == "__main__":
    main()
