# vol5/S-Series/NS6_5_Unification/scripts/build_lake.py
import json
import os
import random
from pathlib import Path

# Naming 1:1 Mirror
TARGET_LAKE = Path("../lake/ns6_5_normalized_raw.jsonl")

def build_lake():
    print("===============================================================")
    print(" 🎲 INITIALIZING NS6_5 (The Synthetic Chaos Mirror)")
    print("===============================================================")
    
    os.makedirs(TARGET_LAKE.parent, exist_ok=True)
    
    with open(TARGET_LAKE, 'w', encoding='utf-8') as f:
        for i in range(50):
            # Synthetic distribution mirroring real-world S6 Master bounds
            s = random.uniform(70.0, 400.0) 
            m = random.uniform(-23.5, -16.0)
            
            f.write(json.dumps({
                "entity_id": f"NS_SOV_{i:03d}",
                "v_dispersion_kms": s,
                "magnitude_r": m,
                "meta": {"name": f"Synthetic_Null_{i}"}
            }) + "\n")
            
    print(f"[+] NS6_5 Mirror Lake built. 50 random noise agents initialized.")

if __name__ == "__main__":
    build_lake()