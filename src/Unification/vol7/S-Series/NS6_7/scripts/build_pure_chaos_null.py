import json
import random
import math
import os

# 🛡️ NS6_31: THE UNCONSTRAINED "PURE CHAOS" NULL
# -----------------------------------------------------------
def build_pure_chaos():
    L = 16.0 / math.pi
    ANCHOR = 6.6069e10
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    output_path = os.path.join(project_root, 'lake', 'Master_Galaxy_Pure_Chaos.jsonl')
    
    print("🎲 GENERATING PURE CHAOS NULL (Unconstrained)...")

    bins = {i: 0 for i in range(10)}
    total_n = 268000
    
    with open(output_path, 'w') as f_out:
        for _ in range(total_n):
            # NO BOUNDARIES: Pure mathematical noise
            # Velocity from 1 to 1000, Mag from 1 to 50, Z from 0 to 5
            v = random.uniform(1.0, 1000.0)
            m = random.uniform(1.0, 50.0)
            z = random.uniform(0.0, 5.0)
            
            lum = 10**((25 - m) / 2.5)
            ks = ((v**4) / lum) / ANCHOR
            phi = math.log(ks) % L
            bin_idx = min(int((phi / L) * 10), 9)
            
            bins[bin_idx] += 1
            f_out.write(json.dumps({"kish_bin": bin_idx, "status": "PURE_CHAOS"}) + '\n')

    # Quick Chi-Square Check
    expected = total_n / 10.0
    chi2 = sum([((bins[i] - expected)**2) / expected for i in range(10)])
    
    print(f"\n==================================================")
    print(f"📊 PURE CHAOS RESULTS (N = {total_n:,})")
    print(f"==================================================")
    print(f"Chi-Squared (X²) : {chi2:,.2f}")
    print(f"Expected (Flat)  : 9.0")
    print(f"==================================================")

if __name__ == "__main__":
    build_pure_chaos()
    input("\nPress ENTER to close...")