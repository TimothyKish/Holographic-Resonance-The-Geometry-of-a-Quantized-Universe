#!/usr/bin/env python3
"""
UMC1 — Scalar Comparison
Materials ↔ Chemistry

Purpose:
    Compare the Kish Lattice Scalar (KLS) distributions between the
    sovereign Materials lake and the sovereign Chemistry lake.

Inputs:
    lakes/materials/*.jsonl
    lakes/chemicals/*.jsonl

Outputs:
    figures/umc/umc1_scalar_compare.png
    reports/umc/umc1_scalar_compare.md
"""

import json
from pathlib import Path
import matplotlib.pyplot as plt

MATERIALS = Path("../../lakes/materials")
CHEMICALS = Path("../../lakes/chemicals")
FIG_OUT = Path("../../figures/umc/umc1_scalar_compare.png")
REPORT_OUT = Path("../../reports/umc/umc1_scalar_compare.md")

def load_scalars(path):
    scalars = []
    for file in path.glob("*.jsonl"):
        with open(file) as f:
            for line in f:
                obj = json.loads(line)
                scalars.append(obj.get("scalar_kls", obj.get("scalar_invariant")))
    return scalars

def main():
    m_scalars = load_scalars(MATERIALS)
    c_scalars = load_scalars(CHEMICALS)

    # Plot
    plt.figure(figsize=(10,6))
    plt.hist(m_scalars, bins=200, alpha=0.5, label="Materials")
    plt.hist(c_scalars, bins=200, alpha=0.5, label="Chemistry")
    plt.legend()
    plt.title("UMC1 — Scalar Comparison")
    plt.savefig(FIG_OUT, dpi=300)

    # Report
    with open(REPORT_OUT, "w") as f:
        f.write("# UMC1 — Scalar Comparison\n")
        f.write("Materials vs Chemistry scalar distributions.\n")

if __name__ == "__main__":
    main()
