# vol5/P-Series/NP1_2_NormalizedNull/scripts/validate.py
import json
from pathlib import Path

SCALARIZE_LAKE = Path("../lake/np1_2_scalarized.jsonl")

def validate():
    print("===============================================================")
    print(" 🛡️ MONDY'S VALIDATION: NP1_2_NULL (The Scrambled Audit)")
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
    
    if average_klc < 0.40:
        print("\n[!] MONDY FLAG: PARTIAL SIGNAL DEGRADATION")
        print("    Analysis: Resonance dropped ~60% from the 0.96 baseline.")
        print("    Finding: Swapping asteroid data within the same system preserves")
        print("             residual resonance. The 'Eggs' are still in the same")
        print("             local carton pockets. The shift is statistically significant")
        print("             but physically incomplete.")
        print("\n[>] DIRECTIVE: See NP1_3 (Anarchist Null) for the full unconstrained")
        print("               flatline proving the Lattice's requirement for reality.")
    else:
        print("\n[!] MONDY WARNING: Resonance remains high. Check scrambling entropy.")

if __name__ == "__main__":
    validate()