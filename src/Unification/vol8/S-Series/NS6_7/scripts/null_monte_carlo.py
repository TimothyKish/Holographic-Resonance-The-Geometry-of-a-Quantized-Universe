import json
import random
import math
import os
import numpy as np

# 🛡️ NS6_28: THE MONTE CARLO NULL-VALIDATOR
# -----------------------------------------------------------
def run_monte_carlo(iterations=1000):
    L = 16.0 / math.pi
    ANCHOR = 6.6069e10
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_path = os.path.join(project_root, 'lake', 'Master_Galaxy_Vol5.jsonl')
    
    print(f"🎲 INITIATING 1,000-SCRAMBLE MONTE CARLO")
    print("Establishing the true mathematical baseline...")

    # Load the real physics ranges to keep the scramble "contained"
    v_disps, mags, zs = [], [], []
    with open(input_path, 'r') as f:
        for line in f:
            d = json.loads(line)
            v_disps.append(float(d['Vdisp']))
            mags.append(float(d['rpmag']))
            zs.append(float(d['zsp']))

    total_n = len(v_disps)
    expected = total_n / 10.0
    null_chi_squares = []

    for i in range(iterations):
        # Scramble the pools
        random.shuffle(v_disps)
        random.shuffle(mags)
        
        bins = {k: 0 for k in range(10)}
        for v, m in zip(v_disps, mags):
            lum = 10**((25 - m) / 2.5)
            ks = ((v**4) / lum) / ANCHOR
            phi = math.log(ks) % L
            bin_idx = min(int((phi / L) * 10), 9)
            bins[bin_idx] += 1
            
        # Calc Chi-Square for this scramble
        chi = sum([((bins[b] - expected)**2) / expected for b in range(10)])
        null_chi_squares.append(chi)
        
        if (i + 1) % 100 == 0:
            print(f"  ... {i+1} scrambles complete ...")

    mu = np.mean(null_chi_squares)
    std = np.std(null_chi_squares)
    
    real_chi2 = 9845.45 # From our previous run
    true_sigma = (real_chi2 - mu) / std

    print(f"\n==================================================")
    print(f"📊 MONTE CARLO RESULTS (N = {total_n:,})")
    print(f"==================================================")
    print(f"Null Mean Chi2 (μ) : {mu:.2f}")
    print(f"Null Std Dev   (σ) : {std:.2f}")
    print(f"Real Lake Chi2     : {real_chi2:.2f}")
    print(f"--------------------------------------------------")
    print(f"TRUE SIGNIFICANCE  : {true_sigma:.2f} σ")
    print(f"==================================================")

if __name__ == "__main__":
    run_monte_carlo()
    input("\nPress ENTER to close...")