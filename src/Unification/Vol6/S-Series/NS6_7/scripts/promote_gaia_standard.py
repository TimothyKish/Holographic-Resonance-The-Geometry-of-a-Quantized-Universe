import pandas as pd
import numpy as np
import json
import os

def promote_gaia_to_vol5():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    lake_dir = os.path.join(project_root, 'lake')
    
    # THE METRIC CONSTANT (The 16/pi Lattice)
    L = 16.0 / np.pi 
    
    sectors = ['NW', 'NE', 'SW', 'SE']
    output_path = os.path.join(lake_dir, 'Master_Stellar_Gaia_Standard.jsonl')

    print("🧬 STITCHING & PROMOTING GAIA QUADRANTS...")
    
    total_count = 0
    with open(output_path, 'w') as f_out:
        for s in sectors:
            path = os.path.join(lake_dir, f'Gaia_Sector_{s}.csv')
            if not os.path.exists(path):
                print(f"⚠️  Missing {s}")
                continue
            
            print(f"   Processing {s}...")
            df = pd.read_csv(path)
            
            # Filter for high-precision parallax
            # Distance (parsecs) = 1000 / parallax (mas)
            df = df[df['parallax'] > 0]
            
            for _, row in df.iterrows():
                try:
                    parallax = float(row['parallax'])
                    dist_pc = 1000.0 / parallax
                    
                    # Convert local distance to metric phase
                    # Since stars are z ≈ 0, this reveals the local anchor point
                    phi = np.log(dist_pc) % L
                    kish_bin = int((phi / L) * 10)
                    
                    record = {
                        "source_id": str(row['source_id']),
                        "ra": float(row['ra']),
                        "dec": float(row['dec']),
                        "dist_pc": dist_pc,
                        "sector": s,
                        "kish_bin": min(max(kish_bin, 0), 9),
                        "standard": "S-Series_Gaia_Vol5"
                    }
                    f_out.write(json.dumps(record) + '\n')
                    total_count += 1
                except:
                    continue

    print(f"\n✅ STELLAR PROMOTION COMPLETE: {total_count:,} stars anchored.")
    print(f"📂 Master File: {output_path}")

if __name__ == "__main__":
    promote_gaia_to_vol5()