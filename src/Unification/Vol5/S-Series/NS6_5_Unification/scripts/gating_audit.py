# vol5/S-Series/NS6_5_Unification/scripts/gating_audit.py
import json
import math
import statistics
from pathlib import Path

SOURCE_LAKE = Path("../../S6_Galactic/lake/s6_galactic_sovereign_raw.jsonl")
LATTICE = 16.0 / math.pi
ANCHOR = 6.6069e10

def get_phase_distribution(galaxies, c, bins=10):
    # Divide the Modulo C into 'bins' to see where galaxies congregate
    occupancy = [0] * bins
    for gal in galaxies:
        val = ((gal["v_dispersion_kms"]**4) / (10**((25 - gal["magnitude_r"]) / 2.5))) / ANCHOR
        phi = abs(math.log(val)) % c
        bin_idx = int((phi / c) * bins)
        if bin_idx == bins: bin_idx -= 1
        occupancy[bin_idx] += 1
    return occupancy

def run_gating_audit():
    print("===============================================================")
    print(" 🛡️ NS6_18: THE GATING INTERVAL (Claude's Phase-Lock)")
    print("===============================================================")
    
    galaxies = []
    with open(SOURCE_LAKE, 'r', encoding='utf-8') as f:
        for line in f: galaxies.append(json.loads(line))

    gates = [
        ("ROOT GATE (1.0L)", LATTICE),
        ("THERMAL GATE (1.8L)", LATTICE * 1.8),
        ("NULL VOID (1.9L)", LATTICE * 1.9),
        ("OCTAVE GATE (2.0L)", LATTICE * 2.0)
    ]

    for label, c in gates:
        print(f"\n--- {label} (C = {c:.3f}) ---")
        dist = get_phase_distribution(galaxies, c)
        
        # Visualize the 'Banding'
        max_occ = max(dist)
        for i, count in enumerate(dist):
            bar = "█" * int((count / max_occ) * 20) if max_occ > 0 else ""
            print(f"Bin {i}: {bar.ljust(21)} ({count} gals)")
        
        # Calculate Coherence (Variance of occupancy)
        # High Variance = Banded (Gated) | Low Variance = Flat (Fluid)
        coherence = statistics.stdev(dist)
        print(f"Gate Coherence Score: {coherence:.2f}")

if __name__ == "__main__":
    run_gating_audit()