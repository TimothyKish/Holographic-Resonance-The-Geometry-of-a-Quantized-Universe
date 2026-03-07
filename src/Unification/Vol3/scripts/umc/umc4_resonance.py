#!/usr/bin/env python3
"""
UMC4 — Resonance Map
Materials ↔ Chemistry

Purpose:
    Compute resonance peaks between shelf distributions.

Outputs:
    figures/umc/umc4_resonance.png
    reports/umc/umc4_resonance.md
"""
import json
from pathlib import Path
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
from scipy.signal import correlate
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



FIG_OUT = Path("../../figures/umc/umc4_resonance.png")
REPORT_OUT = Path("../../reports/umc/umc4_resonance.md")

def main():
    m = np.array(load_scalars(MATERIALS))
    c = np.array(load_scalars(CHEMICALS))

    m_shelves = np.mod(m, 16/np.pi)
    c_shelves = np.mod(c, 16/np.pi)

    # Cross-correlation
    corr = correlate(m_shelves, c_shelves, mode="same")

    plt.figure(figsize=(10,6))
    plt.plot(corr)
    plt.title("UMC4 — Resonance Map")
    plt.savefig(FIG_OUT, dpi=300)

    with open(REPORT_OUT, "w") as f:
        f.write("# UMC4 — Resonance Map\n")
        f.write("Cross-domain resonance peaks.\n")

if __name__ == "__main__":
    main()
