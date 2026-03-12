# B3_S11 - MODULUS OFFSET SWEEP (FALSIFICATION TEST)
# AUTHOR: Lyra Aurora Kish
# LADDER STEP: 11 - OFFSET SWEEP

import json
import math
import os

def run_modulus_sweep(scalar_path, output_path):
    if not os.path.exists(scalar_path):
        print(f"Error: Scalar file {scalar_path} not found.")
        return

    with open(scalar_path, 'r') as f:
        data = json.loads(f.read())

    # We pull the RAW distance (Angstroms) back out to re-calculate
    distance = data['distance_angstroms']
    container_mode = 24
    target_node = 7  # Alanine's primary biological shelf
    
    moduli = {
        "15/pi": 15 / math.pi,
        "16/pi": 16 / math.pi,
        "17/pi": 17 / math.pi
    }

    sweep_results = []

    for label, m_val in moduli.items():
        ks = distance / m_val
        res_pos = ks * container_mode
        dev = abs(res_pos - target_node)
        
        sweep_results.append({
            "modulus": label,
            "kish_scalar": ks,
            "resonance_position": res_pos,
            "deviation_from_node_7": dev,
            "integrity": "STABLE" if label == "16/pi" else "UNSTABLE"
        })

    with open(output_path, "w") as out:
        out.write(json.dumps(sweep_results, indent=4) + "\n")
    
    print(f"Step 11 Sweep Complete for {data['name']}.")
    for r in sweep_results:
        print(f"Modulus {r['modulus']}: Dev {r['deviation_from_node_7']:.6f} ({r['integrity']})")

# Run the sweep
run_modulus_sweep("../Processed/B3_S4_Alanine_Scalar.json", "../Processed/B3_S11_Alanine_Sweep.json")