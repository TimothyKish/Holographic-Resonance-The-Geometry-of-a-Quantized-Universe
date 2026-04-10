import pandas as pd
import numpy as np
import os

def stitch_and_scalarize():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    lake_dir = os.path.join(project_root, 'lake')
    
    sectors = ['NW', 'NE', 'SW', 'SE']
    all_dfs = []

    print("🧵 STITCHING CARDINAL SECTORS...")
    for s in sectors:
        path = os.path.join(lake_dir, f'Sector_{s}_Vol6.csv')
        if os.path.exists(path):
            df = pd.read_csv(path)
            df['sector'] = s
            all_dfs.append(df)
            print(f"   ✅ Added {s}: {len(df):,} galaxies.")

    master_df = pd.concat(all_dfs)
    
    # 🧬 Scalarize: Apply the 16/pi Phase Metric
    print("🛰️  APPLYING GLOBAL PHASE SCALARIZATION (16/π)...")
    master_df['kish_bin'] = ((master_df['zsp'] * 16 / np.pi) % 1.0 * 10).astype(int)

    output_path = os.path.join(lake_dir, 'Master_Galaxy_Vol6_2.csv')
    master_df.to_csv(output_path, index=False)
    
    print(f"\n🏆 MASTER VOL 6.2 READY: {len(master_df):,} total galaxies.")
    print(f"📂 Location: {output_path}")

if __name__ == "__main__":
    stitch_and_scalarize()