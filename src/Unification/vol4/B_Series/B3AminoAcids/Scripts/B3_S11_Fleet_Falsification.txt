# B3_S11_Fleet_Falsification.py
# LADDER STEP: 11 - MULTI-MODULUS SWEEP (THE PROOF)

import json
import os

def run_fleet_falsification():
    audit_path = "../Processed/B3_S4_S8_Fleet_Audit.json"
    if not os.path.exists(audit_path):
        print("Error: Run S4_S8 audit first.")
        return

    with open(audit_path, 'r') as f:
        fleet = json.load(f)

    moduli = {"15/pi": 15/3.1415926535, "16/pi": 16/3.1415926535, "17/pi": 17/3.1415926535}
    
    print(f"\n{'Amino Acid':<15} | {'15/pi Dev':<10} | {'16/pi Dev':<10} | {'17/pi Dev':<10}")
    print("-" * 60)

    for amino in fleet:
        dist = amino['dist']
        shelf = amino['shelf']
        devs = {}

        for label, m_val in moduli.items():
            ks = dist / m_val
            res_pos = ks * 24
            devs[label] = abs(res_pos - shelf)

        print(f"{amino['name']:<15} | {devs['15/pi']:<10.4f} | {devs['16/pi']:<10.4f} | {devs['17/pi']:<10.4f}")

if __name__ == "__main__":
    run_fleet_falsification()