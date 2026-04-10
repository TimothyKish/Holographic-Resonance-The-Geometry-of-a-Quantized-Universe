import json
import os
import numpy as np
import pandas as pd

def run_physical_stellar_sweep():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    lake_dir = os.path.join(project_root, 'lake')
    
    # We need the original CSVs to get Proper Motion (pmra, pmdec) and Magnitude (phot_g_mean_mag)
    sectors = ['NW', 'NE', 'SW', 'SE']
    
    print("🛰️  LOADING PHYSICAL STELLAR ATTRIBUTES (Proper Motion + Flux)...")
    
    mu_total = []
    mags = []
    
    for s in sectors:
        path = os.path.join(lake_dir, f'Gaia_Sector_{s}.csv')
        if not os.path.exists(path): continue
        
        # Note: Ensure your Gaia pull included 'pmra', 'pmdec', and 'phot_g_mean_mag'
        # If not, we may need a quick re-pull of these specific columns.
        df = pd.read_csv(path)
        
        # Calculate Total Proper Motion: mu = sqrt(pmra^2 + pmdec^2)
        if 'pmra' in df.columns and 'pmdec' in df.columns:
            mu = np.sqrt(df['pmra']**2 + df['pmdec']**2)
            mu_total.extend(mu.tolist())
            mags.extend(df['phot_g_mean_mag'].tolist())

    if not mu_total:
        print("❌ Error: Proper Motion columns missing. Need to pull 'pmra' and 'pmdec'.")
        return

    mu_total = np.array(mu_total)
    mags = np.array(mags)
    
    # Calculate Stellar Flux (Luminosity Analog)
    flux = 10**((25 - mags) / 2.5)
    
    # The Stellar Faber-Jackson Analog: (mu^4 / flux) / STELLAR_ANCHOR
    STELLAR_ANCHOR = 1.0 # Initial baseline
    val_stellar = (mu_total**4 / flux) / STELLAR_ANCHOR
    
    # Remove zeros or NaNs
    val_stellar = val_stellar[val_stellar > 0]
    
    test_values = [4.0, 4.5, 5.093, 5.5, 6.0, 6.5]
    
    print("\n" + "="*60)
    print(f"{'L Value':<10} | {'Peak Bin':<10} | {'Peak %':<10} | {'Status'}")
    print("-" * 60)

    for L in test_values:
        phi = np.log(val_stellar) % L
        bins = (phi / L * 10).astype(int)
        bins = np.clip(bins, 0, 9)
        
        counts = np.bincount(bins, minlength=10)
        peak_bin = np.argmax(counts)
        peak_pct = (counts[peak_bin] / len(val_stellar)) * 100
        
        status = "TARGET" if L == 5.093 else "NULL"
        print(f"{L:<10.3f} | {peak_bin:<10} | {peak_pct:<9.2f}% | {status}")

    print("="*60)

if __name__ == "__main__":
    run_physical_stellar_sweep()