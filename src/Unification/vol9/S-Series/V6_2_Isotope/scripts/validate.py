# vol6/S-Series/V6_2_Isotope/scripts/validate.py
import json
from pathlib import Path

PROMOTED_LAKE = Path("../lake/v6_2_isotopes_promoted.jsonl")

def validate():
    print("===============================================================")
    print(" 🛡️ MONDY'S VALIDATION: V6_2 (Isotopic Phase Lock)")
    print("===============================================================")
    
    print(f"{'Atmosphere'.ljust(20)} | {'Status'.ljust(15)} | {'KLC Resonance'}")
    print("-" * 55)
    
    with open(PROMOTED_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            klc = data["klc_resonance"]
            print(f"{data['name'].ljust(20)} | {data['status'].ljust(15)} | {klc:.5f}")
            
    print("-" * 55)
    print("[*] Goal: Identify the 'Phase Dislocation' of Mars.")

if __name__ == "__main__":
    validate()