import json
import os
import numpy as np

def run_quantum_sigma_audit():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(project_root, 'lake', 'q1_spectra_promoted.jsonl')
    
    L = 5.092958 # 16/pi
    scalars = []
    with open(input_path, 'r') as f:
        for line in f:
            scalars.append(json.loads(line)['scalar'])
    
    scalars = np.array(scalars)
    N = len(scalars)
    
    # 1. Real Chi-Squared
    phi_real = np.log(scalars) % L
    bins_real = (phi_real / L * 10).astype(int)
    counts_real = np.bincount(np.clip(bins_real, 0, 9), minlength=10)
    expected = N / 10.0
    chi2_real = sum((counts_real - expected)**2 / expected)
    
    # 2. Scrambled Null (1000 iterations)
    print(f"🎲 SCRAMBLING QUANTUM NULL (N={N}, Iterations=1000)...")
    null_chi2s = []
    for _ in range(1000):
        # We scramble the log-space to see if the binning is specific to these ratios
        shuffled = np.random.choice(scalars, size=N, replace=True)
        phi_null = np.log(shuffled) % L
        bins_null = (phi_null / L * 10).astype(int)
        counts_null = np.bincount(np.clip(bins_null, 0, 9), minlength=10)
        null_chi2s.append(sum((counts_null - expected)**2 / expected))
    
    mean_null = np.mean(null_chi2s)
    std_null = np.std(null_chi2s)
    sigma = (chi2_real - mean_null) / std_null
    
    print("\n" + "="*45)
    print(f"📊 QUANTUM SIGMA AUDIT")
    print("-" * 45)
    print(f"Target Bin:          7")
    print(f"Real Chi2:           {chi2_real:.2f}")
    print(f"Null Mean Chi2:      {mean_null:.2f}")
    print(f"STATISTICAL POWER:   {sigma:.2f}σ")
    print("="*45)

if __name__ == "__main__":
    run_quantum_sigma_audit()