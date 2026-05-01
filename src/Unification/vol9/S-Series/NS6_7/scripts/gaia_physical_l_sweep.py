import json
import os
import numpy as np

def run_physical_l_sweep():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_path = os.path.join(project_root, 'lake', 'Master_Stellar_Gaia_PHYSICAL.jsonl')
    
    print("🛰️  LOADING PHYSICAL VALUES...")
    vals = []
    with open(input_path, 'r') as f:
        for line in f:
            vals.append(json.loads(line)['val'])
    
    vals = np.array(vals)
    test_L = [4.0, 4.5, 5.0, 5.093, 5.2, 5.5, 6.0]
    
    print("\n" + "="*60)
    print(f"{'L Value':<10} | {'Peak Bin':<10} | {'Peak %':<10} | {'Status'}")
    print("-" * 60)

    for L in test_L:
        phi = np.log(vals) % L
        bins = (phi / L * 10).astype(int)
        bins = np.clip(bins, 0, 9)
        
        counts = np.bincount(bins, minlength=10)
        peak_bin = np.argmax(counts)
        peak_pct = (counts[peak_bin] / len(vals)) * 100
        
        status = "TARGET" if L == 5.093 else "NULL"
        print(f"{L:<10.3f} | {peak_bin:<10} | {peak_pct:<9.2f}% | {status}")

    print("="*60)

if __name__ == "__main__":
    run_physical_l_sweep()