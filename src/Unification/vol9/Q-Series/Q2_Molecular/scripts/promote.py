# vol5/Q-Series/Q2_Molecular/scripts/promote.py
import json
import os
from pathlib import Path

RAW_LAKE = Path("../lake/q2_molecular_raw.jsonl")
PROMOTED_LAKE = Path("../lake/q2_molecular_promoted.jsonl")

def promote():
    print("===============================================================")
    print(" 🔬 PROMOTING Q2_MOLECULAR (Empirical Atomic Geometry)")
    print("===============================================================")
    
    if not RAW_LAKE.exists():
        print(f"[-] ERROR: Raw lake not found at {RAW_LAKE}")
        return

    records = []
    with open(RAW_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                
                promoted = {
                    "entity_id": data["entity_id"],
                    "domain": "Q2_Molecular",
                    "primary_value": data["value"],  # The actual angle or length
                    "secondary_value": 1.0,          # Unit multiplier
                    "meta": {
                        "molecule": data["molecule"],
                        "measurement_type": data["measurement_type"],
                        "source": "NIST CCCBDB (Experimental)"
                    }
                }
                records.append(promoted)
            except Exception as e:
                continue

    os.makedirs(PROMOTED_LAKE.parent, exist_ok=True)
    with open(PROMOTED_LAKE, 'w', encoding='utf-8') as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")
            
    print(f"[+] Promotion complete. {len(records)} molecular geometries wrapped in Vol5 Schema.")

if __name__ == "__main__":
    promote()