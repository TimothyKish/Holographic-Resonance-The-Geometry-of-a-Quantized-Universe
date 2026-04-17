import json
import os
import numpy as np

def run_l_sweep():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_path = os.path.join(project_root, 'lake', 'Master_Stellar_Gaia_Standard.jsonl')
    
    if not os.path.exists(input_path):
        print(f"❌ Error: {input_path} not found.")
        return

    # Extract all distances into memory for speed
    print("🛰️  LOADING STELLAR DISTANCES...")
    distances = []
    with open(input_path, 'r') as f:
        for line in f:
            distances.append(json.loads(line)['dist_pc'])
    
    distances = np.array(distances)
    
    # Mondy's L-Sweep Range
    test_values = [4.0, 4.5, 5.093, 5.5, 6.0, 6.5]
    
    print("\n" + "="*50)
    print(f"{'L Value':<10} | {'Peak Bin':<10} | {'Peak %':<10} | {'Status'}")
    print("-" * 50)

    for L in test_values:
        # Re-scalarize with the test L
        phi = np.log(distances) % L
        bins = (phi / L * 10).astype(int)
        bins = np.clip(bins, 0, 9)
        
        counts = np.bincount(bins, minlength=10)
        peak_bin = np.argmax(counts)
        peak_pct = (counts[peak_bin] / len(distances)) * 100
        
        # Check for 16/pi specificity
        status = "TARGET" if L == 5.093 else "NULL"
        print(f"{L:<10.3f} | {peak_bin:<10} | {peak_pct:<9.2f}% | {status}")

    print("="*50)

if __name__ == "__main__":
    run_l_sweep()