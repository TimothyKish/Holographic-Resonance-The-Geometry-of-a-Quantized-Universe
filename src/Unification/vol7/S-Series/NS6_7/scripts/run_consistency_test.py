import pandas as pd
import numpy as np
import os

# 🛡️ NS6_09: THE RANDOM-SPLIT CONSISTENCY TEST
# -----------------------------------------------------------
# Target: Volume-Limited SDSS Pencil Beam (N=448)
# Goal: Prove the "Staircase" is a population-wide invariant.

def run_consistency_test(file_path):
    # 1. Path Management
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found.")
        return

    # 2. Ingest & Clean
    df = pd.read_csv(file_path, sep='|', comment='#', skipinitialspace=True, low_memory=False)
    df.columns = [c.strip() for c in df.columns]
    df = df.iloc[2:].reset_index(drop=True)
    
    # Correctly rename and cast columns
    df = df.rename(columns={'zsp': 'z', 'Vdisp': 'velDisp', 'DE_ICRS': 'dec', 'RA_ICRS': 'ra'})
    for col in ['z', 'velDisp', 'dec', 'ra']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 3. Mondy's Volume-Limited Cut
    # Note: Using the RENAMED 'velDisp' to avoid KeyError
    vl = df[(df['z'] < 0.10) & (df['velDisp'] > 100)].dropna(subset=['z', 'ra'])
    
    if len(vl) < 100:
        print(f"⚠️ Warning: Small sample size (N={len(vl)}). Consistency test may be noisy.")
    
    # 4. RANDOM SPLIT (The "Internal Consistency" Check)
    # Since the data is all North, we split into two random groups.
    np.random.seed(42)
    shuffled = vl.sample(frac=1).reset_index(drop=True)
    half_a = shuffled.iloc[:len(shuffled)//2]
    half_b = shuffled.iloc[len(shuffled)//2:]
    
    print(f"--- 🛡️ LATTICE CONSISTENCY TEST ---")
    print(f"Total Fleet: {len(vl)} galaxies")
    print(f"Half A: {len(half_a)} galaxies | Half B: {len(half_b)} galaxies")
    
    def get_staircase(data, label):
        counts, bins = np.histogram(data['z'], bins=15)
        print(f"\n[{label}] Redshift Staircase:")
        for i in range(len(counts)):
            bar = "█" * int(counts[i] * 1.5)
            print(f"  z={bins[i]:.4f}: {bar} ({counts[i]})")
        return counts

    counts_a = get_staircase(half_a, "GROUP A")
    counts_b = get_staircase(half_b, "GROUP B")
    
    # 5. CORRELATION CALCULATION
    correlation = np.corrcoef(counts_a, counts_b)[0,1]
    print(f"\n" + "="*40)
    print(f" 🧬 LATTICE CONSISTENCY: {correlation:.4f}")
    print("="*40)
    
    if correlation > 0.80:
        print("🏆 VERDICT: LATTICE INVARIANCE CONFIRMED.")
        print("The Staircase peaks are identical across random samples.")
    else:
        print("🏠 VERDICT: STAIRCASE IS NOISE-DEPENDENT.")
        print("Peaks shifted between samples.")

if __name__ == "__main__":
    # Update this path if you move the script
    run_consistency_test('../lake/asu.tsv')