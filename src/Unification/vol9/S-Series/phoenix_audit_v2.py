import json
import os
import numpy as np
from collections import Counter
import scipy.stats as stats

def run_phoenix_v2():
    print("🛡️  INITIATING PHOENIX v2 AUDIT (STRICT EMPIRICAL PROTOCOL)...")
    
    base_dir = os.getcwd()
    ledger = os.path.join(base_dir, 'NS6_7', 'lake', 'Master_Galaxy_Vol6_PHYSICAL.jsonl')
    
    if not os.path.exists(ledger):
        print(f"❌ ERROR: Ledger not found at {ledger}")
        return
        
    print(f"📂 Accessing Local Ledger: {ledger}")
    
    # The Sovereign Constants
    L = 16.0 / np.pi
    ANCHOR = 6.6069e10

    # Data arrays for physical recalculation
    sectors = {}
    all_v = []
    all_m = []
    actual_bins = []
    
    print("   📥 Extracting raw physics (Velocity & Magnitude) and decoupling from pre-computed bins...")
    
    with open(ledger, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                v = float(data['v'])
                m = float(data['m'])
                sector = str(data.get('sector', 'Unknown'))
                
                # We need valid physics to recompute
                if v <= 0 or np.isnan(v) or np.isnan(m): continue
                
                all_v.append(v)
                all_m.append(m)
                
                # LIVE RECALCULATION
                lum = 10**((25 - m) / 2.5)
                scalar = ((v**4) / lum) / ANCHOR
                
                if scalar <= 0: continue
                
                phi = np.log(scalar) % L
                kish_bin = int((phi / L) * 10)
                
                actual_bins.append(kish_bin)
                
                if sector not in sectors:
                    sectors[sector] = []
                sectors[sector].append(kish_bin)
                
            except Exception:
                continue

    total_records = len(actual_v := np.array(all_v))
    actual_m = np.array(all_m)
    
    if total_records == 0:
        print("❌ ERROR: No valid physical data found to recalculate.")
        return

    print(f"\n✅ RECALCULATION COMPLETE: {total_records:,} galaxies processed from raw physics.")
    
    # ---------------------------------------------------------
    # TEST 1: SPATIAL ISOTROPY (SECTOR CHI-SQUARE)
    # ---------------------------------------------------------
    print("\n" + "="*65)
    print("🔭 EMPIRICAL TEST 1: SPATIAL ISOTROPY (CHI-SQUARE TEST)")
    print("Testing if Bin 1 excess is uniform across sky sectors.")
    print("="*65)
    
    global_b1_count = actual_bins.count(1)
    global_b1_pct = global_b1_count / total_records
    
    observed_b1 = []
    expected_b1 = []
    
    for s_name, s_bins in sectors.items():
        if len(s_bins) < 1000: continue # Skip tiny fragment sectors
        s_total = len(s_bins)
        s_b1 = s_bins.count(1)
        s_pct = (s_b1 / s_total) * 100
        
        observed_b1.append(s_b1)
        expected_b1.append(s_total * global_b1_pct)
        
        print(f" Sector {s_name:<8} | Pop: {s_total:<9,} | Bin 1 Peak: {s_pct:.2f}%")

    # Chi-Square Test for Uniformity of the Peak
    chi2_stat, p_val = stats.chisquare(f_obs=observed_b1, f_exp=expected_b1)
    print(f"\n   📉 Chi-Square Statistic: {chi2_stat:.2f}")
    # A high p-value means the peak is beautifully uniform across sectors.
    print(f"   🧬 P-Value (Uniformity): {p_val:.4e}") 

    # ---------------------------------------------------------
    # TEST 2: THE PHYSICAL PERMUTATION NULL (THE TRUE NULL)
    # ---------------------------------------------------------
    print("\n" + "="*65)
    print("🛡️ EMPIRICAL TEST 2: THE PHYSICAL PERMUTATION NULL")
    print("Shuffling Magnitudes against Velocities 100 times.")
    print("This destroys the physical pairing but preserves empirical distributions.")
    print("="*65)

    null_b1_counts = []
    
    # 100 Iteration Monte Carlo of the Physics
    for i in range(100):
        # Shuffle magnitudes
        shuffled_m = np.copy(actual_m)
        np.random.shuffle(shuffled_m)
        
        # Vectorized recalculation for speed
        lum_array = 10**((25 - shuffled_m) / 2.5)
        scalar_array = ((actual_v**4) / lum_array) / ANCHOR
        
        # Filter valid scalars
        valid_mask = scalar_array > 0
        valid_scalars = scalar_array[valid_mask]
        
        phi_array = np.log(valid_scalars) % L
        bin_array = (phi_array / L * 10).astype(int)
        
        null_b1_counts.append(np.sum(bin_array == 1))

    mean_null_b1 = np.mean(null_b1_counts)
    std_null_b1 = np.std(null_b1_counts)
    
    mean_null_pct = (mean_null_b1 / total_records) * 100
    actual_b1_pct_display = (global_b1_count / total_records) * 100
    
    sigma = (global_b1_count - mean_null_b1) / std_null_b1 if std_null_b1 > 0 else 0

    print(f"📊 Actual Bin 1 Peak:        {actual_b1_pct_display:.2f}% ({global_b1_count:,} galaxies)")
    print(f"🎲 Physical Null Mean Peak:  {mean_null_pct:.2f}% ({int(mean_null_b1):,} galaxies)")
    print(f"📉 Null Standard Dev (σ):    {std_null_b1:,.2f} galaxies")
    print(f"🔥 TRUE STATISTICAL POWER:   {sigma:.2f} Sigma")
    
    print("\n📝 PHOENIX REPORT v2:")
    if sigma > 5.0:
        print("   The signal survives the True Physical Null. The 16/pi lock")
        print("   is strictly dependent on the actual pairing of a galaxy's mass")
        print("   and light. It is a genuine physical phenomenon.")
    else:
        print("   The peak vanished into the background distribution limits.")
        print("   The framework is rejected.")

if __name__ == "__main__":
    run_phoenix_v2()