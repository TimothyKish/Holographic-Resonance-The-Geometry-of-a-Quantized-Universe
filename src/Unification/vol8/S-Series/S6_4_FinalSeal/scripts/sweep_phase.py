# vol5/S-Series/S6_4_FinalSeal/scripts/sweep_phase.py
import json
import math
import os
from pathlib import Path

RAW_LAKE = Path("../../S6_Galactic/lake/s6_galactic_sovereign_raw.jsonl")
LATTICE_CONSTANT = 16.0 / math.pi

def run_sweep():
    print("===============================================================")
    print(" 🪐 S6_SWEEP: FINDING THE GALACTIC LATTICE PHASE")
    print("===============================================================")
    
    if not RAW_LAKE.exists(): return

    # Load the 50 Master Benchmarks into memory once
    galaxies = []
    with open(RAW_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            galaxies.append(json.loads(line))

    best_resonance = -1.0
    best_anchor = 0.0
    
    # We sweep the anchor from 1.0e10 to 1.0e11 (The Galactic Scale)
    print("[*] Sweeping Anchor range: 1.0e10 to 1.0e11...")
    
    results = []
    # 200 steps for high-precision tuning
    for i in range(200):
        # Exponential sweep to cover the log-scale
        test_anchor = 1.0e10 * (10 ** (i / 200)) 
        
        total_klc = 0.0
        for gal in galaxies:
            sigma = gal["v_dispersion_kms"]
            mag = gal["magnitude_r"]
            L = 10**((25 - mag) / 2.5)
            
            # The Invariant
            val = (sigma**4) / (L * test_anchor)
            
            # The Lattice Mapping
            log_val = abs(math.log(val))
            residue = log_val % LATTICE_CONSTANT
            klc = math.cos(residue * (2 * math.pi / LATTICE_CONSTANT))
            total_klc += klc
            
        avg_klc = total_klc / len(galaxies)
        results.append((test_anchor, avg_klc))
        
        if avg_klc > best_resonance:
            best_resonance = avg_klc
            best_anchor = test_anchor

    print("-" * 63)
    print(f"[+] SWEEP COMPLETE.")
    print(f"[!] PEAK RESONANCE FOUND: {best_resonance:.5f}")
    print(f"[!] OPTIMAL GALACTIC ANCHOR: {best_anchor:.4e}")
    print("-" * 63)
    
    # Simple ASCII visualization of the resonance curve
    print("\nVisualizing the Phase-Lock Peak:")
    for anchor, res in results[::10]: # Print every 10th step
        bar = "#" * int((res + 1) * 20)
        print(f"{anchor:.2e} [{bar.ljust(40)}] {res:+.3f}")

if __name__ == "__main__":
    run_sweep()