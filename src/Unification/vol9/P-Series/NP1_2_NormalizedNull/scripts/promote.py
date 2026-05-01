# vol5/P-Series/NP1_2_NormalizedNull/scripts/promote.py
import json
import os
from pathlib import Path

RAW_LAKE = Path("../lake/np1_2_normalized_null_raw.jsonl")
PROMOTED_LAKE = Path("../lake/np1_2_promoted.jsonl")
SOLAR_K = (365.25**2) / (1.0**3) 

def promote():
    print("[*] Promoting Scrambled NP1_2 Null...")
    records = []
    with open(RAW_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            raw_k = (data["period_days"]**2) / (data["semi_major_au"]**3)
            normalized_val = raw_k / SOLAR_K
            records.append({"entity_id": data["entity_id"], "domain": "NP1_2_Null", "primary_value": normalized_val})
    
    os.makedirs(PROMOTED_LAKE.parent, exist_ok=True)
    with open(PROMOTED_LAKE, 'w', encoding='utf-8') as f:
        for rec in records: f.write(json.dumps(rec) + "\n")
    print(f"[+] Promotion complete.")

if __name__ == "__main__":
    promote()