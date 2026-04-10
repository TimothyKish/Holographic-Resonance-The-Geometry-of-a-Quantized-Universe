import numpy as np
import json
import os
from scipy.stats import chisquare
import math

def run_dual_scramble_final():
    print("🛡️  EXECUTING DUAL SCRAMBLE NULL (REFEREE PROTOCOL - JSONL)")
    
    # --- RIGOROUS PATHING ---
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Up from 'scripts' to 'FRB_Calibration_Network' to 'vol5'
    vol5_root = os.path.dirname(os.path.dirname(script_dir))
    input_path = os.path.join(vol5_root, 'S-Series', 'NS6_7', 'lake', 'Master_Galaxy_Vol6_PHYSICAL.jsonl')
    
    if not os.path.exists(input_path):
        print(f"❌ ERROR: Cannot find file at {input_path}")
        return
        
    L = 16.0 / math.pi
    ANCHOR = 6.6069e10
    
    # 1. LOAD RAW DATA
    v_vals = []
    m_vals = []
    
    print(f"📂 Extracting vectors from {input_path}...")
    with open(input_path, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                # 'v' is Vdisp, 'm' is magnitude
                v_vals.append(data['v'])
                m_vals.append(data['m'])
            except:
                continue
                
    v_vals = np.array(v_vals)
    m_vals = np.array(m_vals)
    N = len(v_vals)
    
    # Clean zeros/NaNs
    mask = (v_vals > 0) & (~np.isnan(v_vals)) & (~np.isnan(m_vals))
    v_vals, m_vals = v_vals[mask], m_vals[mask]
    
    print(f"✅ Loaded {len(v_vals):,} synced galaxy signatures.")

    # 2. CALCULATE REAL CHI-SQUARED
    lum_real = 10**((25 - m_vals) / 2.5)
    val_real = (v_vals**4 / lum_real) / ANCHOR
    phi_real = np.log(val_real[val_real > 0]) % L
    obs_real, _ = np.histogram(phi_real, bins=10, range=(0, L))
    chi2_real, _ = chisquare(f_obs=obs_real, f_exp=np.full(10, len(phi_real)/10.0))
    
    print(f"\n📊 REAL DATA χ²: {chi2_real:.4f}")

    # 3. DUAL SCRAMBLE LOOP (THE GHOST KILLER)
    print(f"🔄 Running 1,000 Dual Scrambles (Shuffling V and M independently)...")
    null_chi2s = []
    
    for i in range(1000):
        # Independent shuffling destroys the Faber-Jackson physical link
        v_shuf = np.random.permutation(v_vals)
        m_shuf = np.random.permutation(m_vals)
        
        lum_s = 10**((25 - m_shuf) / 2.5)
        val_s = (v_shuf**4 / lum_s) / ANCHOR
        phi_s = np.log(val_s[val_s > 0]) % L
        obs_s, _ = np.histogram(phi_s, bins=10, range=(0, L))
        c2, _ = chisquare(f_obs=obs_s, f_exp=np.full(10, len(phi_s)/10.0))
        null_chi2s.append(c2)
        
        if (i+1) % 100 == 0:
            print(f"   Completed {i+1}/1000...")

    null_mean = np.mean(null_chi2s)
    null_std = np.std(null_chi2s)
    final_sigma = (chi2_real - null_mean) / null_std

    print("\n" + "="*55)
    print(f"🏁 FINAL REFEREE VERDICT")
    print("="*55)
    print(f"Real Chi-squared:    {chi2_real:.2f}")
    print(f"Null Mean (Artifact): {null_mean:.2f}")
    print(f"Null Std Dev:        {null_std:.2f}")
    print(f"SIGNAL SIGNIFICANCE: {final_sigma:.2f}σ")
    print("="*55)

    if final_sigma >= 5.0:
        print("🔥 RESULT: THE LATTICE IS PHYSICAL.")
        print("   The signal exists in the RELATIONSHIP between V and M.")
    else:
        print("❄️  RESULT: THE LATTICE IS A LOGNORMAL ARTIFACT.")
        print("   The signal is explained by the distributions alone.")

if __name__ == "__main__":
    run_dual_scramble_final()