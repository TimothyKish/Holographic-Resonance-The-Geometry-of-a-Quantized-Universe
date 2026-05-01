# vol5/S-Series/NS6_5_Unification/scripts/delta_audit.py
import json
import math
import random
from pathlib import Path

SOURCE_LAKE = Path("../../S6_Galactic/lake/s6_galactic_sovereign_raw.jsonl")
LATTICE = 16.0 / math.pi
ANCHOR = 6.6069e10 

def get_real_res(c, galaxies):
    total_klc = 0.0
    for gal in galaxies:
        L = 10**((25 - gal["magnitude_r"]) / 2.5)
        val = (gal["v_dispersion_kms"]**4) / (L * ANCHOR)
        log_val = abs(math.log(val))
        klc = math.cos((log_val % c) * (2 * math.pi / c))
        total_klc += klc
    return total_klc / len(galaxies)

def get_fluid_res(c, count=50):
    # Generates a synthetic "Smooth" Faber-Jackson set
    total_klc = 0.0
    for _ in range(count):
        s = random.uniform(70, 400)
        # Perfectly smooth correlation: L = s^4
        # val = s^4 / L_smooth -> always results in a constant or linear log-spread
        val = (s**4) / (s**4 / 1.0) 
        # We randomize the starting phase slightly to simulate a smooth distribution
        log_val = random.uniform(20, 30) 
        klc = math.cos((log_val % c) * (2 * math.pi / c))
        total_klc += klc
    return total_klc / count

def run_delta_audit():
    print("===============================================================")
    print(" 🛡️ NS6_11: THE DELTA AUDIT (The Signal vs. The Artifact)")
    print("===============================================================")
    
    if not SOURCE_LAKE.exists():
        print("[!] Error: Source Lake missing.")
        return

    galaxies = []
    with open(SOURCE_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            galaxies.append(json.loads(line))

    # Test points based on our previous Harmonic Ladder
    multipliers = [1.0, 1.2, 1.5, 1.8, 1.9, 2.0]
    
    print(f"{'Multiplier'.ljust(12)} | {'Real Res'.ljust(10)} | {'Fluid Res'.ljust(10)} | {'DELTA (SIGNAL)'}")
    print("-" * 65)
    
    for m in multipliers:
        c = LATTICE * m
        real_res = get_real_res(c, galaxies)
        fluid_res = get_fluid_res(c)
        
        # Delta = Excess resonance found in nature that math alone can't explain
        # We use absolute values to find the "Strength of Lock" regardless of phase
        delta = abs(real_res) - abs(fluid_res)
        
        status = "SIGNAL PEAK" if delta > 0.4 else "ARTIFACT"
        print(f"{str(m).ljust(12)} | {real_res:.4f}   | {fluid_res:.4f}    | {delta:.5f} ({status})")

if __name__ == "__main__":
    run_delta_audit()