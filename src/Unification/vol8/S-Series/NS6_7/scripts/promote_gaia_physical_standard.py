import pandas as pd
import numpy as np
import json
import os

def promote_gaia_physical():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    lake_dir = os.path.join(project_root, 'lake')
    
    L = 16.0 / np.pi 
    sectors = ['NW', 'NE', 'SW', 'SE']
    output_path = os.path.join(lake_dir, 'Master_Stellar_Gaia_PHYSICAL.jsonl')

    print("🧬 PROMOTING GAIA TO PHYSICAL STELLAR STANDARD...")
    
    total_count = 0
    with open(output_path, 'w') as f_out:
        for s in sectors:
            path = os.path.join(lake_dir, f'Gaia_Physical_{s}.csv')
            if not os.path.exists(path): continue
            
            print(f"   Refining Sector {s}...")
            df = pd.read_csv(path)
            
            # 1. Total Proper Motion mu = sqrt(pmra^2 + pmdec^2)
            mu = np.sqrt(df['pmra']**2 + df['pmdec']**2)
            # 2. Flux from G-mag
            flux = 10**((25 - df['phot_g_mean_mag']) / 2.5)
            
            # 3. Physical Transform (Anchor=1.0 for initial sweep)
            val = (mu**4 / flux)
            
            # Filter valid physics
            valid_mask = (val > 0)
            val = val[valid_mask]
            
            # Calculate bins for the 16/pi target
            phi = np.log(val) % L
            kish_bins = (phi / L * 10).astype(int)
            
            # Iterate and write JSONL
            for i, b in enumerate(kish_bins):
                record = {
                    "sector": s,
                    "kish_bin": int(np.clip(b, 0, 9)),
                    "val": float(val.iloc[i])
                }
                f_out.write(json.dumps(record) + '\n')
                total_count += 1

    print(f"\n✅ PHYSICAL PROMOTION COMPLETE: {total_count:,} stars.")
    print(f"📂 Master File: {output_path}")

if __name__ == "__main__":
    promote_gaia_physical()