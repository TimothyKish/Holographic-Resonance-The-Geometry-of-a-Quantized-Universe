# vol6/S-Series/V6_AntiLife/scripts/validate.py
import json
from pathlib import Path

PROMOTED_LAKE = Path("../lake/v6_lethal_promoted.jsonl")

def validate():
    print("===============================================================")
    print(" 🛡️ MONDY'S VALIDATION: V6 (The Geometric Pinch)")
    print("===============================================================")
    
    total_klc = 0.0
    count = 0
    
    print(f"{'Environment'.ljust(20)} | {'Status'.ljust(15)} | {'KLC Resonance'}")
    print("-" * 55)
    
    with open(PROMOTED_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            klc = data["klc_resonance"]
            print(f"{data['name'].ljust(20)} | {data['status'].ljust(15)} | {klc:.5f}")
            
            total_klc += klc
            count += 1
            
    avg_klc = total_klc / count
    print("-" * 55)
    print(f"[+] Average Lethal Resonance: {avg_klc:.5f}")
    
    if avg_klc < -0.50:
        print("\n[+] VERDICT: THE POCKET IS SEALED.")
        print("    Analysis: Sterile environments occupy the Lattice Ridges.")
    elif avg_klc > 0.50:
        print("\n[!] VERDICT: POCKET OPEN.")
        print("    Analysis: Complexity should be possible. Check for 'Hidden Life'.")
    else:
        print("\n[*] VERDICT: THE NEUTRAL SLOPE.")
        print("    Analysis: Environment is in transition (Extremophile zone).")

if __name__ == "__main__":
    validate()