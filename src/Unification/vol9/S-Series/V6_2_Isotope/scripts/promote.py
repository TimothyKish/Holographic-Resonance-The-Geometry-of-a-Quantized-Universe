# vol6/S-Series/V6_2_Isotope/scripts/promote.py
import json
import math
import os
from pathlib import Path

RAW_LAKE = Path("../lake/v6_2_isotopes_raw.jsonl")
PROMOTED_LAKE = Path("../lake/v6_2_isotopes_promoted.jsonl")

# THE UNIFIED LATTICE CONSTANT
LATTICE_CONSTANT = 16.0 / math.pi
V6_ANCHOR = 6.6069e10 

def promote():
    print("===============================================================")
    print(" 🧪 PROMOTING V6_2: THE ISOTOPIC ANAGRAM (The Brake Test)")
    print("===============================================================")
    
    if not RAW_LAKE.exists(): return
    
    records = []
    with open(RAW_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            
            # KINETIC ISOTOPE PROXY:
            # The Argon ratio represents the "stiffness" of the atmospheric shell.
            # We scale this to see where the planet sits on the Lattice wave.
            val = (data["ar_40_36"] * 1e8) / V6_ANCHOR
                
            log_val = abs(math.log(val))
            residue = log_val % LATTICE_CONSTANT
            klc = math.cos(residue * (2 * math.pi / LATTICE_CONSTANT))
            
            data["klc_resonance"] = klc
            records.append(data)
            
    os.makedirs(PROMOTED_LAKE.parent, exist_ok=True)
    with open(PROMOTED_LAKE, 'w', encoding='utf-8') as f:
        for rec in records: f.write(json.dumps(rec) + "\n")
    print(f"[+] V6_2 Promotion complete. Atmospheric Phase mapped.")

if __name__ == "__main__":
    promote()