# vol5/S-Series/NS6_5_Unification/scripts/fluid_null.py
import json
import math
import random
from pathlib import Path

LATTICE = 16.0 / math.pi
ANCHOR = 6.6069e10

def run_fluid_null():
    print("===============================================================")
    print(" 🛡️ NS6_10: THE FLUID NULL (The Ultimate Falsification)")
    print("===============================================================")
    
    # Generate 50 "Fluid" Galaxies
    # Perfectly correlated (Faber-Jackson) but SMOOTH (no quantization)
    fluid_galaxies = []
    for i in range(50):
        s = random.uniform(70, 400)
        # Perfectly correlated Magnitude (L = s^4)
        # We add NO lattice noise, just a smooth distribution
        m = 25 - 2.5 * math.log10(s**4 / 1.0) 
        fluid_galaxies.append({"s": s, "m": m})

    test_points = [
        ("Root (1.0x)", LATTICE),
        ("Thermal (1.8x)", LATTICE * 1.8),
        ("Octave (2.0x)", LATTICE * 2.0)
    ]

    print(f"{'Position'.ljust(15)} | {'Resonance'}")
    print("-" * 30)

    for label, c in test_points:
        total_klc = 0.0
        for gal in fluid_galaxies:
            L = 10**((25 - gal["m"]) / 2.5)
            val = (gal["s"]**4) / (L * ANCHOR)
            log_val = abs(math.log(val))
            klc = math.cos((log_val % c) * (2 * math.pi / c))
            total_klc += klc
        
        avg_klc = total_klc / 50
        print(f"{label.ljust(15)} | {avg_klc:.5f}")

if __name__ == "__main__":
    run_fluid_null()