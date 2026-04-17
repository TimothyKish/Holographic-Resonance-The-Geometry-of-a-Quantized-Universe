import pandas as pd
import numpy as np
import json
import os

def promote_physical_standard():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    lake_dir = os.path.join(project_root, 'lake')
    
    # THE SACRED CONSTANTS (Mondy's Standard)
    L = 16.0 / np.pi      # 5.0929...
    ANCHOR = 6.6069e10    # Standard S-Series Anchor
    
    sectors = ['NW', 'NE', 'SW', 'SE']
    output_path = os.path.join(lake_dir, 'Master_Galaxy_Vol6_PHYSICAL.jsonl')

    print("🧬 PROMOTING TO PHYSICAL FABER-JACKSON STANDARD...")
    
    total_count = 0
    with open(output_path, 'w') as f_out:
        for s in sectors:
            path = os.path.join(lake_dir, f'Sector_{s}_Vol6.csv')
            if not os.path.exists(path): continue
            
            # Note: We need 'rPmag' for Luminosity. 
            # If your CSV has 'rpmag', use that.
            df = pd.read_csv(path)
            print(f"   Processing {s} ({len(df):,} galaxies)...")
            
            for _, row in df.iterrows():
                try:
                    vdisp = float(row['Vdisp'])
                    # Use rPmag if available, else fallback to any magnitude column
                    mag = float(row.get('rPmag', row.get('rpmag', 18.0)))
                    
                    # 1. Calculate Luminosity
                    lum = 10**((25 - mag) / 2.5)
                    
                    # 2. The Faber-Jackson Scalar (The "Pulse")
                    val = ((vdisp**4) / lum) / ANCHOR
                    if val <= 0: continue
                    
                    # 3. Log-Modulo Transformation
                    phi = np.log(val) % L
                    kish_bin = int((phi / L) * 10)
                    kish_bin = min(max(kish_bin, 0), 9) # Safety clamp
                    
                    record = {
                        "objID": str(row['objID']),
                        "sector": s,
                        "kish_bin": kish_bin,
                        "z": float(row['zsp']),
                        "v": vdisp,
                        "m": mag
                    }
                    f_out.write(json.dumps(record) + '\n')
                    total_count += 1
                except:
                    continue

    print(f"\n✅ PHYSICAL PROMOTION COMPLETE: {total_count:,} galaxies.")
    print(f"📂 Saved to: {output_path}")

if __name__ == "__main__":
    promote_physical_standard()