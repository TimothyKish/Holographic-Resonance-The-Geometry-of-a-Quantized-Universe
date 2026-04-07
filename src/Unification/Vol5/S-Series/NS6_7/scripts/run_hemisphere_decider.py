import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run_hemisphere_decider(file_path):
    # Load and clean local lake
    df = pd.read_csv(file_path, sep='|', comment='#', skipinitialspace=True, low_memory=False)
    df.columns = [c.strip() for c in df.columns]
    df = df.iloc[2:].reset_index(drop=True)
    df = df.rename(columns={'zsp': 'z', 'Vdisp': 'velDisp', 'DE_ICRS': 'dec'})
    df['z'] = pd.to_numeric(df['z'], errors='coerce')
    df['dec'] = pd.to_numeric(df['dec'], errors='coerce')
    
    # Mondy's Volume-Limited Cut
    vl = df[(df['z'] < 0.10) & (pd.to_numeric(df['Vdisp'], errors='coerce') > 100)].dropna(subset=['z', 'dec'])
    
    # Split by Hemisphere (Declination)
    north = vl[vl['dec'] >= 0]
    south = vl[vl['dec'] < 0]
    
    print(f"--- 🛡️ HEMISPHERE STAIRCASE TEST ---")
    print(f"North Fleet: {len(north)} galaxies")
    print(f"South Fleet: {len(south)} galaxies")
    
    def get_peaks(data, label):
        counts, bins = np.histogram(data['z'], bins=15)
        peak_idx = np.argmax(counts)
        print(f"[{label}] Primary Peak at z ≈ {bins[peak_idx]:.4f}")
        return counts, bins

    n_counts, n_bins = get_peaks(north, "NORTH")
    s_counts, s_bins = get_peaks(south, "SOUTH")
    
    # Check for "Tooth Alignment"
    correlation = np.corrcoef(n_counts, s_counts)[0,1]
    print(f"Hemisphere Correlation: {correlation:.4f}")
    
    if correlation > 0.7:
        print("\n🏆 VERDICT: LATTICE DRAG DETECTED.")
        print("The staircase is UNIVERSAL across sky quadrants.")
    else:
        print("\n🏠 VERDICT: LARGE SCALE STRUCTURE (LSS) DETECTED.")
        print("The staircase is direction-dependent.")

run_hemisphere_decider('../lake/asu.tsv')