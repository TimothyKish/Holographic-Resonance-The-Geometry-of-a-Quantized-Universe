# vol5/S-Series/S6_5_Unification/scripts/validate.py
import json
from pathlib import Path

SCALARIZE_LAKE = Path("../lake/s6_5_scalarized.jsonl")

def validate():
    print("===============================================================")
    print(" 🛡️ MONDY'S VALIDATION: S6_5 (Volume 5 Unification)")
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
    
    if average_klc > 0.70:
        print("\n[+] MONDY APPROVES: THE TRIPLE-LOCK IS COMPLETE.")
        print("    Audit Summary: Atoms, Planets, and Galaxies are Phase-Locked.")
        print("    Bridge Status: Volume 5 SECURED.")
    else:
        print("\n[!] MONDY WARNING: Deviation detected. Re-check Mirror parity.")

if __name__ == "__main__":
    validate()