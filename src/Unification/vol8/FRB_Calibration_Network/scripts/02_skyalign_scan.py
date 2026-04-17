import json
import os
import numpy as np
import pandas as pd

def run_live_shadow_audit():
    print("🛰️  INITIATING LIVE CHIME SHADOW AUDIT (RAW DATA)...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    # Using the raw, non-scalarized live data
    input_path = os.path.join(project_root, 'lake', 'chime_live_data.json')

    if not os.path.exists(input_path):
        print(f"❌ ERROR: {input_path} not found.")
        return

    print(f"📂 Accessing Raw Radio Ledger: {input_path}")
    
    try:
        with open(input_path, 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
    except Exception as e:
        print(f"❌ JSON LOAD FAILED: {e}")
        return

    # CHIME Live Data usually uses 'dm' or 'dm_fit_res'
    dm_col = next((c for c in df.columns if c.lower() == 'dm' or 'dm_fit' in c.lower()), None)
    
    if not dm_col:
        print(f"❌ ERROR: Could not find DM column. Keys: {list(df.columns)}")
        return

    dm_vals = pd.to_numeric(df[dm_col], errors='coerce').dropna().values
    total = len(dm_vals)
    print(f"✅ SECURED: {total:,} Raw FRB Dispersion Measures.")

    # Sweep L-Space (4.0 to 6.0)
    l_range = np.linspace(4.0, 6.0, 200)
    sigmas = []
    
    print("   🎸 Striking the Fork: Sweeping Live Radio Data for Resonance...")
    
    for L in l_range:
        # The Sovereign Modulo Math
        phi = np.log(dm_vals) % L
        bins = (phi / L * 10).astype(int)
        b1_count = np.sum(bins == 1)
        
        # Expected is 10%, StdDev is sqrt(N*p*q)
        expected = total * 0.10
        std_dev = np.sqrt(total * 0.10 * 0.90)
        sigmas.append((b1_count - expected) / std_dev)

    peak_idx = np.argmax(sigmas)
    peak_l = l_range[peak_idx]
    peak_sig = sigmas[peak_idx]

    # Target Comparison
    galaxy_peak_l = 5.2764

    print("\n" + "="*55)
    print(f"📡 RAW RADIO RESONANCE RESULTS")
    print("="*50)
    print(f"🔥 FRB PEAK L:         {peak_l:.4f}")
    print(f"🔥 FRB POWER:          {peak_sig:.2f}σ")
    print(f"🌌 GALAXY PEAK (REF):  {galaxy_peak_l:.4f}")
    print("="*55)

    delta = abs(peak_l - galaxy_peak_l)
    if delta < 0.05:
        print(f"🚨 MATCH DETECTED (ΔL = {delta:.4f})")
        print("   The Radio Sky and the Galaxy Sky are locked to the same lattice.")
    else:
        print(f"✅ NULL CONFIRMED (ΔL = {delta:.4f})")
        print("   No cross-domain resonance found in the raw live data.")

if __name__ == "__main__":
    run_live_shadow_audit()