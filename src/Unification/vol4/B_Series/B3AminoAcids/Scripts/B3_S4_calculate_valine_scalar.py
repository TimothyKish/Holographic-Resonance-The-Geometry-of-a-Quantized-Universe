# B3_S4_calculate_valine_scalar.py
# LADDER STEP: 4 - SCALAR COMPUTATION

import json
import math

def calculate_valine_scalar(lake_path, output_path):
    with open(lake_path, 'r') as f:
        data = json.loads(f.readline())
    
    coords = data['coords']
    n = coords[2]   # Nitrogen
    ca = coords[3]  # Alpha-Carbon

    distance = math.sqrt((n['x']-ca['x'])**2 + (n['y']-ca['y'])**2 + (n['z']-ca['z'])**2)
    k_modulus = 16 / math.pi
    kish_scalar = distance / k_modulus

    result = {
        "step": 4, "name": "Valine", "distance_angstroms": distance,
        "kish_scalar": kish_scalar, "modulus_used": "16/pi"
    }

    with open(output_path, "w") as out:
        out.write(json.dumps(result, indent=4))
    print(f"Valine Scalar: {kish_scalar:.6f}")

calculate_valine_scalar("../Lake/B3_S1_Valine_5876.jsonl", "../Processed/B3_S4_Valine_Scalar.json")