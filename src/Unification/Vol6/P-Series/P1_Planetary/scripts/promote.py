# vol5/P-Series/P1_Planetary/scripts/promote.py
import json
import os
from pathlib import Path

RAW_LAKE = Path("../lake/p1_planetary_raw.jsonl")
PROMOTED_LAKE = Path("../lake/p1_planetary_promoted.jsonl")

def promote():
    print("===============================================================")
    print(" 🪐 PROMOTING P1_PLANETARY (Keplerian Orbital Mapping)")
    print("===============================================================")
    
    if not RAW_LAKE.exists():
        print(f"[-] ERROR: Raw lake not found.")
        return

    records = []
    with open(RAW_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                
                # Kepler's Harmonic Law: P^2 / a^3
                # For our Solar System (AU and Days), this is a specific constant (~133,000)
                # For Exoplanets, this varies by the Mass of the Host Star.
                p = data["period_days"]
                a = data["semi_major_au"]
                kepler_val = (p**2) / (a**3)
                
                promoted = {
                    "entity_id": data["entity_id"],
                    "domain": "P1_Planetary",
                    "primary_value": kepler_val,
                    "secondary_value": a, # We keep the distance as a secondary scalar
                    "meta": {
                        "name": data["name"],
                        "source": data["source"]
                    }
                }
                records.append(promoted)
            except Exception:
                continue

    os.makedirs(PROMOTED_LAKE.parent, exist_ok=True)
    with open(PROMOTED_LAKE, 'w', encoding='utf-8') as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")
            
    print(f"[+] Promotion complete. {len(records)} orbital systems ready for the Lattice.")

if __name__ == "__main__":
    promote()