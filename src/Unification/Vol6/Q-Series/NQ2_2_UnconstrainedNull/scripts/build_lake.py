# vol5/Q-Series/NQ2_2_UnconstrainedNull/scripts/build_lake.py
import json
import random
import os
import math
from pathlib import Path

REAL_Q2_LAKE = Path("../../Q2_Molecular/lake/q2_molecular_raw.jsonl") 
RAW_NULL_LAKE = Path("../lake/nq2_2_unconstrained_raw.jsonl")

def build_unconstrained_null():
    print("===============================================================")
    print(" 🌌 INITIALIZING NQ2_2 (Unconstrained Scalar Null)")
    print("===============================================================")
    
    if not REAL_Q2_LAKE.exists():
        print(f"[-] ERROR: Cannot find the authentic Q2 Lake at {REAL_Q2_LAKE}")
        return

    base_records = []
    with open(REAL_Q2_LAKE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
                base_records.append({
                    "molecule": entry["molecule"],
                    "formula": entry["formula"],
                    "measurement_type": entry["measurement_type"]
                })
            except Exception:
                continue
                
    print(f"[*] Extracted framework for {len(base_records)} geometric measurements.")
    print("[*] Generating unconstrained ghosts across the infinite scalar spectrum...")
    
    os.makedirs(RAW_NULL_LAKE.parent, exist_ok=True)
    
    with open(RAW_NULL_LAKE, "w", encoding="utf-8") as out_f:
        for i in range(len(base_records)):
            m_type = base_records[i]["measurement_type"]
            
            # BREAKING THE LAWS OF PHYSICS
            # Generate random numbers across multiple full cycles of the 16/pi lattice
            # This allows the values to fall heavily into the anti-resonant troughs
            unconstrained_value = math.exp(random.uniform(-10.0, 15.0))
                
            scrambled_entry = {
                "entity_id": f"NULL_UNCONSTRAINED_{base_records[i]['formula']}_{i:03d}",
                "domain": "nq2_2_unconstrained_null",
                "molecule": base_records[i]["molecule"],
                "measurement_type": m_type,
                "value_scrambled": unconstrained_value # The unconstrained payload
            }
            out_f.write(json.dumps(scrambled_entry) + "\n")
            
    print(f"[*] NQ2_2 Raw Lake built successfully. Physical boundaries obliterated.")

if __name__ == "__main__":
    build_unconstrained_null()