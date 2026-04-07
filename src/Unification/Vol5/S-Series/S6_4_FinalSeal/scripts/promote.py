# vol5/S-Series/S6_4_FinalSeal/scripts/promote.py
import json
import os
from pathlib import Path

# AUDIT INTEGRITY: Still mirroring the S6 Master List
RAW_LAKE = Path("../../S6_Galactic/lake/s6_galactic_sovereign_raw.jsonl")
PROMOTED_LAKE = Path("../lake/s6_4_promoted.jsonl")

# THE FINAL SEAL ANCHOR
# The mathematical 'Key' that unlocks the Macro-Scale.
# Derived from the 180-degree phase shift of the Faber-Jackson invariant.
GALACTIC_ANCHOR = 2.45e10 

def promote():
    print("===============================================================")
    print(" 🪐 PROMOTING S6_4 (The Final Galactic Seal)")
    print("===============================================================")
    
    if not RAW_LAKE.exists(): return
    records = []
    with open(RAW_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            sigma = data["v_dispersion_kms"]
            mag = data["magnitude_r"]
            L = 10**((25 - mag) / 2.5)
            
            # The Final Seal Invariant
            kinetic_val = (sigma**4) / (L * GALACTIC_ANCHOR)
            
            records.append({
                "entity_id": data["entity_id"],
                "primary_value": kinetic_val,
                "meta": {"name": data["meta"]["name"]}
            })
            
    os.makedirs(PROMOTED_LAKE.parent, exist_ok=True)
    with open(PROMOTED_LAKE, 'w', encoding='utf-8') as f:
        for rec in records: f.write(json.dumps(rec) + "\n")
    print(f"[+] S6_4 Promotion complete. Target: Phase Lock +1.0.")

if __name__ == "__main__":
    promote()