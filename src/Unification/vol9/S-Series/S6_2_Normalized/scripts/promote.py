# vol5/S-Series/S6_2_Normalized/scripts/promote.py
import json
import os
from pathlib import Path

# Pointing back to the Sovereign Lake we just built
RAW_LAKE = Path("../../S6_Galactic/lake/s6_galactic_sovereign_raw.jsonl")
PROMOTED_LAKE = Path("../lake/s6_2_promoted.jsonl")

# THE NORMALIZATION ANCHOR
# We adjust the anchor to account for the 'Ridge' shift.
# This aligns the Milky Way-scale kinematics with the Lattice Floor.
GALACTIC_ANCHOR = 1.35e10 

def promote():
    print("===============================================================")
    print(" 🌌 PROMOTING S6_2 (Normalized Galactic Alignment)")
    print("===============================================================")
    
    if not RAW_LAKE.exists():
        print(f"[-] Source Lake not found at {RAW_LAKE}")
        return

    records = []
    with open(RAW_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            sigma = data["v_dispersion_kms"]
            mag = data["magnitude_r"]
            
            # Linear Luminosity proxy
            L = 10**((25 - mag) / 2.5)
            
            # Normalized Faber-Jackson Invariant
            kinetic_val = (sigma**4) / (L * GALACTIC_ANCHOR)
            
            records.append({
                "entity_id": data["entity_id"],
                "primary_value": kinetic_val,
                "meta": {"name": data["meta"]["name"]}
            })
            
    os.makedirs(PROMOTED_LAKE.parent, exist_ok=True)
    with open(PROMOTED_LAKE, 'w', encoding='utf-8') as f:
        for rec in records: f.write(json.dumps(rec) + "\n")
    print(f"[+] S6_2 Normalization complete. 50 galaxies phase-shifted.")

if __name__ == "__main__":
    promote()