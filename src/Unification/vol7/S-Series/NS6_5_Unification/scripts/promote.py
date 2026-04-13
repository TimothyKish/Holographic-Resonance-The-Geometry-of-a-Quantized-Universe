# vol5/S-Series/NS6_5_Unification/scripts/promote.py
import json
import os
from pathlib import Path

RAW_LAKE = Path("../lake/ns6_5_normalized_raw.jsonl")
PROMOTED_LAKE = Path("../lake/ns6_5_promoted.jsonl")

# THE GOLDEN ANCHOR: The verified galactic phase-lock constant
GALACTIC_ANCHOR = 6.6069e10 

def promote():
    print("===============================================================")
    print(" 🪐 PROMOTING NS6_5 (The Null-Phase Test)")
    print("===============================================================")
    
    if not RAW_LAKE.exists(): return
    records = []
    with open(RAW_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            sigma = data["v_dispersion_kms"]
            mag = data["magnitude_r"]
            L = 10**((25 - mag) / 2.5)
            
            # The Unified Invariant Transform
            kinetic_val = (sigma**4) / (L * GALACTIC_ANCHOR)
            
            records.append({
                "entity_id": data["entity_id"],
                "primary_value": kinetic_val
            })
            
    os.makedirs(PROMOTED_LAKE.parent, exist_ok=True)
    with open(PROMOTED_LAKE, 'w', encoding='utf-8') as f:
        for rec in records: f.write(json.dumps(rec) + "\n")
    print(f"[+] NS6_5 Promotion complete. Chaos processed through the Engine.")

if __name__ == "__main__":
    promote()