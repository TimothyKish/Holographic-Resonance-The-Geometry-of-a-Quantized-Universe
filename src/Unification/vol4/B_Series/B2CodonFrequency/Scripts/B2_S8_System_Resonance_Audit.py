# B2_S8_System_Resonance_Audit.py
# LADDER STEP: 8 - INTEGRATED SIGNAL MAPPING

import json, math, os

def run_system_resonance():
    correlation_path = "../Processed/B2_S4_Correlation_Summary.json"
    
    if not os.path.exists(correlation_path):
        print("Error: Run S4 Correlation first.")
        return

    with open(correlation_path, 'r') as f:
        data = json.load(f)

    print(f"\n{'Amino Acid':<20} | {'Burden':<10} | {'24-Mode Pos':<12} | {'Stability'}")
    print("-" * 60)

    total_burden = 0
    for aa in data:
        # The 'Burden' is our corrected signal strength
        # We look at where this integrated energy sits in the container
        pos = (aa['burden'] % 24)
        stability = "HIGH" if (abs(pos-7) < 2 or abs(pos-13) < 2) else "LOW"
        
        print(f"{aa['name']:<20} | {aa['burden']:<10.4f} | {pos:<12.4f} | {stability}")
        total_burden += aa['burden']

    print("-" * 60)
    print(f"TOTAL ALPHABET BURDEN: {total_burden:.4f}")
    print(f"SYSTEM HARMONIC: {(total_burden % 24):.4f}")

if __name__ == "__main__":
    run_system_resonance()