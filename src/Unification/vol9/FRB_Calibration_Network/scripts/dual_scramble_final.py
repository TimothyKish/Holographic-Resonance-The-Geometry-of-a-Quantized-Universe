import numpy as np
import json
import os
from scipy.stats import chisquare
import math

def run_dual_scramble_subsample():
    print("🛡️  DUAL SCRAMBLE — SUBSAMPLE METHOD (REFEREE PROTOCOL)")
    print("   Targeting N=5,000 for meaningful variance...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    vol5_root = os.path.dirname(os.path.dirname(script_dir))
    input_path = os.path.join(vol5_root, 'S-Series', 'NS6_7', 'lake', 'Master_Galaxy_Vol6_PHYSICAL.jsonl')
    
    L = 16.0 / math.pi
    ANCHOR = 6.6069e10
    SUBSAMPLE_N = 5000   
    N_SCRAMBLES = 1000
    
    # 1. LOAD ALL DATA
    v_all, m_all = [], []
    with open(input_path, 'r') as f:
        for line in f:
            try:
                d = json.loads(line)
                v_all.append(d['v'])
                m_all.append(d['m'])
            except: continue
    
    v_all, m_all = np.array(v_all), np.array(m_all)
    mask = (v_all > 0) & (~np.isnan(v_all)) & (~np.isnan(m_all))
    v_all, m_all = v_all[mask], m_all[mask]
    
    def get_chi2(v, m):
        lum = 10**((25 - m) / 2.5)
        val = (v**4 / lum) / ANCHOR
        phi = np.log(val[val > 0]) % L
        obs, _ = np.histogram(phi, bins=10, range=(0, L))
        exp = np.full(10, len(phi) / 10.0)
        c2, _ = chisquare(f_obs=obs, f_exp=exp)
        return c2
    
    # 2. REAL SUBSAMPLE MEAN (100 trials)
    real_chi2s = [get_chi2(*np.transpose([ (v_all[i], m_all[i]) for i in np.random.choice(len(v_all), SUBSAMPLE_N, replace=False) ])) for _ in range(100)]
    # Optimized sampler
    real_chi2s = []
    for _ in range(100):
        idx = np.random.choice(len(v_all), SUBSAMPLE_N, replace=False)
        real_chi2s.append(get_chi2(v_all[idx], m_all[idx]))
    
    chi2_real_mean = np.mean(real_chi2s)
    print(f"✅ Real Subsample χ² Mean: {chi2_real_mean:.4f}")
    
    # 3. DUAL SCRAMBLE NULL (1000 trials)
    print(f"🔄 Running {N_SCRAMBLES} Dual Scrambles...")
    null_chi2s = []
    for i in range(N_SCRAMBLES):
        idx = np.random.choice(len(v_all), SUBSAMPLE_N, replace=False)
        v_sub, m_sub = v_all[idx].copy(), m_all[idx].copy()
        np.random.shuffle(v_sub)
        np.random.shuffle(m_sub)
        null_chi2s.append(get_chi2(v_sub, m_sub))
        if (i+1) % 250 == 0: print(f"   {i+1}/{N_SCRAMBLES}...")
    
    null_mean, null_std = np.mean(null_chi2s), np.std(null_chi2s)
    sigma = (chi2_real_mean - null_mean) / null_std
    
    print("\n" + "="*55)
    print(f"🏁 FINAL DUAL SCRAMBLE VERDICT")
    print("="*55)
    print(f"Real Subsample χ²:     {chi2_real_mean:.2f}")
    print(f"Scrambled Null Mean:   {null_mean:.2f}")
    print(f"Scrambled Null Std:    {null_std:.2f}")
    print(f"SIGNIFICANCE:          {sigma:.2f}σ")
    print("="*55)

    if sigma >= 5.0:
        print("🔥 RESULT: PHYSICAL SIGNAL CONFIRMED.")
    else:
        print("❄️  RESULT: ARTIFACT CONFIRMED.")

if __name__ == "__main__":
    run_dual_scramble_subsample()