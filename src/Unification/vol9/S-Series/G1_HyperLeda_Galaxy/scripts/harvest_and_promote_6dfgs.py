import pandas as pd
import numpy as np
import json
import os
import requests

def harvest_and_promote_unbreakable():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    lake_dir = os.path.join(project_root, 'lake')
    if not os.path.exists(lake_dir): os.makedirs(lake_dir)
    
    raw_path = os.path.join(lake_dir, '6dfgs_raw.csv')
    output_path = os.path.join(lake_dir, '6dFGS_PHYSICAL.jsonl')

    print("🛰️  404 DETECTED. INITIATING FORCED CSV STREAM (BANKER'S BYPASS)...")
    
    # -source=J/MNRAS/427/245 hits the master catalog, bypassing broken table aliases.
    # -out.form=csv forces pure CSV output, dropping all broken XML schemas.
    url = "https://vizier.cds.unistra.fr/viz-bin/asu-txt?-source=J/MNRAS/427/245&-out.form=csv&-out=6dFGS,s,Kmag&-out.max=15000"

    try:
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        
        # VizieR still injects '#' comments and empty lines. We strip them out.
        lines = r.text.splitlines()
        clean_lines = []
        for line in lines:
            if line.startswith('#'): continue
            if line.strip() == '': continue
            clean_lines.append(line)
            
        if len(clean_lines) < 2:
            print("❌ ERROR: Stream returned empty data.")
            return
            
        # Save the raw artifact to the lake so Phoenix can audit it
        with open(raw_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(clean_lines))
        print(f"✅ RAW CSV ARTIFACT SECURED: {raw_path}")
        
        # Load into Pandas. (engine='python' handles inconsistent separators if VizieR glitches)
        df = pd.read_csv(raw_path, sep=';|,', engine='python', on_bad_lines='skip')
        
        # If row 0 contains text like '[mag]' or '---', drop it (VizieR units row)
        if df.iloc[0].astype(str).str.contains('[a-zA-Z-]', regex=True).any():
            df = df.iloc[1:].reset_index(drop=True)
            
        print(f"📊 DATA LOADED: {len(df)} Southern Sky galaxies.")
        
    except Exception as e:
        print(f"❌ STREAM FAILED: {e}")
        return

    # Find the physics columns dynamically to prevent key errors
    col_sig = next((c for c in df.columns if 's' in c.lower() or 'sig' in c.lower() or 'disp' in c.lower()), None)
    col_mag = next((c for c in df.columns if 'k' in c.lower() or 'mag' in c.lower()), None)

    if not col_sig or not col_mag:
        print(f"❌ ERROR: Missing Physics Columns. Found: {list(df.columns)}")
        return

    # Clean strings to numeric, drop NaNs
    df[col_sig] = pd.to_numeric(df[col_sig], errors='coerce')
    df[col_mag] = pd.to_numeric(df[col_mag], errors='coerce')
    df = df.dropna(subset=[col_sig, col_mag]).copy()

    # THE SOVEREIGN CONSTANTS
    L = 16.0 / np.pi
    ANCHOR = 6.6069e10

    print(f"🧬 PROMOTING TO KISH SPACE...")
    
    total_promoted = 0
    with open(output_path, 'w') as f:
        for _, row in df.iterrows():
            try:
                l_sigma = float(row[col_sig])
                mag = float(row[col_mag])
                
                # 's' in Magoulas 2012 is log10(sigma)
                vdisp = 10 ** l_sigma
                lum = 10**((25 - mag) / 2.5)
                val = ((vdisp**4) / lum) / ANCHOR
                
                if val <= 0 or np.isnan(val) or np.isinf(val): 
                    continue
                
                phi = np.log(val) % L
                kish_bin = int((phi / L) * 10)
                
                record = {
                    "id": str(row.iloc[0]),
                    "kish_bin": min(max(kish_bin, 0), 9),
                    "scalar": val
                }
                f.write(json.dumps(record) + '\n')
                total_promoted += 1
            except Exception:
                continue

    print(f"✅ SUCCESS: {total_promoted:,} Southern Sky galaxies promoted.")
    print("🎯 NEXT STEP: Run 'audit_6dfgs.py' to check the Phase Shift.")

if __name__ == "__main__":
    harvest_and_promote_unbreakable()