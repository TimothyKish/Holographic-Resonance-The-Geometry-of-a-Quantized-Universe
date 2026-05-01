import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def run_tuning_fork():
    print("🛰️  INITIATING KINEMATIC TUNING FORK (L-SWEEP)...")
    
    base_dir = os.getcwd()
    ledger = os.path.join(base_dir, 'NS6_7', 'lake', 'Master_Galaxy_Vol6_2.csv')
    
    if not os.path.exists(ledger):
        print(f"❌ ERROR: Ledger not found.")
        return
        
    # Load raw velocities
    df = pd.read_csv(ledger, on_bad_lines='skip')
    v_col = next((c for c in df.columns if c.lower() in ['vdisp', 'v', 'sigma']), None)
    df[v_col] = pd.to_numeric(df[v_col], errors='coerce')
    v_data = df[df[v_col] > 10][v_col].values # Filter noise below 10 km/s
    
    total = len(v_data)
    print(f"✅ Loaded {total:,} kinematic signatures.")

    # Constants
    ANCHOR = 6.6069e10
    M_CONSTANT = 18.0
    LUM_CONSTANT = 10**((25 - M_CONSTANT) / 2.5)
    
    # Pre-calculate natural logs to speed up the sweep
    ln_scalars = np.log(((v_data**4) / LUM_CONSTANT) / ANCHOR)
    
    # Sweep Range: 4.0 to 6.0
    l_range = np.linspace(4.0, 6.0, 200)
    sigmas = []
    
    print("   🎸 Striking the Fork: Sweeping L-Space for Resonance...")
    
    for L in l_range:
        # Calculate bins for this specific L
        phi = ln_scalars % L
        bins = (phi / L * 10).astype(int)
        
        # Measure Bin 1 excess
        b1_count = np.sum(bins == 1)
        
        # Simple Sigma Calculation (Observed - Expected) / StdDev
        # Expected is 10%, StdDev for binomial is sqrt(N * p * q)
        expected = total * 0.10
        std_dev = np.sqrt(total * 0.10 * 0.90)
        
        sigma = (b1_count - expected) / std_dev
        sigmas.append(sigma)

    # 1. Output the Full 10-Bin Vector for the target L (16/pi)
    L_target = 16.0 / np.pi
    target_phi = ln_scalars % L_target
    target_bins = (target_phi / L_target * 10).astype(int)
    bin_counts = [np.sum(target_bins == i) for i in range(10)]
    bin_pcts = [(c / total) * 100 for c in bin_counts]

    print("\n" + "="*50)
    print(f"🎯 RESULTS AT SOVEREIGN FREQUENCY (L = {L_target:.4f})")
    print("="*50)
    for i, pct in enumerate(bin_pcts):
        bar = "█" * int(pct)
        print(f"Bin {i}: {pct:05.2f}% {bar}")
    print("="*50)

    # 2. Find the peak L in the sweep
    peak_idx = np.argmax(sigmas)
    print(f"🔥 SWEEP PEAK: L = {l_range[peak_idx]:.4f} (Power: {sigmas[peak_idx]:.2f}σ)")
    
    # 3. Optional: Save a quick text plot for the console
    print("\n📈 L-SWEEP RESONANCE GRAPH:")
    max_sig = max(sigmas)
    for i in range(0, len(l_range), 10):
        norm_sig = int((sigmas[i] / max_sig) * 40) if max_sig > 0 else 0
        print(f"L={l_range[i]:.2f} | {'#' * norm_sig}")

if __name__ == "__main__":
    run_tuning_fork()