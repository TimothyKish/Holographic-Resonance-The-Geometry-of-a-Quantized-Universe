import os
import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture

def run_mixture_audit():
    print("🛡️  INITIATING KINEMATIC MIXTURE AUDIT (ROBUST PATHING)...")
    
    # --- DYNAMIC PATH DISCOVERY ---
    # We look for the ledger in common locations relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    potential_paths = [
        # If run from FRB_Calibration_Network/scripts
        os.path.join(script_dir, '..', '..', 'S-Series', 'NS6_7', 'lake', 'Master_Galaxy_Vol6_2.csv'),
        # If run from S-Series/scripts
        os.path.join(script_dir, '..', 'NS6_7', 'lake', 'Master_Galaxy_Vol6_2.csv'),
        # Absolute fallback (Current Dir)
        'Master_Galaxy_Vol6_2.csv'
    ]
    
    ledger = None
    for p in potential_paths:
        if os.path.exists(p):
            ledger = p
            break
            
    if not ledger:
        print("❌ ERROR: Ledger not found. Please ensure Master_Galaxy_Vol6_2.csv is in S-Series/NS6_7/lake/")
        return
        
    print(f"📂 Found Ledger: {ledger}")
    
    # --- DATA LOADING ---
    try:
        df = pd.read_csv(ledger, on_bad_lines='skip')
        v_col = next((c for c in df.columns if c.lower() in ['vdisp', 'v', 'sigma']), None)
        v_data = pd.to_numeric(df[v_col], errors='coerce').dropna()
        # Focus on the "Physical Heart" of the distribution
        v_phys = v_data[(v_data > 40) & (v_data < 450)].values
    except Exception as e:
        print(f"❌ FAILED TO READ DATA: {e}")
        return
    
    ln_v = np.log(v_phys).reshape(-1, 1)
    print(f"✅ Loaded {len(ln_v):,} kinematic signatures.")

    # --- THE BIC TEST (Bayesian Information Criterion) ---
    # This is the "Phoenix Filter": It penalizes over-fitting.
    # If BIC is lowest at n=1, Phoenix wins.
    print("📊 Stripping the Log-Space... testing 1 to 5 populations...")
    
    best_bic = np.inf
    best_n = 0
    best_model = None

    for n in range(1, 6):
        gmm = GaussianMixture(n_components=n, random_state=42, n_init=3)
        gmm.fit(ln_v)
        bic = gmm.bic(ln_v)
        print(f"   n={n} | BIC Score: {bic:,.2f}")
        
        if bic < best_bic:
            best_bic = bic
            best_n = n
            best_model = gmm

    print(f"\n🔥 WINNING MODEL: {best_n} Population(s)")
    
    # --- NODE EXTRACTION ---
    means = np.exp(best_model.means_.flatten())
    weights = best_model.weights_
    
    print("\n" + "="*50)
    print(f"🧬 DETECTED KINEMATIC NODES (km/s)")
    print("="*50)
    for i in range(best_n):
        print(f"Node {i+1}: {means[i]:>6.2f} km/s | Weight: {weights[i]*100:>5.2f}%")
    print("="*50)

    print("\n📝 PHOENIX VERDICT:")
    if best_n == 1:
        print("   The distribution is a single smooth lognormal 'Ghost'.")
        print("   The structure in the modulo test was a mathematical artifact.")
    else:
        print(f"   The universe is MULTI-MODAL ({best_n} distinct mass-classes).")
        print("   The 361-Sigma result is driven by real physical gaps between")
        print("   these discrete galaxy populations.")

if __name__ == "__main__":
    run_mixture_audit()