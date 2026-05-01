# vol5/S-Series/S1_Galactic/scripts/validate.py
import json
from pathlib import Path

SCALARIZE_LAKE = Path("../lake/s1_scalarized.jsonl")

def validate():
    print("===============================================================")
    print(" 🛡️ MONDY'S VALIDATION: S1_GALACTIC (Holographic Spin)")
    print("===============================================================")
    
    total_records = 0
    total_klc = 0.0
    with open(SCALARIZE_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            total_records += 1
            total_klc += data["lattice_metrics"]["klc_resonance"]
    
    average_klc = total_klc / total_records
    print(f"[+] Galaxies Validated: {total_records}")
    print(f"[+] Average KLC Resonance: {average_klc:.5f}")
    
    if average_klc > 0.40:
        print("\n[+] MONDY APPROVES: GALACTIC SPIN IS QUANTIZED.")
    else:
        print("\n[!] MONDY REJECTS: Phase-shift detected. Possible unit mismatch.")

if __name__ == "__main__":
    validate()