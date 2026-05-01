# vol6/S-Series/V6_3_Pinch/scripts/promote.py
import json
import math
import os
from pathlib import Path

RAW_LAKE = Path("../lake/v6_3_pinch_raw.jsonl")
PROMOTED_LAKE = Path("../lake/v6_3_pinch_promoted.jsonl")

LATTICE_CONSTANT = 16.0 / math.pi
V6_ANCHOR = 6.6069e10 

def promote():
    print("===============================================================")
    print(" 🧪 PROMOTING V6_3: THE CUMULATIVE PINCH (The Snap-Shut Test)")
    print("===============================================================")
    
    if not RAW_LAKE.exists(): return
    
    records = []
    with open(RAW_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            
            # CUMULATIVE STIFFNESS LOGIC:
            # 1. Base Argon Shift (The Planet's rotational 'Age')
            base_val = data["ar_ratio"] * 1e7
            # 2. Chemical Stiffness (Salinity/Perchlorates)
            chem_factor = (data.get("salinity_gl", 0) + data.get("perchlorate_gl", 0)) * 1e8
            # 3. Radiation Jitter (UV/Cosmic)
            rad_factor = data.get("uv_stiffness", 0) * 1e9
            
            total_kinetic_val = (base_val + chem_factor + rad_factor) / V6_ANCHOR
                
            log_val = abs(math.log(total_kinetic_val))
            residue = log_val % LATTICE_CONSTANT
            klc = math.cos(residue * (2 * math.pi / LATTICE_CONSTANT))
            
            data["klc_resonance"] = klc
            records.append(data)
            
    os.makedirs(PROMOTED_LAKE.parent, exist_ok=True)
    with open(PROMOTED_LAKE, 'w', encoding='utf-8') as f:
        for rec in records: f.write(json.dumps(rec) + "\n")
    print(f"[+] V6_3 Cumulative Promotion complete.")

if __name__ == "__main__":
    promote()