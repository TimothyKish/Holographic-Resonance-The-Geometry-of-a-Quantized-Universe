import pandas as pd
import numpy as np
import json
import os
import math

def run_skyalign_scan():
    print("🛰️  INITIATING FRB SKYALIGN SCAN (JSON MULTI-LOADER)...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    lake_dir = os.path.join(project_root, 'lake')
    
    # Target the primary CHIME catalog
    input_path = os.path.join(lake_dir, 'chimefrbcat1.json')
    output_path = os.path.join(lake_dir, 'detected_nodes.jsonl')

    if not os.path.exists(input_path):
        print(f"❌ ERROR: {input_path} not found.")
        return

    # Load JSON (Handling list of dicts format)
    try:
        with open(input_path, 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        print(f"📊 DATA LOADED: {len(df)} FRBs found in Catalog 1.")
    except Exception as e:
        print(f"❌ JSON LOAD FAILED: {e}")
        return

    # CHIME Catalog 1 Keys: 'dm_fit_res' is the standard dispersion measure
    col_dm = 'dm_fit_res'
    col_name = 'tns_name'

    # The "Ideal" Theorems
    theorems = {
        "Pi (π)": 3.14159,
        "Golden Ratio (Φ)": 1.61803,
        "Euler's Number (e)": 2.71828,
        "Lattice Constant (16/π)": 5.09295,
        "Fine Structure (α^-1)": 137.036
    }

    # The "Phoenix Shift" (3.6% offset observed in galaxies)
    PHOENIX_SHIFT = 5.2764 / 5.0930 
    print(f"⚙️  Applying Phoenix Correction Factor: {PHOENIX_SHIFT:.4f}")

    nodes = []
    
    for _, row in df.iterrows():
        try:
            dm = float(row[col_dm])
            name = str(row[col_name])
            
            for t_name, t_val in theorems.items():
                # Test 1: Pure Match
                scale = 10**np.floor(np.log10(dm) - np.log10(t_val))
                target_pure = t_val * scale
                
                # Test 2: Shifted Match (The Calibration Hypothesis)
                target_shifted = (t_val * PHOENIX_SHIFT) * scale
                
                err_pure = abs(dm - target_pure) / target_pure
                err_shifted = abs(dm - target_shifted) / target_shifted
                
                # If it hits within 0.5% tolerance
                if err_pure < 0.005 or err_shifted < 0.005:
                    nodes.append({
                        "name": name,
                        "theorem": t_name,
                        "mode": "Pure" if err_pure < err_shifted else "Shifted",
                        "raw_dm": round(dm, 2),
                        "expected_dm": round(target_pure if err_pure < err_shifted else target_shifted, 2),
                        "error_pct": round(min(err_pure, err_shifted) * 100, 4)
                    })
                    break
        except:
            continue

    with open(output_path, 'w') as f:
        for n in nodes:
            f.write(json.dumps(n) + '\n')

    pure_count = len([n for n in nodes if n['mode'] == 'Pure'])
    shifted_count = len([n for n in nodes if n['mode'] == 'Shifted'])

    print(f"\n✅ SCAN COMPLETE: {len(nodes)} Calibration Nodes identified.")
    print(f"   💎 Pure Theorem Nodes:    {pure_count}")
    print(f"   📡 Shifted (Phoenix) Nodes: {shifted_count}")
    print(f"📂 Results saved to {output_path}")

if __name__ == "__main__":
    run_skyalign_scan()