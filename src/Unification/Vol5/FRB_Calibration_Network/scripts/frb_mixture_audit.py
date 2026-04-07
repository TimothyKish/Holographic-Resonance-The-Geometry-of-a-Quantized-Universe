import json
import os
import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture

def run_frb_mixture_audit():
    print("🛡️  INITIATING FRB MIXTURE AUDIT (DISPERSION DISSECTION)...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_path = os.path.join(project_root, 'lake', 'chime_live_data.json')

    if not os.path.exists(input_path):
        print(f"❌ ERROR: {input_path} not found.")
        return

    # 1. LOAD DATA
    with open(input_path, 'r') as f:
        df = pd.DataFrame(json.load(f))
    
    # Targeting the high-fidelity fit
    dm_vals = pd.to_numeric(df['dm_fitb'], errors='coerce').dropna().values
    ln_dm = np.log(dm_vals).reshape(-1, 1)
    
    print(f"✅ Loaded {len(ln_dm):,} Raw Radio Signatures.")
    print("📊 Stripping the Log-DM Space... testing 1 to 5 populations...")

    # 2. THE BIC TEST (Bayesian Information Criterion)
    best_bic = np.inf
    best_n = 0
    best_model = None

    for n in range(1, 6):
        gmm = GaussianMixture(n_components=n, random_state=42, n_init=3)
        gmm.fit(ln_dm)
        bic = gmm.bic(ln_dm)
        print(f"   n={n} | BIC Score: {bic:,.2f}")
        
        if bic < best_bic:
            best_bic = bic
            best_n = n
            best_model = gmm

    print(f"\n🔥 WINNING FRB MODEL: {best_n} Population(s)")
    
    # 3. NODE EXTRACTION (Dispersion Centers)
    means = np.exp(best_model.means_.flatten())
    weights = best_model.weights_
    
    print("\n" + "="*50)
    print(f"🧬 DETECTED RADIO NODES (pc/cm³)")
    print("="*50)
    for i in range(best_n):
        print(f"Node {i+1}: {means[i]:>7.2f} DM | Weight: {weights[i]*100:>5.2f}%")
    print("="*50)

    print("\n📝 PHOENIX PRE-AUDIT NOTE:")
    if best_n > 1:
        print(f"   The radio sky is structured into {best_n} discrete shells.")
        print("   This mirrors the multi-modal architecture of the galaxies.")
    else:
        print("   The radio sky is a single smooth distribution.")

if __name__ == "__main__":
    run_frb_mixture_audit()