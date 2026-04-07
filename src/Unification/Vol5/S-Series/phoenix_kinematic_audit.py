import os
import numpy as np
import pandas as pd
from collections import Counter
import scipy.stats as stats

def run_pure_kinematic_audit():
    print("🛡️  INITIATING PHOENIX v3: THE PURE KINEMATIC AUDIT...")
    
    base_dir = os.getcwd()
    # Using the raw file scouted earlier
    ledger = os.path.join(base_dir, 'NS6_7', 'lake', 'Master_Galaxy_Vol6_2.csv')
    
    if not os.path.exists(ledger):
        print(f"❌ ERROR: Ledger not found at {ledger}")
        return
        
    print(f"📂 Accessing Raw Kinematic Vault: {ledger}")
    
    # Load the data
    try:
        df = pd.read_csv(ledger, on_bad_lines='skip')
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return
        
    # Extract Velocity Dispersion
    v_col = next((c for c in df.columns if c.lower() in ['vdisp', 'v', 'sigma']), None)
    if not v_col:
        print("❌ ERROR: Could not find Velocity column.")
        return
        
    print("   📥 Extracting and cleaning Velocity Dispersions...")
    df[v_col] = pd.to_numeric(df[v_col], errors='coerce')
    actual_v = df[df[v_col] > 0][v_col].values
    total_records = len(actual_v)
    
    if total_records == 0:
        print("❌ ERROR: No valid velocity data.")
        return
        
    print(f"✅ DATA SECURED: {total_records:,} kinematic signatures extracted.")

    # The Sovereign Constants
    L = 16.0 / np.pi
    ANCHOR = 6.6069e10
    M_CONSTANT = 18.0 # The normalized baseline used in the original pipeline
    LUM_CONSTANT = 10**((25 - M_CONSTANT) / 2.5)
    
    # ---------------------------------------------------------
    # CALCULATE THE ACTUAL LATTICE LOCK
    # ---------------------------------------------------------
    actual_scalars = ((actual_v**4) / LUM_CONSTANT) / ANCHOR
    actual_phi = np.log(actual_scalars) % L
    actual_bins = (actual_phi / L * 10).astype(int)
    
    actual_b1_count = np.sum(actual_bins == 1)
    actual_b1_pct = (actual_b1_count / total_records) * 100

    # ---------------------------------------------------------
    # TEST: THE SMOOTH LOG-NORMAL NULL (PHOENIX PROTOCOL)
    # ---------------------------------------------------------
    print("\n" + "="*65)
    print("🛡️ THE SMOOTH KINEMATIC NULL (THE EXECUTIONER)")
    print("Generating a perfectly smooth universe with the exact same")
    print("mean and variance as SDSS, then running the Modulo math.")
    print("="*65)

    # Calculate the shape of the real universe
    log_v = np.log(actual_v)
    mu = np.mean(log_v)
    sigma_v = np.std(log_v)
    
    null_b1_counts = []
    
    # Run 100 Monte Carlo generations of a Smooth Universe
    for _ in range(100):
        # Generate 1.9M smooth, non-quantized velocities
        smooth_v = np.random.lognormal(mean=mu, sigma=sigma_v, size=total_records)
        
        # Run through the exact same invariant math
        smooth_scalars = ((smooth_v**4) / LUM_CONSTANT) / ANCHOR
        smooth_phi = np.log(smooth_scalars) % L
        smooth_bins = (smooth_phi / L * 10).astype(int)
        
        null_b1_counts.append(np.sum(smooth_bins == 1))

    mean_null_b1 = np.mean(null_b1_counts)
    std_null_b1 = np.std(null_b1_counts)
    mean_null_pct = (mean_null_b1 / total_records) * 100
    
    sigma_power = (actual_b1_count - mean_null_b1) / std_null_b1 if std_null_b1 > 0 else 0

    print(f"📊 Actual SDSS Bin 1 Peak:    {actual_b1_pct:.2f}% ({actual_b1_count:,} galaxies)")
    print(f"🎲 Smooth Null Mean Peak:     {mean_null_pct:.2f}% ({int(mean_null_b1):,} galaxies)")
    print(f"📉 Null Standard Dev (σ):     {std_null_b1:,.2f} galaxies")
    print(f"🔥 TRUE STATISTICAL POWER:    {sigma_power:.2f} Sigma")
    
    print("\n📝 PHOENIX REPORT v3:")
    if sigma_power > 5.0:
        print("   The signal survives the Smooth Kinematic Null.")
        print("   The math does not inherently cause the peak. The galaxies")
        print("   themselves are physically clustered at 16/pi harmonic velocities.")
        print("   Kinematic Quantization is Verified.")
    else:
        print("   The peak is easily reproduced by a smooth curve.")
        print("   The signal is a mathematical artifact of the log-modulo function.")
        print("   Framework Rejected.")

if __name__ == "__main__":
    run_pure_kinematic_audit()