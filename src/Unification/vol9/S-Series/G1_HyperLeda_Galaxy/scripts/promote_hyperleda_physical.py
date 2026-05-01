import pandas as pd
import numpy as np
import json
import os

def promote_hyperleda_standard():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_path = os.path.join(project_root, 'lake', 'hyperleda_raw.csv')
    output_path = os.path.join(project_root, 'lake', 'HyperLeda_PHYSICAL.jsonl')

    L = 16.0 / np.pi
    ANCHOR = 6.6069e10

    print(f"🧬 PROMOTING: {input_path}")
    if not os.path.exists(input_path):
        print("❌ Error: File not found.")
        return

    df = pd.read_csv(input_path)
    
    # DEBUG: Print columns to solve the mapping issue
    print(f"🔍 CSV Columns detected: {list(df.columns)}")

    # Map columns dynamically based on common VizieR variants
    def find_col(possible_names):
        for name in possible_names:
            if name in df.columns: return name
        return None

    c_sigma = find_col(['l_vdisp', 'log_vdisp', '_log_vdisp'])
    c_mag = find_col(['BTmag', 'bt', 'BTC', '_BTmag'])
    c_ra = find_col(['_RAJ2000', 'RAJ2000', 'ra'])
    c_dec = find_col(['_DEJ2000', 'DEJ2000', 'dec'])
    c_id = find_col(['PGC', 'pgc', 'objname'])

    if not all([c_sigma, c_mag]):
        print(f"❌ CRITICAL ERROR: Could not find Sigma ({c_sigma}) or Mag ({c_mag}) columns.")
        return

    total_promoted = 0
    with open(output_path, 'w') as f:
        for _, row in df.iterrows():
            try:
                # VizieR usually provides log10(sigma)
                l_sigma = float(row[c_sigma])
                vdisp = 10**l_sigma
                mag = float(row[c_mag])
                
                # Faber-Jackson Invariant
                lum = 10**((25 - mag) / 2.5)
                val = ((vdisp**4) / lum) / ANCHOR
                
                if val <= 0 or np.isnan(val) or np.isinf(val): continue
                
                phi = np.log(val) % L
                kish_bin = int((phi / L) * 10)
                
                record = {
                    "pgc": str(row.get(c_id, 'Unknown')),
                    "ra": float(row.get(c_ra, 0)),
                    "dec": float(row.get(c_dec, 0)),
                    "kish_bin": min(max(kish_bin, 0), 9),
                    "scalar": val
                }
                f.write(json.dumps(record) + '\n')
                total_promoted += 1
            except:
                continue

    print(f"✅ SUCCESS: {total_promoted:,} HyperLeda galaxies promoted.")
    print(f"📂 Master File: {output_path}")

if __name__ == "__main__":
    promote_hyperleda_standard()