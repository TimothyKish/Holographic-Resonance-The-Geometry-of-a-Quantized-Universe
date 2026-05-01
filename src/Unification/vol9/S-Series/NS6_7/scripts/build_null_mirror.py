import json
import random
import math
import os
import time
from collections import Counter

# 🛡️ NS6_21: THE NULL MIRROR GENERATOR
# -----------------------------------------------------------
# Goal: Create the "Ghost Lake" control dataset by randomizing 
#       the physics while keeping the spatial coordinates real.

def generate_null_lake():
    L = 16.0 / math.pi
    ANCHOR = 6.6069e10 
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    source_path = os.path.join(project_root, 'lake', 'Master_Galaxy_Vol5.jsonl')
    null_path = os.path.join(project_root, 'lake', 'Master_Galaxy_Null_Vol5.jsonl')
    
    print("💀 INITIATING GHOST LAKE GENERATION")
    print(f"Source: {os.path.basename(source_path)}")
    print(f"Output: {os.path.basename(null_path)}\n")
    
    if not os.path.exists(source_path):
        print(f"❌ ERROR: Could not find {source_path}")
        return

    processed = 0
    bin_counts = Counter()
    start_time = time.time()
    
    with open(source_path, 'r', encoding='utf-8') as infile, \
         open(null_path, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            try:
                data = json.loads(line)
                
                # 1. Randomize the Physics within the SDSS bounds
                # Vdisp: 70 to 400 km/s
                # rpmag: 13 to 22 (typical visible Sloan limits)
                # zsp: 0.01 to 0.70
                rand_vdisp = random.uniform(70.0, 400.0)
                rand_rpmag = random.uniform(13.0, 22.0)
                rand_zsp = random.uniform(0.01, 0.70)
                
                # 2. Recalculate the 16/pi Physics
                lum = 10**((25 - rand_rpmag) / 2.5)
                ks = ((rand_vdisp**4) / lum) / ANCHOR
                phi = math.log(ks) % L
                bin_idx = min(int((phi / L) * 10), 9)
                
                # 3. Inject the "Null" values back into the JSON
                data['Vdisp'] = round(rand_vdisp, 3)
                data['rpmag'] = round(rand_rpmag, 3)
                data['zsp'] = round(rand_zsp, 5)
                data['kish_phi'] = round(phi, 6)
                data['kish_bin'] = bin_idx
                data['vol5_status'] = "NULL_CONTROL"
                
                # 4. Save and count
                outfile.write(json.dumps(data) + '\n')
                bin_counts[bin_idx] += 1
                processed += 1
                
            except json.JSONDecodeError:
                continue

    elapsed = time.time() - start_time
    print(f"🏆 GHOST LAKE BUILT: {processed:,} synthetic probes generated in {elapsed:.2f}s")
    print("--------------------------------------------------")
    print("📊 THE NULL MIRROR PHASE DISTRIBUTION:")
    
    # Print the Null Histogram
    for i in range(10):
        count = bin_counts.get(i, 0)
        percentage = (count / processed) * 100 if processed > 0 else 0
        bar = '▒' * int(percentage)
        print(f"Bin {i}: [{count:7d}] | {percentage:05.2f}% | {bar}")
        
    print("--------------------------------------------------")

if __name__ == "__main__":
    try:
        generate_null_lake()
    except Exception as e:
        import traceback
        print("\n❌ CRITICAL SYSTEM CRASH:")
        traceback.print_exc()
    finally:
        input("\nPress ENTER to close this window...")