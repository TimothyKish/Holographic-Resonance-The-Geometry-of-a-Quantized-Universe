# vol5/S-Series/NS6_5_Unification/scripts/q_factor_audit.py
import json
import math
import os
from pathlib import Path

SOURCE_LAKE = Path("../../S6_Galactic/lake/s6_galactic_sovereign_raw.jsonl")

def get_resonance(galaxies, anchor, constant):
    total_klc = 0.0
    for gal in galaxies:
        L = 10**((25 - gal["magnitude_r"]) / 2.5)
        # The Unified Transform
        val = (gal["v_dispersion_kms"]**4) / (L * anchor)
        log_val = abs(math.log(val))
        klc = math.cos((log_val % constant) * (2 * math.pi / constant))
        total_klc += klc
    return total_klc / len(galaxies)

def run_q_audit():
    print("===============================================================")
    print(" 🛡️ Q-FACTOR AUDIT: TESTING PEAK SENSITIVITY")
    print("===============================================================")
    
    # 1. Load Real Data
    galaxies = []
    if not SOURCE_LAKE.exists():
        print("[!] Error: Master Lake not found.")
        return
    with open(SOURCE_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            galaxies.append(json.loads(line))

    # 2. Define the Contenders
    contenders = {
        "16/pi (Lattice)": 16.0 / math.pi,
        "2*pi (Circle)": 2.0 * math.pi
    }

    print(f"[*] Analyzing {len(galaxies)} galaxies for Structural Integrity...")
    print("-" * 63)

    for label, const in contenders.items():
        # Step A: Find the Local Peak Anchor via Sweep
        best_res = 0.0
        peak_anchor = 0.0
        for i in range(500):
            test_anchor = 1.0e10 * (10 ** (i / 500))
            res = get_resonance(galaxies, test_anchor, const)
            if abs(res) > best_res:
                best_res = abs(res)
                peak_anchor = test_anchor
        
        # Step B: Measure "Shatter Rate" (Move anchor by 0.5%)
        off_anchor = peak_anchor * 1.005 
        off_res = abs(get_resonance(galaxies, off_anchor, const))
        
        # Q-Factor Calculation: How much signal is lost by 0.5% drift?
        loss_percentage = ((best_res - off_res) / best_res) * 100
        
        print(f"RESULTS FOR {label}:")
        print(f"  > Peak Resonance: {best_res:.5f}")
        print(f"  > 0.5% Drift Res: {off_res:.5f}")
        print(f"  > SHATTER RATE:   {loss_percentage:.2f}%")
        
        if loss_percentage > 15.0:
            print(f"  [+] VERDICT: HIGH Q-FACTOR (Structural Bolt)")
        else:
            print(f"  [!] VERDICT: LOW Q-FACTOR (Sloppy Artifact)")
        print("-" * 63)

if __name__ == "__main__":
    run_clean_audit = run_q_audit()