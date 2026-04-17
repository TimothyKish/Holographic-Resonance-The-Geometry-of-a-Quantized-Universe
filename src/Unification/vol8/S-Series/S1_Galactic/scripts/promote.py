# vol5/S-Series/S1_Galactic/scripts/promote.py
import json
import os
from pathlib import Path

RAW_LAKE = Path("../lake/s1_galactic_raw.jsonl")
PROMOTED_LAKE = Path("../lake/s1_promoted.jsonl")

def promote():
    print("===============================================================")
    print(" 🌌 PROMOTING S1 (Kinetic Luminosity Mapping)")
    print("===============================================================")
    
    records = []
    with open(RAW_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            # Faber-Jackson proxy: Sigma^4 / Luminosity
            # Note: Magnitude is logarithmic, so we convert it back to a linear flux proxy
            sigma = data["v_dispersion_kms"]
            mag = data["magnitude_r"]
            
            # Linear Luminosity proxy (Inverse log of magnitude)
            L = 10**((25 - mag) / 2.5) 
            
            # The Kinetic Ratio
            kinetic_val = (sigma**4) / L
            
            records.append({
                "entity_id": data["entity_id"],
                "domain": "S1_Galactic",
                "primary_value": kinetic_val,
                "meta": {"sigma": sigma, "mag": mag}
            })
            
    os.makedirs(PROMOTED_LAKE.parent, exist_ok=True)
    with open(PROMOTED_LAKE, 'w', encoding='utf-8') as f:
        for rec in records: f.write(json.dumps(rec) + "\n")
    print(f"[+] S1 Promotion complete. {len(records)} galaxies mapped.")

if __name__ == "__main__":
    promote()