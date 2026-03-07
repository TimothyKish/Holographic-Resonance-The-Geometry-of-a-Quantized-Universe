#!/usr/bin/env python3
"""
UMC2 — Distribution Overlay
Materials ↔ Chemistry

Purpose:
    Overlay normalized KLS distributions to identify shared structure.

Outputs:
    figures/umc/umc2_distributions.png
    reports/umc/umc2_distributions.md
"""
import json
from pathlib import Path
import matplotlib.pyplot as plt
from pathlib import Path
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


FIG_OUT = Path("../../figures/umc/umc2_distributions.png")
REPORT_OUT = Path("../../reports/umc/umc2_distributions.md")

def main():
    m_scalars = load_scalars(MATERIALS)
    c_scalars = load_scalars(CHEMICALS)

    plt.figure(figsize=(10,6))
    plt.hist(m_scalars, bins=300, density=True, alpha=0.5, label="Materials")
    plt.hist(c_scalars, bins=300, density=True, alpha=0.5, label="Chemistry")
    plt.legend()
    plt.title("UMC2 — Normalized Distributions")
    plt.savefig(FIG_OUT, dpi=300)

    with open(REPORT_OUT, "w") as f:
        f.write("# UMC2 — Distribution Overlay\n")
        f.write("Normalized distributions for cross-domain comparison.\n")

if __name__ == "__main__":
    main()
