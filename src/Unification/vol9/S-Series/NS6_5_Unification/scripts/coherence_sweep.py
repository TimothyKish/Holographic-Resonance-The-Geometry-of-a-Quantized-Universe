# vol5/S-Series/NS6_5_Unification/scripts/coherence_sweep.py
import json
import math
import statistics
from pathlib import Path

SOURCE_LAKE = Path("../../S6_Galactic/lake/s6_galactic_sovereign_raw.jsonl")
L = 16.0 / math.pi
ANCHOR = 6.6069e10

def get_coherence(galaxies, c):
    bins = 10
    occupancy = [0] * bins
    for gal in galaxies:
        # Calculate the invariant value
        val = ((gal["v_dispersion_kms"]**4) / (10**((25 - gal["magnitude_r"]) / 2.5))) / ANCHOR
        phi = abs(math.log(val)) % c
        bin_idx = int((phi / c) * bins)
        if bin_idx == bins: bin_idx -= 1
        occupancy[bin_idx] += 1
    # Coherence = Standard Deviation of Bin Occupancy
    # High = Banded/Gated | Low = Flat/Fluid
    return statistics.stdev(occupancy)

def run_sweep():
    print("===============================================================")
    print(" 🛡️ NS6_19: THE COHERENCE SWEEP (The Lattice Teeth)")
    print("===============================================================")
    
    if not SOURCE_LAKE.exists(): return
    galaxies = []
    with open(SOURCE_LAKE, 'r', encoding='utf-8') as f:
        for line in f: galaxies.append(json.loads(line))

    print(f"{'Multiplier'.ljust(12)} | {'Modulus C'.ljust(12)} | {'Coherence (Gate Strength)'}")
    print("-" * 60)

    # Prompt 2: Sweep C/L from 0.5 to 2.5
    steps = 40
    results = []
    for i in range(steps + 1):
        m = 0.5 + (i * (2.0 / steps)) # Multiplier m = C/L
        c = m * L
        score = get_coherence(galaxies, c)
        results.append((m, c, score))
        
        # Visualize the sweep in real-time
        bar = "█" * int(score * 2)
        print(f"{m:.2f}x L".ljust(12), f"| {c:.4f}".ljust(12), f"| {score:.2f} {bar}")

    # Prompt 3: Identify discrete C values (The "Dominant Wells")
    print("\n--- IDENTIFIED DISCRETE GATES (Coherence > 8.0) ---")
    for m, c, score in results:
        if score > 8.0:
            status = "ROOT" if 0.9 <= m <= 1.1 else "THERMAL" if 1.7 <= m <= 1.9 else "OCTAVE" if m >= 1.95 else "UNDEFINED"
            print(f"GATE DETECTED: {m:.2f}x L (C={c:.4f}) | Strength: {score:.2f} [{status}]")

if __name__ == "__main__":
    run_sweep()