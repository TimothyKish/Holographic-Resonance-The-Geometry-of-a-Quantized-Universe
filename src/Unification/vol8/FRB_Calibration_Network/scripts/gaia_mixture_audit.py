import os
import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture

def run_gaia_mixture_audit():
    print("🛡️  INITIATING GAIA TRANSVERSE MIXTURE AUDIT (2D KINEMATICS)...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    vol5_dir = os.path.dirname(os.path.dirname(script_dir))
    gaia_lake_dir = os.path.join(vol5_dir, 'S-Series', 'NS6_7', 'lake')
    
    sector_files = [f for f in os.listdir(gaia_lake_dir) if f.startswith('Gaia_Physical_') and f.endswith('.csv')]
    
    all_vt = []

    for f in sector_files:
        path = os.path.join(gaia_lake_dir, f)
        try:
            df = pd.read_csv(path, on_bad_lines='skip')
            # 1. CLEAN DATA
            df['pmra'] = pd.to_numeric(df['pmra'], errors='coerce')
            df['pmdec'] = pd.to_numeric(df['pmdec'], errors='coerce')
            df['parallax'] = pd.to_numeric(df['parallax'], errors='coerce')
            
            # Filter for positive parallax (measurable distance)
            df = df[df['parallax'] > 0.1].dropna(subset=['pmra', 'pmdec', 'parallax'])
            
            # 2. CALCULATE TOTAL PROPER MOTION (mu)
            mu = np.sqrt(df['pmra']**2 + df['pmdec']**2)
            
            # 3. CONVERT TO TRANSVERSE VELOCITY (km/s)
            vt = 4.74 * (mu / df['parallax'])
            
            # 4. FILTER FOR LOCAL STELLAR SPEEDS (10 to 400 km/s)
            vt_phys = vt[(vt > 10) & (vt < 400)].values
            all_vt.extend(vt_phys)
        except Exception as e:
            continue

    if not all_vt:
        print("❌ ERROR: No valid Transverse Velocity data calculated.")
        return

    v_total = np.array(all_vt)
    ln_v = np.log(v_total).reshape(-1, 1)
    print(f"✅ SUCCESS: Loaded {len(v_total):,} Stellar Transverse Signatures.")

    # --- THE BIC TEST ---
    print("📊 Testing 1 to 5 Populations...")
    best_bic, best_n, best_model = np.inf, 0, None

    for n in range(1, 6):
        gmm = GaussianMixture(n_components=n, random_state=42, n_init=2)
        gmm.fit(ln_v)
        bic = gmm.bic(ln_v)
        print(f"   n={n} | BIC Score: {bic:,.2f}")
        if bic < best_bic:
            best_bic, best_n, best_model = bic, n, gmm

    means = np.exp(np.sort(best_model.means_.flatten()))
    print("\n" + "="*55)
    print(f"🧬 DETECTED STELLAR NODES (km/s)")
    print("="*55)
    for i, m in enumerate(means):
        print(f"Node {i+1}: {m:>7.2f} km/s")
    print("="*55)
    
    # GALAXY TARGET
    print(f"\n🌌 GALAXY INVARIANT REF: 92.7 km/s")

if __name__ == "__main__":
    run_gaia_mixture_audit()