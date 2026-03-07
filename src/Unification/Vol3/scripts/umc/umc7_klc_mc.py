#!/usr/bin/env python3
# UMC7 — Final Unified Coordinate (KLC–MC)
# © 2026 KishLattice 16pi Initiative — Sovereign Audit Script
# Purpose: Compute the unified coordinate from UMC1–UMC6 outputs.
"""
UMC7 — Final Unified Coordinate (KLC-MC)
Materials ↔ Chemistry

Purpose:
    Produce the unified Kish Lattice Coordinate for the M↔C domain pair.

Outputs:
    lakes/clean/klc_mc.jsonl
    figures/umc/umc7_klc_mc.png
    reports/umc/umc7_klc_mc.md
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



OUT_LAKE = Path("../../lakes/clean/klc_mc.jsonl")
FIG_OUT = Path("../../figures/umc/umc7_klc_mc.png")
REPORT_OUT = Path("../../reports/umc/umc7_klc_mc.md")

def main():
    m = np.array(load_scalars(MATERIALS))
    c = np.array(load_scalars(CHEMICALS))

    # Placeholder unified coordinate (replace with your logic)
    klc_mc = (m.mean() + c.mean()) / 2

    # Write lake
    with open(OUT_LAKE, "w") as f:
        f.write(json.dumps({"kuu_series": "KLC-MC", "value": klc_mc}) + "\n")

    # Plot
    plt.figure(figsize=(6,4))
    plt.bar(["KLC-MC"], [klc_mc])
    plt.title("UMC7 — Final Unified Coordinate")
    plt.savefig(FIG_OUT, dpi=300)

    # Report
    with open(REPORT_OUT, "w") as f:
        f.write("# UMC7 — Final Unified Coordinate (KLC-MC)\n")
        f.write(f"KLC-MC = {klc_mc}\n")

if __name__ == "__main__":
    main()
