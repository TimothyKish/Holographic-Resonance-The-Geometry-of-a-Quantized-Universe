# vol5/S-Series/NS6_5_Unification/scripts/constant_battle.py
import json
import math
from pathlib import Path

SOURCE_LAKE = Path("../../S6_Galactic/lake/s6_galactic_sovereign_raw.jsonl")

def run_battle():
    print("===============================================================")
    print(" 🛡️ THE CONSTANT BATTLE: IS 16/PI PRIVILEGED?")
    print("===============================================================")
    
    # 1. Load Real Data
    galaxies = []
    with open(SOURCE_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            galaxies.append(json.loads(line))

    # 2. Define the Contenders
    contenders = {
        "16/pi (Lattice)": 16.0 / math.pi,
        "2*pi (Circle)": 2.0 * math.pi,
        "5.0 (Integer)": 5.0,
        "e (Natural)": math.e
    }

    results = {}

    print("[*] Sweeping anchors for each contender...")
    for label, const in contenders.items():
        best_res = 0.0
        # Sweep anchor from 1e10 to 1e11
        for i in range(200):
            anchor = 1.0e10 * (10 ** (i / 200))
            total_klc = 0.0
            for gal in galaxies:
                L = 10**((25 - gal["magnitude_r"]) / 2.5)
                val = (gal["v_dispersion_kms"]**4) / (L * anchor)
                log_val = abs(math.log(val))
                klc = math.cos((log_val % const) * (2 * math.pi / const))
                total_klc += klc
            
            avg_klc = total_klc / len(galaxies)
            if abs(avg_klc) > best_res:
                best_res = abs(avg_klc)
        
        results[label] = best_res

    print("-" * 63)
    for label, res in results.items():
        bar = "#" * int(res * 40)
        print(f"{label.ljust(15)} [{bar.ljust(40)}] {res:.5f}")
    
    print("-" * 63)
    # The ultimate check: Is 16/pi the king of the hill?
    if results["16/pi (Lattice)"] == max(results.values()):
        print("[+] VERDICT: 16/pi is the GLOBAL MAXIMUM.")
    else:
        print("[!] WARNING: An arbitrary constant outperformed the Lattice.")

if __name__ == "__main__":
    run_battle()