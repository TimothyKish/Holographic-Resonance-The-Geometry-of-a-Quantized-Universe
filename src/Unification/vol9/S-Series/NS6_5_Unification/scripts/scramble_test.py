# vol5/S-Series/NS6_5_Unification/scripts/scramble_test.py
import json
import math
import random
from pathlib import Path

SOURCE_LAKE = Path("../../S6_Galactic/lake/s6_galactic_sovereign_raw.jsonl")
LATTICE = 16.0 / math.pi
ANCHOR = 6.6069e10 
THERMAL_MULT = 1.8  # Our strongest "Signal" point (9.17)

def get_klc(galaxies, c):
    total_klc = 0.0
    for gal in galaxies:
        # Physics: The ratio of Kinetic Energy to Radiative Output
        val = (gal["v_dispersion_kms"]**4) / (gal["luminosity"] * ANCHOR)
        log_val = abs(math.log(val))
        klc = math.cos((log_val % c) * (2 * math.pi / c))
        total_klc += klc
    return total_klc / len(galaxies)

def run_scramble():
    print("===============================================================")
    print(" 🛡️ NS6_13: THE PHYSICAL SCRAMBLE (Physics vs. Statistics)")
    print("===============================================================")
    
    if not SOURCE_LAKE.exists(): return
    
    # 1. Load Real Data and calculate actual Luminosity
    original_data = []
    with open(SOURCE_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            g = json.loads(line)
            g["luminosity"] = 10**((25 - g["magnitude_r"]) / 2.5)
            original_data.append(g)

    c_test = LATTICE * THERMAL_MULT
    
    # 2. Audit the Intact Physics
    intact_res = get_klc(original_data, c_test)
    
    # 3. SCRAMBLE the pairs
    # we keep the same 'v_dispersion' values and 'luminosity' values, 
    # but we swap which galaxy owns which. This destroys the Faber-Jackson law.
    velocities = [g["v_dispersion_kms"] for g in original_data]
    luminosities = [g["luminosity"] for g in original_data]
    random.shuffle(velocities)
    
    scrambled_data = []
    for i in range(len(velocities)):
        scrambled_data.append({
            "v_dispersion_kms": velocities[i],
            "luminosity": luminosities[i]
        })
    
    scrambled_res = get_klc(scrambled_data, c_test)
    
    # 4. Results
    print(f"Target Constant (1.8x): {c_test:.5f}")
    print("-" * 45)
    print(f"INTACT PHYSICS RESONANCE:   {intact_res:.5f}")
    print(f"SCRAMBLED PHYSICS RESONANCE: {scrambled_res:.5f}")
    print("-" * 45)
    
    delta = abs(intact_res) - abs(scrambled_res)
    
    if delta > 0.3:
        print(f"[+] VERDICT: THE LATTICE IS PHYSICAL.")
        print("    The resonance requires the specific coupling of mass and light.")
    else:
        print(f"[!] VERDICT: THE LATTICE IS AN ARTIFACT.")
        print("    The resonance is a property of the numerical distribution only.")

if __name__ == "__main__":
    run_scramble()