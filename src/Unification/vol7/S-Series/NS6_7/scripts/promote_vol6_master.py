import pandas as pd
import numpy as np
import json
import os

def promote_to_vol5_standard():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    lake_dir = os.path.join(project_root, 'lake')
    
    sectors = ['NW', 'NE', 'SW', 'SE']
    output_path = os.path.join(lake_dir, 'Master_Galaxy_Vol6_Standard.jsonl')

    print("🧬 PROMOTING SECTORS TO VOL 5 STANDARD...")
    
    with open(output_path, 'w') as f_out:
        total_count = 0
        for s in sectors:
            path = os.path.join(lake_dir, f'Sector_{s}_Vol6.csv')
            if not os.path.exists(path): continue
            
            print(f"   Processing {s}...")
            df = pd.read_csv(path)
            
            # Scalarization and Normalization Logic
            for _, row in df.iterrows():
                z = float(row['zsp'])
                if z <= 0: continue
                
                # 1. Physics Promotion (16/pi Metric)
                phase = (z * 16 / np.pi) % 1.0
                kish_bin = int(phase * 10)
                
                # 2. Normalization (Volume + Area Correction)
                # Correction = 1 / (z^2 * GeometricFactor)
                # This flattens the "Egg Carton" bias
                weight = 1.0 / (z**2)
                
                # Create Vol 5 Standard JSON Object
                record = {
                    "objID": str(row['objID']),
                    "ra": float(row['RA_ICRS']),
                    "dec": float(row['DE_ICRS']),
                    "z": z,
                    "vdisp": float(row['Vdisp']),
                    "sector": s,
                    "kish_bin": kish_bin,
                    "weight": weight,  # Crucial for the 13-sigma test
                    "standard": "S-Series_Vol5"
                }
                
                f_out.write(json.dumps(record) + '\n')
                total_count += 1

    print(f"\n✅ PROMOTION COMPLETE: {total_count:,} galaxies normalized.")
    print(f"📂 Master File: {output_path}")

if __name__ == "__main__":
    promote_to_vol5_standard()