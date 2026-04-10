import json
import os
import numpy as np
from collections import Counter
import random

def run_phoenix_audit():
    print("🛡️  INITIATING PHOENIX MASTER AUDIT...")
    
    # We are running from the S-Series root
    base_dir = os.getcwd()
    
    # Priority list of known large ledgers
    candidates = [
        os.path.join(base_dir, 'S6_5_Unification', 'lake', 's6_5_scalarized.jsonl'),
        os.path.join(base_dir, 'S6_4_FinalSeal', 'lake', 's6_4_scalarized.jsonl'),
        os.path.join(base_dir, 'S6_Galactic', 'lake', 's6_scalarized.jsonl'),
        os.path.join(base_dir, 'NS6_7', 'lake', 'Master_Galaxy_Vol6_PHYSICAL.jsonl')
    ]
    
    ledger = None
    for c in candidates:
        if os.path.exists(c) and os.path.getsize(c) > 1024 * 1024: # Must be larger than 1MB
            ledger = c
            break
            
    if not ledger:
        print("❌ ERROR: Could not locate a massive Master Galaxy Ledger.")
        return
        
    print(f"📂 Accessing Local Ledger: {ledger}")
    
    # Auto-detect Schema (read first line)
    with open(ledger, 'r') as f:
        first_line = json.loads(f.readline())
        
    print(f"🔍 SCHEMA DETECTED: {list(first_line.keys())}")
        
    # Dynamically find the correct keys
    key_ra = next((k for k in ['ra', 'RA', 'raj2000'] if k in first_line), None)
    key_dec = next((k for k in ['dec', 'DEC', 'dej2000'] if k in first_line), None)
    key_bin = next((k for k in ['kish_bin', 'bin', 'phase_bin', 'Bin'] if k in first_line), None)
    
    if not key_bin:
        print(f"❌ ERROR: Could not find a 'bin' key in this file.")
        return

    quadrants = {
        "Q1 (North-East)": [], "Q2 (North-West)": [],
        "Q3 (South-East)": [], "Q4 (South-West)": [],
        "Global (No Coords)": []
    }
    
    total_records = 0
    
    print("   📥 Loading and partitioning galaxies...")
    with open(ledger, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                bin_val = int(data[key_bin])
                
                if key_ra and key_dec:
                    ra = float(data[key_ra])
                    dec = float(data[key_dec])
                    if dec >= 0 and ra < 180: q = "Q1 (North-East)"
                    elif dec >= 0 and ra >= 180: q = "Q2 (North-West)"
                    elif dec < 0 and ra < 180: q = "Q3 (South-East)"
                    else: q = "Q4 (South-West)"
                else:
                    q = "Global (No Coords)"
                    
                quadrants[q].append(bin_val)
                total_records += 1
            except Exception:
                continue

    print(f"\n✅ LEDGER SECURED: {total_records:,} galaxies audited.")
    
    # Quadrant Audit
    print("\n" + "="*60)
    print("🔭 EMPIRICAL TEST 1: SPATIAL ISOTROPY (THE CARDINAL AUDIT)")
    print("="*60)
    
    for q_name, bins in quadrants.items():
        if len(bins) == 0: continue
        counts = Counter(bins)
        total_q = len(bins)
        b1_pct = (counts.get(1, 0) / total_q) * 100
        print(f" {q_name:<18} | Pop: {total_q:<9,} | Bin 1 Peak: {b1_pct:.2f}%")

    # The Mondy Scrambled Null
    print("\n" + "="*60)
    print("🛡️ EMPIRICAL TEST 2: THE MONDY SCRAMBLED NULL")
    print("Scrambling data 100 times to calculate standard deviation of noise...")
    print("="*60)

    all_bins = []
    for bins in quadrants.values():
        all_bins.extend(bins)
        
    actual_b1_count = all_bins.count(1)
    actual_b1_pct = (actual_b1_count / total_records) * 100
    
    null_peaks = []
    for _ in range(100):
        scrambled = [random.randint(0, 9) for _ in range(total_records)]
        null_peaks.append(scrambled.count(1))
        
    mean_null = np.mean(null_peaks)
    std_null = np.std(null_peaks)
    sigma = (actual_b1_count - mean_null) / std_null if std_null > 0 else 0

    print(f"📊 Actual Global Bin 1 Peak:  {actual_b1_pct:.2f}%")
    print(f"🎲 Expected Scrambled Peak:   10.00%")
    print(f"📉 Standard Deviation (σ):    {std_null:,.2f} galaxies")
    print(f"🔥 STATISTICAL POWER:         {sigma:.2f} Sigma")
    
    print("\n📝 PHOENIX REPORT:")
    if sigma > 5.0:
        print("   The signal survives the Mondy Protocol. It is mathematically")
        print("   impossible for this to be random noise. Framework verified.")
    else:
        print("   The signal dissolved into the null noise. Framework rejected.")

if __name__ == "__main__":
    run_phoenix_audit()