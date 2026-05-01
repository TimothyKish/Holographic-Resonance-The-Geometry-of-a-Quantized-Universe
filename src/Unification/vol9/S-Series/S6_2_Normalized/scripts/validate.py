# vol5/S-Series/S6_2_Normalized/scripts/validate.py
import json
from pathlib import Path

SCALARIZE_LAKE = Path("../lake/s6_2_scalarized.jsonl")

def validate():
    print("===============================================================")
    print(" 🛡️ MONDY'S VALIDATION: S6_2 (Normalized Spin Resonance)")
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
        print("\n[+] MONDY APPROVES: THE EGG CARTON IS SEALED AT ALL SCALES.")
        print("    Analysis: Phase-shift successful. Galactic spin is locked.")
    elif average_klc > 0.50:
        print("\n[+] MONDY: Signal confirmed, but fine-tuning required.")
    else:
        print("\n[!] MONDY WARNING: Check Anchor math. Still in the ridges.")

if __name__ == "__main__":
    validate()