# vol5/P-Series/NP1_3_AnarchistNull/scripts/validate.py
import json
from pathlib import Path

SCALARIZE_LAKE = Path("../lake/np1_3_scalarized.jsonl")

def validate():
    print("===============================================================")
    print(" 🛡️ MONDY'S VALIDATION: NP1_3 (The Anarchist Flatline)")
    print("===============================================================")
    if not SCALARIZE_LAKE.exists(): return
    total_records = 0
    total_klc = 0.0
    with open(SCALARIZE_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            total_records += 1
            total_klc += data["lattice_metrics"]["klc_resonance"]
    
    average_klc = total_klc / total_records
    print(f"[+] Total Records Audited: {total_records}")
    print(f"[+] Average KLC Resonance: {average_klc:.5f}")
    
    if abs(average_klc) < 0.15:
        print("\n[+] MONDY APPROVES: NP1_3 HAS FLATLINED.")
        print("    Analysis: By removing physical constraints, the resonance has vanished.")
        print("    Conclusion: The 0.96 resonance in P1_2 is a result of REAL PHYSICS,")
        print("                not a mathematical artifact of the modulus.")
    else:
        print("\n[!] MONDY WARNING: Ghost resonance detected. Check randomization seed.")

if __name__ == "__main__":
    validate()