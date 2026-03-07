#!/usr/bin/env python3
"""
UMC3 — Harmonic Shelves
Materials ↔ Chemistry

Purpose:
    Identify harmonic shelf structure across domains.

Outputs:
    figures/umc/umc3_shelves.png
    reports/umc/umc3_shelves.md
"""
import json
from pathlib import Path
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
# Same imports + load_scalars as UMC1

ROOT = Path(__file__).resolve().parents[2]
MATERIALS = ROOT / "lakes" / "materials"
CHEMICALS = ROOT / "lakes" / "chemicals"


def load_scalars(path):
    scalars = []
    for file in path.glob("*.jsonl"):
        with open(file) as f:
            for line in f:
                obj = json.loads(line)
                # Chemistry uses scalar_kls
                # Materials use scalar_invariant
                val = obj.get("scalar_kls", obj.get("scalar_invariant"))
                if val is not None:
                    scalars.append(val)
    return scalars


FIG_OUT = Path("../../figures/umc/umc3_shelves.png")
REPORT_OUT = Path("../../reports/umc/umc3_shelves.md")

def compute_shelves(scalars, modulus=16/np.pi):
    return np.mod(scalars, modulus)

def main():
    m_scalars = np.array(load_scalars(MATERIALS))
    c_scalars = np.array(load_scalars(CHEMICALS))

    m_shelves = compute_shelves(m_scalars)
    c_shelves = compute_shelves(c_scalars)

    plt.figure(figsize=(10,6))
    plt.hist(m_shelves, bins=200, alpha=0.5, label="Materials")
    plt.hist(c_shelves, bins=200, alpha=0.5, label="Chemistry")
    plt.legend()
    plt.title("UMC3 — Harmonic Shelves")
    plt.savefig(FIG_OUT, dpi=300)

    with open(REPORT_OUT, "w") as f:
        f.write("# UMC3 — Harmonic Shelves\n")
        f.write("Shelf alignment across Materials and Chemistry.\n")

if __name__ == "__main__":
    main()
