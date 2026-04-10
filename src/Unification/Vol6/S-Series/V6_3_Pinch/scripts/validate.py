# vol6/S-Series/V6_3_Pinch/scripts/validate.py
import json
from pathlib import Path

PROMOTED_LAKE = Path("../lake/v6_3_pinch_promoted.jsonl")

def validate():
    print("===============================================================")
    print(" 🛡️ MONDY'S VALIDATION: V6_3 (The Geometric Hard-Stop)")
    print("===============================================================")
    
    print(f"{'Environment'.ljust(25)} | {'KLC Resonance'}")
    print("-" * 45)
    
    with open(PROMOTED_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            klc = data["klc_resonance"]
            print(f"{data['name'].ljust(25)} | {klc:.5f}")
            
    print("-" * 45)
    print("[*] Analysis: Does the combination of factors trigger the Ridge flip?")

if __name__ == "__main__":
    validate()