import pandas as pd
import numpy as np
import json
import os

def promote_quantum():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(project_root, 'lake', 'nist_raw_v1.csv')
    output_path = os.path.join(project_root, 'lake', 'q1_spectra_promoted.jsonl')
    
    # Fundamental Anchor
    R_INF = 109737.31568 # cm^-1
    
    print("🧬 PROMOTING QUANTUM SPECTRA (Rydberg Standard)...")
    
    # Load raw manual punch data
    df = pd.read_csv(input_path)
    
    # Cleaning helper to handle NIST "=""Value""" format from manual CSV export
    def clean_val(x):
        if pd.isna(x): return None
        return str(x).replace('="', '').replace('"', '').strip()

    total_promoted = 0
    with open(output_path, 'w') as f:
        for _, row in df.iterrows():
            # Use Ritz if available, otherwise Observed
            ritz = clean_val(row.get('ritz_wl_air(nm)'))
            obs = clean_val(row.get('obs_wl_air(nm)'))
            
            wl_nm = ritz if ritz and ritz != "" else obs
            if not wl_nm or wl_nm == "": continue
            
            try:
                wl = float(wl_nm)
                # Convert nm (air) to wavenumber (cm^-1)
                # Simple conversion for bubble mode; vacuum correction pending for Vol 6
                wavenumber = 1e7 / wl 
                
                # Physical Invariant
                scalar = wavenumber / R_INF
                
                record = {
                    "element": clean_val(row['element']),
                    "scalar": scalar,
                    "wavenumber": wavenumber,
                    "type": "ATOMIC_TRANSITION"
                }
                f.write(json.dumps(record) + '\n')
                total_promoted += 1
            except:
                continue

    print(f"✅ PROMOTED {total_promoted} transitions to Kish space.")

if __name__ == "__main__":
    promote_quantum()