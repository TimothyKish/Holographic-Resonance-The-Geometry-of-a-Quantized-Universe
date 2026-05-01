# vol5/Q-Series/NQ2_MolecularNull/scripts/build_lake.py
import json
import random
import os
from pathlib import Path

REAL_Q2_LAKE = Path("../../Q2_Molecular/lake/q2_molecular_raw.jsonl") 
RAW_NULL_LAKE = Path("../lake/nq2_molecular_raw.jsonl")

def build_synthetic_null():
    print("===============================================================")
    print(" 🪞 INITIALIZING NQ2_MOLECULAR (Synthetic Ghost Null)")
    print("===============================================================")
    
    if not REAL_Q2_LAKE.exists():
        print(f"[-] ERROR: Cannot find the authentic Q2 Lake at {REAL_Q2_LAKE}")
        return

    base_records = []
    
    # 1. Read the real lake to get the shape of the data
    with open(REAL_Q2_LAKE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
                base_records.append({
                    "molecule": entry["molecule"],
                    "formula": entry["formula"],
                    "cas_number": entry["cas_number"],
                    "measurement_type": entry["measurement_type"]
                })
            except Exception:
                continue
                
    print(f"[*] Extracted framework for {len(base_records)} geometric measurements.")
    print("[*] Generating synthetic physical ghosts within biological boundaries...")
    
    os.makedirs(RAW_NULL_LAKE.parent, exist_ok=True)
    
    # 2. Generate random floats that fall within plausible molecular ranges
    with open(RAW_NULL_LAKE, "w", encoding="utf-8") as out_f:
        for i in range(len(base_records)):
            m_type = base_records[i]["measurement_type"]
            
            if m_type == "bond_length_angstroms":
                # Typical bond lengths are 0.5 to 3.5 Angstroms
                synthetic_value = random.uniform(0.5, 3.5)
            else:
                # Typical bond angles are 50 to 180 degrees
                synthetic_value = random.uniform(50.0, 180.0)
                
            scrambled_entry = {
                "entity_id": f"NULL_CCCBDB_{base_records[i]['formula']}_{i:03d}",
                "domain": "null_molecular_geometry",
                "molecule": base_records[i]["molecule"],
                "measurement_type": m_type,
                "value_scrambled": synthetic_value # The synthetic payload
            }
            out_f.write(json.dumps(scrambled_entry) + "\n")
            
    print(f"[*] NQ2_Molecular Raw Lake built successfully. Real geometry replaced with random noise.")

if __name__ == "__main__":
    build_synthetic_null()