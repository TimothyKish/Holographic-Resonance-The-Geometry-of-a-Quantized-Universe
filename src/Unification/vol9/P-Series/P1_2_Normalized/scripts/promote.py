# vol5/P-Series/P1_2_Normalized/scripts/promote.py
import json
import os
from pathlib import Path

RAW_LAKE = Path("../lake/p1_2_normalized_raw.jsonl")
PROMOTED_LAKE = Path("../lake/p1_2_promoted.jsonl")
SOLAR_K = (365.25**2) / (1.0**3) 

def promote():
    print("===============================================================")
    print(" 🪐 PROMOTING P1_2 (The Egg Carton Alignment)")
    print("===============================================================")
    if not RAW_LAKE.exists(): return
    records = []
    with open(RAW_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                raw_k = (float(data["period_days"])**2) / (float(data["semi_major_au"])**3)
                normalized_val = raw_k / SOLAR_K
                promoted = {"entity_id": data["entity_id"], "domain": "P1_2_Normalized", "primary_value": normalized_val, "meta": {"name": data["name"], "raw_k": raw_k}}
                records.append(promoted)
            except: continue
    os.makedirs(PROMOTED_LAKE.parent, exist_ok=True)
    with open(PROMOTED_LAKE, 'w', encoding='utf-8') as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")
    print(f"[+] P1_2 Alignment complete. Orbits shifted to Solar Baseline.")

if __name__ == "__main__":
    promote()