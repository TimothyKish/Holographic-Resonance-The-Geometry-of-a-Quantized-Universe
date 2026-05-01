# vol5/S-Series/NS6_5_Unification/scripts/global_sweep.py
import json
import math
from pathlib import Path

SOURCE_LAKE = Path("../../S6_Galactic/lake/s6_galactic_sovereign_raw.jsonl")
ANCHOR = 6.6069e10 # Fixed Anchor to prevent "Hunting"

def run_global_sweep():
    print("===============================================================")
    print(" 🛡️ NS6_6: THE GLOBAL CONSTANT SWEEP (Brute Force Audit)")
    print("===============================================================")
    
    galaxies = []
    with open(SOURCE_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            galaxies.append(json.loads(line))

    # We sweep the CONSTANT itself, keeping the Anchor steady.
    # This removes the "Tuning" bias Phoenix is worried about.
    results = []
    
    # Sweep from 2.0 to 10.0
    for i in range(200, 1000):
        c = i / 100.0
        total_klc = 0.0
        for gal in galaxies:
            L = 10**((25 - gal["magnitude_r"]) / 2.5)
            val = (gal["v_dispersion_kms"]**4) / (L * ANCHOR)
            log_val = abs(math.log(val))
            klc = math.cos((log_val % c) * (2 * math.pi / c))
            total_klc += klc
        
        avg_klc = total_klc / len(galaxies)
        results.append((c, avg_klc))

    # Find the top 3 peaks
    results.sort(key=lambda x: abs(x[1]), reverse=True)
    
    print(f"{'Constant'.ljust(15)} | {'Resonance'}")
    print("-" * 30)
    for c, res in results[:10]:
        mark = "<-- THE LATTICE?" if abs(c - (16/math.pi)) < 0.05 else ""
        print(f"{str(round(c, 2)).ljust(15)} | {res:.5f} {mark}")

if __name__ == "__main__":
    run_global_sweep()