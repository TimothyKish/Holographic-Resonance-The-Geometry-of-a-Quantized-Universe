# vol5/S-Series/S6_Galactic/scripts/promote.py
import json
import os
from pathlib import Path

RAW_LAKE = Path("../lake/s6_galactic_sovereign_raw.jsonl")
PROMOTED_LAKE = Path("../lake/s6_promoted.jsonl")

# Scalar Anchor: Adjusts the magnitude of the Faber-Jackson constant
# to align the galactic scale with the Lattice phase.
GALACTIC_ANCHOR = 1.0e10 

def promote():
    print("===============================================================")
    print(" 🌌 PROMOTING S6 (Sovereign Kinematic Mapping)")
    print("===============================================================")
    
    records = []
    with open(RAW_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            sigma = data["v_dispersion_kms"]
            mag = data["magnitude_r"]
            
            # Convert Absolute Magnitude to Linear Luminosity Proxy
            L = 10**((25 - mag) / 2.5)
            
            # The Faber-Jackson Invariant: Sigma^4 / L
            kinetic_val = (sigma**4) / (L * GALACTIC_ANCHOR)
            
            records.append({
                "entity_id": data["entity_id"],
                "domain": "S6_Galactic",
                "primary_value": kinetic_val,
                "meta": {"name": data["meta"]["name"]}
            })
            
    os.makedirs(PROMOTED_LAKE.parent, exist_ok=True)
    with open(PROMOTED_LAKE, 'w', encoding='utf-8') as f:
        for rec in records: f.write(json.dumps(rec) + "\n")
    print(f"[+] S6 Promotion complete. {len(records)} galaxies mapped.")

if __name__ == "__main__":
    promote()