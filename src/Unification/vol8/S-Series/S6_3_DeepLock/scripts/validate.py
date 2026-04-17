# vol5/S-Series/S6_3_DeepLock/scripts/validate.py
import json
from pathlib import Path

SCALARIZE_LAKE = Path("../lake/s6_3_scalarized.jsonl")

def validate():
    print("===============================================================")
    print(" 🛡️ MONDY'S VALIDATION: S6_3 (The Galactic Unification)")
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
    
    # SUCCESS THRESHOLD: 
    # Moving from -0.49 to > 0.50 is a 1.0 Phase Shift.
    if average_klc > 0.80:
        print("\n[+] MONDY APPROVES: THE DEEPLOCK IS SEALED.")
        print("    Finding: The Galactic Scale is now in 1:1 phase with the Solar Scale.")
    elif average_klc > 0.0:
        print("\n[+] MONDY: Polarity flip successful. Nearing the pocket center.")
    else:
        print("\n[!] MONDY WARNING: Sub-zero resonance. Anchor is still off-center.")

if __name__ == "__main__":
    validate()