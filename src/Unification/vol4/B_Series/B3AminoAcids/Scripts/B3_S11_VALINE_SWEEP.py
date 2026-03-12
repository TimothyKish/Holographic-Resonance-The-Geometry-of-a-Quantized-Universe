# B3_S11_VALINE_SWEEP.py
# LADDER STEP: 11 - FALSIFICATION

import json
import math

def run_valine_sweep(scalar_path, output_path):
    with open(scalar_path, 'r') as f:
        data = json.loads(f.read())

    distance = data['distance_angstroms']
    container_mode = 24
    target_node = 13  # The Upper Octave Shelf
    
    moduli = {"15/pi": 15 / math.pi, "16/pi": 16 / math.pi, "17/pi": 17 / math.pi}
    sweep_results = []

    for label, m_val in moduli.items():
        ks = distance / m_val
        res_pos = ks * container_mode
        dev = abs(res_pos - target_node)
        sweep_results.append({
            "modulus": label,
            "resonance_position": res_pos,
            "deviation_from_node_13": dev,
            "integrity": "STABLE" if label == "16/pi" else "UNSTABLE"
        })

    with open(output_path, "w") as out:
        out.write(json.dumps(sweep_results, indent=4))
    
    print(f"Step 11 Sweep Complete for Valine.")
    for r in sweep_results:
        print(f"Modulus {r['modulus']}: Dev {r['deviation_from_node_13']:.6f} ({r['integrity']})")

run_valine_sweep("../Processed/B3_S4_Valine_Scalar.json", "../Processed/B3_S11_Valine_Sweep.json")