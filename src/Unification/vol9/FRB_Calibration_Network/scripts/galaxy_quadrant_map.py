import os
import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture

def run_quadrant_mixture_map():
    print("🛡️  INITIATING GALAXY QUADRANT MIXTURE MAP (FORCE-PATH)...")
    
    # --- PATH RECOVERY ---
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Moving up from 'scripts' to 'FRB_Calibration_Network' to 'vol5'
    vol5_dir = os.path.dirname(os.path.dirname(script_dir))
    
    ledger = os.path.join(vol5_dir, 'S-Series', 'NS6_7', 'lake', 'Master_Galaxy_Vol6_2.csv')
    
    if not os.path.exists(ledger):
        print(f"❌ ERROR: Ledger not found at {ledger}")
        print("Searching for any .csv in S-Series/NS6_7/lake...")
        return
        
    print(f"📂 Accessing Ledger: {ledger}")
    
    # --- DATA LOADING ---
    try:
        df = pd.read_csv(ledger, on_bad_lines='skip')
        # Standardizing column names
        df.columns = [c.strip() for c in df.columns]
        v_col = next((c for c in df.columns if c.lower() in ['vdisp', 'v', 'sigma']), None)
        s_col = next((c for c in df.columns if c.lower() in ['sector', 'quadrant']), None)
        
        if not v_col or not s_col:
            print(f"❌ ERROR: Missing columns. Found: {list(df.columns)}")
            return

        df[v_col] = pd.to_numeric(df[v_col], errors='coerce')
        df = df[(df[v_col] > 40) & (df[v_col] < 450)].dropna(subset=[v_col, s_col])
    except Exception as e:
        print(f"❌ FAILED TO READ DATA: {e}")
        return
    
    sectors = sorted(df[s_col].unique())
    print(f"✅ Data Ready. Sectors identified: {sectors}")
    print("📊 Fitting 5-Node Mixture Models to each quadrant...")

    results = {}

    for sec in sectors:
        sec_data = df[df[s_col] == sec][v_col].values
        if len(sec_data) < 100: continue # Skip empty or tiny sectors
        
        ln_v = np.log(sec_data).reshape(-1, 1)
        
        # Fit the GMM
        gmm = GaussianMixture(n_components=5, random_state=42, n_init=2)
        gmm.fit(ln_v)
        
        # Sort means (Smallest to Largest)
        means = np.exp(np.sort(gmm.means_.flatten()))
        results[sec] = means
        print(f"   Sector {sec:<4} | n={len(sec_data):<7} | Nodes: {', '.join([f'{m:.1f}' for m in means])}")

    if not results:
        print("❌ ERROR: No sectors processed.")
        return

    print("\n" + "="*75)
    print(f"{'Sector':<10} | {'Node 1':<9} | {'Node 2':<9} | {'Node 3':<9} | {'Node 4':<9} | {'Node 5':<9}")
    print("-" * 75)
    for sec, nodes in results.items():
        print(f"{sec:<10} | {nodes[0]:<9.1f} | {nodes[1]:<9.1f} | {nodes[2]:<9.1f} | {nodes[3]:<9.1f} | {nodes[4]:<9.1f}")
    print("="*75)

    # Global Stability Analysis
    all_nodes = np.array(list(results.values()))
    std_devs = np.std(all_nodes, axis=0)
    
    print(f"\n📈 INTER-QUADRANT STABILITY (Std Dev km/s):")
    for i, sd in enumerate(std_devs):
        print(f"   Node {i+1}: {sd:.2f} km/s")

if __name__ == "__main__":
    run_quadrant_mixture_map()