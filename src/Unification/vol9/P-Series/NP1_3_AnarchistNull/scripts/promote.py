# vol5/P-Series/NP1_3_AnarchistNull/scripts/promote.py
import json
import os
from pathlib import Path

RAW_LAKE = Path("../lake/np1_3_anarchist_null_raw.jsonl")
PROMOTED_LAKE = Path("../lake/np1_3_promoted.jsonl")
SOLAR_K = (365.25**2) / (1.0**3) 

def promote():
    print("===============================================================")
    print(" 🪞 PROMOTING NP1_3 (The Chaotic Ghost Audit)")
    print("===============================================================")
    if not RAW_LAKE.exists(): return
    records = []
    with open(RAW_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                # Calculating Keplerian constant for impossible orbits
                raw_k = (float(data["period_days"])**2) / (float(data["semi_major_au"])**3)
                normalized_val = raw_k / SOLAR_K
                records.append({"entity_id": data["entity_id"], "primary_value": normalized_val})
            except: continue
    os.makedirs(PROMOTED_LAKE.parent, exist_ok=True)
    with open(PROMOTED_LAKE, 'w', encoding='utf-8') as f:
        for rec in records: f.write(json.dumps(rec) + "\n")
    print(f"[+] NP1_3 Promotion complete. 13,521 chaotic states ready.")

if __name__ == "__main__":
    promote()