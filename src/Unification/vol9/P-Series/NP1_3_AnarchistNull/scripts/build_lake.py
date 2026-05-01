# vol5/P-Series/NP1_3_AnarchistNull/scripts/build_lake.py
import json
import random
import os
import math
from pathlib import Path

REAL_P1_2_LAKE = Path("../../P1_2_Normalized/lake/p1_2_normalized_raw.jsonl")
RAW_NULL_LAKE = Path("../lake/np1_3_anarchist_null_raw.jsonl")

def build_anarchist_null():
    print("===============================================================")
    print(" 🪞 INITIALIZING NP1_3 (The Anarchist Null)")
    print("===============================================================")
    if not REAL_P1_2_LAKE.exists(): return
    
    records_count = 13521
    
    os.makedirs(RAW_NULL_LAKE.parent, exist_ok=True)
    with open(RAW_NULL_LAKE, 'w', encoding='utf-8') as out:
        for i in range(records_count):
            # Generate unconstrained orbits (Sub-mercurial to Interstellar)
            # This forces the values to land in the 'ridges' between the carton pockets
            p_days = math.exp(random.uniform(0.1, 15.0))
            a_au = math.exp(random.uniform(-5.0, 8.0))
            
            entry = {
                "entity_id": f"GHOST_ORBIT_{i:05d}",
                "period_days": p_days,
                "semi_major_au": a_au
            }
            out.write(json.dumps(entry) + "\n")
    print(f"[+] NP1_3 Null Lake built. 13,521 chaotic ghosts generated.")

if __name__ == "__main__":
    build_anarchist_null()