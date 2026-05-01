import json
import os
import numpy as np

def run_q_l_sweep():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(project_root, 'lake', 'q1_spectra_promoted.jsonl')
    
    scalars = []
    with open(input_path, 'r') as f:
        for line in f:
            scalars.append(json.loads(line)['scalar'])
    
    scalars = np.array(scalars)
    test_L = [4.0, 4.5, 5.0, 5.093, 5.2, 5.5, 6.0]
    
    print("\n" + "="*60)
    print(f"{'L Value':<10} | {'Peak Bin':<10} | {'Peak %':<10} | {'Status'}")
    print("-" * 60)

    for L in test_L:
        phi = np.log(scalars) % L
        bins = (phi / L * 10).astype(int)
        bins = np.clip(bins, 0, 9)
        
        counts = np.bincount(bins, minlength=10)
        peak_bin = np.argmax(counts)
        peak_pct = (counts[peak_bin] / len(scalars)) * 100
        
        status = "TARGET" if abs(L - 5.093) < 0.01 else "NULL"
        print(f"{L:<10.3f} | {peak_bin:<10} | {peak_pct:<9.2f}% | {status}")
    print("="*60)

if __name__ == "__main__":
    run_q_l_sweep()