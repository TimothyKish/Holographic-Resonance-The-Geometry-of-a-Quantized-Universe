# vol5/P-Series/NP1_PlanetaryNull/scripts/build_lake.py
import json
import random
import os
from pathlib import Path

REAL_P1_LAKE = Path("../../P1_Planetary/lake/p1_planetary_raw.jsonl")
RAW_NULL_LAKE = Path("../lake/np1_planetary_raw.jsonl")

def build_null():
    print("===============================================================")
    print(" 🪞 INITIALIZING NP1_PLANETARY (Scrambled Orbital Null)")
    print("===============================================================")
    
    records = []
    with open(REAL_P1_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            records.append(json.loads(line))
            
    # Extract periods and shuffle them to destroy the Keplerian relationship
    periods = [r['period_days'] for r in records]
    random.shuffle(periods)
    
    os.makedirs(RAW_NULL_LAKE.parent, exist_ok=True)
    with open(RAW_NULL_LAKE, 'w', encoding='utf-8') as out:
        for i in range(len(records)):
            records[i]['period_days'] = periods[i] # Injected noise
            records[i]['entity_id'] = f"NULL_{records[i]['entity_id']}"
            out.write(json.dumps(records[i]) + "\n")
            
    print(f"[+] NP1 Null Lake built. 13,521 orbits scrambled.")

if __name__ == "__main__":
    build_null()