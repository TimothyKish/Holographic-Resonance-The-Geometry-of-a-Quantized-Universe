import json
import os
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

def run_ghost_mirror_audit():
    print("🛡️  INITIATING PHOENIX CONTROL: THE GHOST MIRROR AUDIT...")
    
    # 1. LOAD REAL GALAXY DATA (The Anchor)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    s_series_lake = os.path.join(os.path.dirname(project_root), 'S-Series', 'NS6_7', 'lake')
    gal_path = os.path.join(s_series_lake, 'Master_Galaxy_Vol6_2.csv')
    
    df_gal = pd.read_csv(gal_path, on_bad_lines='skip')
    v_gal = pd.to_numeric(df_gal['Vdisp'], errors='coerce').dropna().values
    
    # 2. LOAD REAL FRB DATA (To Model the Ghost)
    frb_path = os.path.join(project_root, 'lake', 'chime_live_data.json')
    with open(frb_path, 'r') as f:
        df_frb = pd.DataFrame(json.load(f))
    dm_real = pd.to_numeric(df_frb['dm_fitb'], errors='coerce').dropna().values
    
    # 3. GENERATE THE GHOST (Smooth Lognormal Null)
    mu = np.mean(np.log(dm_real))
    sigma = np.std(np.log(dm_real))
    dm_ghost = np.random.lognormal(mean=mu, sigma=sigma, size=len(dm_real))
    
    # THE PARAMETERS
    L_PEAK = 5.3166 
    ANCHOR = 6.6069e10
    M_CONST = 18.0
    LUM_CONST = 10**((25 - M_CONST) / 2.5)

    def get_bins(data, is_galaxy=True):
        if is_galaxy:
            scalars = ((data**4) / LUM_CONST) / ANCHOR
        else:
            scalars = data 
        phi = np.log(scalars) % L_PEAK
        bins = (phi / L_PEAK * 10).astype(int)
        counts = np.bincount(bins, minlength=10)
        return counts / len(data) * 100

    gal_sig = get_bins(v_gal, is_galaxy=True)
    ghost_sig = get_bins(dm_ghost, is_galaxy=False)

    print("\n" + "="*65)
    print(f"{'Bin':<10} | {'Real Galaxy %':<18} | {'Ghost FRB %':<15}")
    print("-" * 65)
    for i in range(10):
        print(f"Bin {i:<7} | {gal_sig[i]:<17.2f} | {ghost_sig[i]:<14.2f}")
    print("="*65)

    # Statistical Correlation
    corr_real = 0.9515 # From our previous run
    corr_ghost, _ = pearsonr(gal_sig, ghost_sig)
    
    print(f"\n📊 RESULTS:")
    print(f"   Real Correlation (Mass vs. Light): {corr_real:.4f}")
    print(f"   Ghost Correlation (Mass vs. Math):  {corr_ghost:.4f}")
    
    print("\n📝 PHOENIX VERDICT:")
    if corr_real > corr_ghost + 0.3:
        print("   ✅ THE LATTICE SURVIVES. The real data has structure that")
        print("   math alone cannot explain. The 0.95 is physical.")
    else:
        print("   ❌ THE LATTICE COLLAPSES. The correlation is a property")
        print("   of the log-modulo transform acting on any lognormal curve.")

if __name__ == "__main__":
    run_ghost_mirror_audit()