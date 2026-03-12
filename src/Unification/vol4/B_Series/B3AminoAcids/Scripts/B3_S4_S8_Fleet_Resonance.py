# B3_S4_S8_Fleet_Resonance.py
# LADDER STEP: 4 (SCALAR) & 8 (RESONANCE)
# TARGET: FULL 20 FLEET

import json
import math
import os
import glob

def run_fleet_resonance():
    lake_dir = "../Lake/"
    output_path = "../Processed/B3_S4_S8_Fleet_Audit.json"
    k_modulus = 16 / math.pi
    container_mode = 24
    
    lake_files = glob.glob(os.path.join(lake_dir, "*.jsonl"))
    results = []

    print(f"{'Amino Acid':<15} | {'Dist':<8} | {'Scalar':<8} | {'Shelf':<5} | {'Dev':<8}")
    print("-" * 55)

    for file_path in lake_files:
        with open(file_path, 'r') as f:
            data = json.loads(f.readline())
        
        name = data['name']
        coords = data['coords']
        
        # Standard Backbone: Nitrogen (2) to Alpha-Carbon (3)
        n, ca = coords[2], coords[3]
        dist = math.sqrt((n['x']-ca['x'])**2 + (n['y']-ca['y'])**2 + (n['z']-ca['z'])**2)
        ks = dist / k_modulus
        res_pos = ks * container_mode
        
        # Determine closest harmonic shelf (7 or 13)
        target_shelf = 7 if abs(res_pos - 7) < abs(res_pos - 13) else 13
        deviation = abs(res_pos - target_shelf)

        results.append({
            "name": name, "dist": round(dist, 4), "scalar": round(ks, 6),
            "shelf": target_shelf, "deviation": round(deviation, 6)
        })
        
        print(f"{name:<15} | {dist:<8.4f} | {ks:<8.6f} | {target_shelf:<5} | {deviation:<8.6f}")

    with open(output_path, "w") as out:
        out.write(json.dumps(results, indent=4))

if __name__ == "__main__":
    run_fleet_resonance()