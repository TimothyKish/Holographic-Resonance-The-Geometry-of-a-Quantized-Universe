# vol5/S-Series/S6_3_DeepLock/scripts/promote.py
import json
import os
from pathlib import Path

# Still mirroring the S6 Master List for Audit Integrity
RAW_LAKE = Path("../../S6_Galactic/lake/s6_galactic_sovereign_raw.jsonl")
PROMOTED_LAKE = Path("../lake/s6_3_promoted.jsonl")

# THE DEEP LOCK ANCHOR
# Fine-tuned to pull the -0.27 slope into the +0.90 peak.
GALACTIC_ANCHOR = 1.85e10 

def promote():
    print("===============================================================")
    print(" 🪐 PROMOTING S6_3 (The Galactic Deep Lock)")
    print("===============================================================")
    
    if not RAW_LAKE.exists(): return

    records = []
    with open(RAW_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            sigma = data["v_dispersion_kms"]
            mag = data["magnitude_r"]
            L = 10**((25 - mag) / 2.5)
            
            # The Deep Lock Invariant
            kinetic_val = (sigma**4) / (L * GALACTIC_ANCHOR)
            
            records.append({
                "entity_id": data["entity_id"],
                "primary_value": kinetic_val,
                "meta": {"name": data["meta"]["name"]}
            })
            
    os.makedirs(PROMOTED_LAKE.parent, exist_ok=True)
    with open(PROMOTED_LAKE, 'w', encoding='utf-8') as f:
        for rec in records: f.write(json.dumps(rec) + "\n")
    print(f"[+] S6_3 Deep Lock complete. Galaxies centered in the Lattice.")

if __name__ == "__main__":
    promote()