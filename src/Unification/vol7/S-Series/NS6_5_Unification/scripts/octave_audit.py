# vol5/S-Series/NS6_5_Unification/scripts/octave_audit.py
import json
import math
from pathlib import Path

SOURCE_LAKE = Path("../../S6_Galactic/lake/s6_galactic_sovereign_raw.jsonl")
ANCHOR = 6.6069e10 
LATTICE = 16.0 / math.pi

def run_octave_audit():
    print("===============================================================")
    print(" 🛡️ NS6_8: THE HARMONIC OCTAVE AUDIT (The Galactic Chord)")
    print("===============================================================")
    
    galaxies = []
    with open(SOURCE_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            galaxies.append(json.loads(line))

    # We test the Root, the Thermal Shift (9/5), and the Double Octave (2/1)
    harmonics = {
        "Root (1:1)": LATTICE,
        "Thermal (9/5)": LATTICE * 1.8,
        "Octave (2:1)": LATTICE * 2.0,
        "Random (Pi/2)": LATTICE * (math.pi / 2) # The "Fluid" Control
    }

    print(f"{'Harmonic'.ljust(15)} | {'Constant'.ljust(10)} | {'Resonance'}")
    print("-" * 45)

    for label, const in harmonics.items():
        total_klc = 0.0
        for gal in galaxies:
            L = 10**((25 - gal["magnitude_r"]) / 2.5)
            val = (gal["v_dispersion_kms"]**4) / (L * ANCHOR)
            log_val = abs(math.log(val))
            klc = math.cos((log_val % const) * (2 * math.pi / const))
            total_klc += klc
        
        avg_klc = total_klc / len(galaxies)
        print(f"{label.ljust(15)} | {str(round(const, 3)).ljust(10)} | {avg_klc:.5f}")

if __name__ == "__main__":
    run_octave_audit()