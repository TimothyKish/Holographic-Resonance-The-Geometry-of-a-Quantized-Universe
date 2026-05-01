# vol5/P-Series/NP1_2_NormalizedNull/scripts/build_lake.py
import json
import random
import os
from pathlib import Path

REAL_P1_2_LAKE = Path("../../P1_2_Normalized/lake/p1_2_normalized_raw.jsonl")
RAW_NULL_LAKE = Path("../lake/np1_2_normalized_null_raw.jsonl")

def build_null():
    print("===============================================================")
    print(" 🪞 INITIALIZING NP1_2 (Scrambled Normalized Null)")
    print("===============================================================")
    if not REAL_P1_2_LAKE.exists(): return
    
    records = []
    with open(REAL_P1_2_LAKE, 'r', encoding='utf-8') as f:
        for line in f: records.append(json.loads(line))
            
    # Scramble periods to destroy Kepler's Law
    periods = [r['period_days'] for r in records]
    random.shuffle(periods)
    
    os.makedirs(RAW_NULL_LAKE.parent, exist_ok=True)
    with open(RAW_NULL_LAKE, 'w', encoding='utf-8') as out:
        for i in range(len(records)):
            records[i]['period_days'] = periods[i] # Physics destroyed
            records[i]['entity_id'] = f"NULL_{records[i]['entity_id']}"
            out.write(json.dumps(records[i]) + "\n")
    print(f"[+] NP1_2 Null Lake built. 13,521 orbital relationships broken.")

if __name__ == "__main__":
    build_null()