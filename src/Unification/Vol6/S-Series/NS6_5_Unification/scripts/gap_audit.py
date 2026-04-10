# vol5/S-Series/NS6_5_Unification/scripts/gap_audit.py
import json
import math
from pathlib import Path

SOURCE_LAKE = Path("../../S6_Galactic/lake/s6_galactic_sovereign_raw.jsonl")
LATTICE = 16.0 / math.pi
ANCHOR = 6.6069e10 

def get_res(galaxies, c):
    total_klc = 0.0
    for gal in galaxies:
        L = 10**((25 - gal["magnitude_r"]) / 2.5)
        val = (gal["v_dispersion_kms"]**4) / (L * ANCHOR)
        log_val = abs(math.log(val))
        klc = math.cos((log_val % c) * (2 * math.pi / c))
        total_klc += klc
    return total_klc / len(galaxies)

def run_gap_audit():
    print("===============================================================")
    print(" 🛡️ NS6_9: THE GAP AUDIT (Quantization vs. Fluidity)")
    print("===============================================================")
    
    if not SOURCE_LAKE.exists(): return
    galaxies = []
    with open(SOURCE_LAKE, 'r', encoding='utf-8') as f:
        for line in f: galaxies.append(json.loads(line))

    # Testing the Harmonics vs. The "Smooth" Gaps
    test_points = [
        ("Root (1.0x)", LATTICE),             # Harmonic
        ("Gap A (1.2x)", LATTICE * 1.2),       # The "Smooth" Void
        ("Gap B (1.5x)", LATTICE * 1.5),       # The "Smooth" Void
        ("Thermal (1.8x)", LATTICE * 1.8),     # Harmonic Peak
        ("Gap C (1.9x)", LATTICE * 1.9),       # The "Smooth" Void
        ("Octave (2.0x)", LATTICE * 2.0)      # Harmonic Ridge
    ]

    print(f"{'Position'.ljust(15)} | {'Multiplier'.ljust(12)} | {'Resonance'}")
    print("-" * 45)

    for label, c in test_points:
        res = get_res(galaxies, c)
        mult = c / LATTICE
        print(f"{label.ljust(15)} | {str(round(mult, 2)).ljust(12)} | {res:.5f}")

if __name__ == "__main__":
    run_gap_audit()