# B1_S4_S8_Chirality_Fleet_Resonance.py
# LADDER STEP: 4 (SCALAR) & 8 (RESONANCE)
# TARGET: FULL 20 MIRROR FLEET (INCLUDING GHOST GLYCINE)

import json
import math
import os
import glob

def run_mirror_fleet_resonance():
    lake_dir = "../Lake/"
    output_path = "../Processed/B1_S4_S8_Mirror_Audit.json"
    k_modulus = 16 / math.pi
    container_mode = 24
    
    lake_files = glob.glob(os.path.join(lake_dir, "*.jsonl"))
    results = []

    print(f"\n{'Mirror Acid':<25} | {'Dist':<8} | {'Scalar':<8} | {'Shelf':<5} | {'Dev':<8}")
    print("-" * 75)

    for file_path in lake_files:
        with open(file_path, 'r') as f:
            data = json.loads(f.readline())
        
        name = data['name']
        coords = data['coords']
        # Check if it's our synthetic intruder
        is_simulated = "SIMULATED" in data.get('metadata', '') or "Simulated" in name
        
        try:
            # We target the Nitrogen-to-Alpha-Carbon bond
            # In standard B-Series ingestion, these are usually at indices 2 and 3
            n, ca = coords[2], coords[3]
            dist = math.sqrt((n['x']-ca['x'])**2 + (n['y']-ca['y'])**2 + (n['z']-ca['z'])**2)
            ks = dist / k_modulus
            res_pos = ks * container_mode
            
            # Shelf Logic: 7 (Backbone) or 13 (Sidechain influence)
            target_shelf = 7 if abs(res_pos - 7) < abs(res_pos - 13) else 13
            deviation = abs(res_pos - target_shelf)

            display_name = f"*{name}" if is_simulated else name

            results.append({
                "name": name, 
                "dist": round(dist, 6), 
                "scalar": round(ks, 6),
                "shelf": target_shelf, 
                "deviation": round(deviation, 6),
                "simulated": is_simulated
            })
            
            print(f"{display_name:<25} | {dist:<8.4f} | {ks:<8.6f} | {target_shelf:<5} | {deviation:<8.6f}")
        except Exception as e:
            print(f"Error processing {name}: {e}")

    # Sort results for the report
    results.sort(key=lambda x: x['name'])

    with open(output_path, "w") as out:
        out.write(json.dumps(results, indent=4))
    print(f"\n[!] Audit complete. 20-mode Mirror Fleet mapped to Processed folder.")

if __name__ == "__main__":
    run_mirror_fleet_resonance() # Removed the colon grit