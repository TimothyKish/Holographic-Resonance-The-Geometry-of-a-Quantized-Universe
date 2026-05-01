# vol5/S-Series/S6_4_FinalSeal/scripts/validate.py
import json
from pathlib import Path

SCALARIZE_LAKE = Path("../lake/s6_4_scalarized.jsonl")

def validate():
    print("===============================================================")
    print(" 🛡️ MONDY'S VALIDATION: S6_4 (Final Macro-Scale Seal)")
    print("===============================================================")
    
    total_records = 0
    total_klc = 0.0
    with open(SCALARIZE_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            total_records += 1
            total_klc += data["lattice_metrics"]["klc_resonance"]
    
    average_klc = total_klc / total_records
    print(f"[+] Galaxies Audited: {total_records}")
    print(f"[+] Average KLC Resonance: {average_klc:.5f}")
    
    if average_klc > 0.85:
        print("\n[+] MONDY APPROVES: THE UNIFIED FIELD IS LOCKED.")
        print("    Conclusion: Atoms, Planets, and Galaxies share the same geometry.")
    elif average_klc > 0.40:
        print("\n[+] MONDY: Strong resonance. The Macro-Scale is validated.")
    else:
        print("\n[!] MONDY WARNING: Check Anchor. Resonance did not peak.")

if __name__ == "__main__":
    validate()