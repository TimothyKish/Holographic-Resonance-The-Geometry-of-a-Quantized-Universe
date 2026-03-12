# B1_S11_Mirror_Falsification.py
# LADDER STEP: 11 - MULTI-MODULUS SWEEP (THE MIRROR PROOF)

import json
import os
import math

def run_mirror_falsification():
    # Use the processed audit we just generated in S4_S8
    audit_path = "../Processed/B1_S4_S8_Mirror_Audit.json"
    
    if not os.path.exists(audit_path):
        print("Error: Run S4_S8 audit first to generate the fleet data.")
        return

    with open(audit_path, 'r') as f:
        fleet = json.load(f)

    pi_val = math.pi
    # The Three Moduli: The "Biological" 16/pi and its neighbors
    moduli = {
        "15/pi": 15/pi_val, 
        "16/pi": 16/pi_val, 
        "17/pi": 17/pi_val
    }
    
    print(f"\n{'Mirror Acid':<25} | {'15/pi Dev':<10} | {'16/pi Dev':<10} | {'17/pi Dev':<10}")
    print("-" * 75)

    for amino in fleet:
        dist = amino['dist']
        shelf = amino['shelf']
        name = amino['name']
        is_simulated = amino.get('simulated', False)
        
        devs = {}
        for label, m_val in moduli.items():
            ks = dist / m_val
            res_pos = ks * 24
            devs[label] = abs(res_pos - shelf)

        display_name = f"*{name}" if is_simulated else name
        
        print(f"{display_name:<25} | {devs['15/pi']:<10.4f} | {devs['16/pi']:<10.4f} | {devs['17/pi']:<10.4f}")

    print("\n[!] Falsification Sweep Complete.")
    print("Compare these 16/pi deviations to the B3 Sovereign Fleet to find the 'Chirality Tax'.")

if __name__ == "__main__":
    run_mirror_falsification()