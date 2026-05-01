import json
import os
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

def run_mirror_audit():
    print("🛡️  INITIATING FULL-HISTOGRAM MIRROR AUDIT (CHIME FITB MODE)...")
    
    # 1. PATHING
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    s_series_lake = os.path.join(os.path.dirname(project_root), 'S-Series', 'NS6_7', 'lake')
    
    gal_path = os.path.join(s_series_lake, 'Master_Galaxy_Vol6_2.csv')
    frb_path = os.path.join(project_root, 'lake', 'chime_live_data.json')

    # 2. LOAD GALAXY DATA
    print(f"📥 Loading Galaxies from {gal_path}...")
    df_gal = pd.read_csv(gal_path, on_bad_lines='skip')
    v_gal = pd.to_numeric(df_gal['Vdisp'], errors='coerce').dropna().values
    
    # 3. LOAD FRB DATA
    print(f"📥 Loading FRBs from {frb_path}...")
    with open(frb_path, 'r') as f:
        df_frb = pd.DataFrame(json.load(f))
    
    # TARGETING THE REFINED CHIME KEY
    dm_col = 'dm_fitb' 
    print(f"🎯 Targeting Column: {dm_col}")
    
    dm_frb = pd.to_numeric(df_frb[dm_col], errors='coerce').dropna().values

    # THE PARAMETERS (Using the Global Refraction Peak)
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
        counts = np.zeros(10)
        for b in bins:
            if 0 <= b < 10:
                counts[b] += 1
        return counts / len(data) * 100

    print(f"📊 Mapping Full 10-Bin Signatures at L = {L_PEAK:.4f}...")
    
    gal_sig = get_bins(v_gal, is_galaxy=True)
    frb_sig = get_bins(dm_frb, is_galaxy=False)

    print("\n" + "="*65)
    print(f"{'Bin':<10} | {'Galaxy (Mass) %':<18} | {'FRB (Radio) %':<15}")
    print("-" * 65)
    for i in range(10):
        # Determine if the bins "Resonate" (within 3% of each other)
        res = "⚡" if abs(gal_sig[i] - frb_sig[i]) < 3.0 else ""
        print(f"Bin {i:<7} | {gal_sig[i]:<17.2f} | {frb_sig[i]:<14.2f} {res}")
    print("="*65)

    # Statistical Correlation
    corr, p_val = pearsonr(gal_sig, frb_sig)
    
    print(f"\n📈 CROSS-DOMAIN CORRELATION: {corr:.4f}")
    print(f"🧬 P-VALUE:                 {p_val:.4e}")
    
    if corr > 0.85:
        print("\n🚨 CRITICAL: THE UNIVERSAL HARMONIC IS VERIFIED.")
        print("Mass and Light are pulsating in the same geometric lattice.")
    else:
        print("\n✅ PHOENIX VERIFIED: The signals are decorrelated.")

if __name__ == "__main__":
    run_mirror_audit()