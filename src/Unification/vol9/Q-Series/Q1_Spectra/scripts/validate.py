# vol5/Q-Series/Q1_Spectra/scripts/validate.py
import json
from pathlib import Path

SCALARIZE_LAKE = Path("../lake/q1_spectra_scalarized.jsonl")

def validate():
    print("===============================================================")
    print(" 🛡️ MONDY'S VALIDATION: Q1_SPECTRA (Empirical Quantum Floor)")
    print("===============================================================")
    
    if not SCALARIZE_LAKE.exists():
        print(f"[-] ERROR: Scalarized lake not found at {SCALARIZE_LAKE}")
        return

    required_keys = ["entity_id", "domain", "primary_value", "secondary_value", "lattice_metrics"]
    metrics_keys = ["log_value", "residue", "klc_resonance"]
    
    total_records = 0
    total_klc = 0.0

    with open(SCALARIZE_LAKE, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                
                # Schema Check
                for key in required_keys:
                    if key not in data:
                        print(f"[-] Validation Failed at line {line_num}: Missing primary key '{key}'")
                        return
                        
                for key in metrics_keys:
                    if key not in data["lattice_metrics"]:
                        print(f"[-] Validation Failed at line {line_num}: Missing metric key '{key}'")
                        return
                
                total_records += 1
                total_klc += data["lattice_metrics"]["klc_resonance"]
                
            except json.JSONDecodeError:
                print(f"[-] Validation Failed at line {line_num}: Invalid JSON.")
                return

    if total_records == 0:
        print("[-] Validation Failed: Lake is empty.")
        return

    average_klc = total_klc / total_records
    
    print(f"[+] Schema Intact: All records conform to Vol5 Standard.")
    print(f"[+] Total Records Validated: {total_records}")
    print(f"[+] Average KLC Resonance: {average_klc:.5f}")
    
    # Mondy's specific check for Physical domains (Looking for Resonance)
    if average_klc > 0.50:
        print("\n[+] MONDY APPROVES: Q1_Spectra exhibits strong 16/pi geometric resonance. The Quantum Floor is locked.")
    else:
        print(f"\n[!] MONDY WARNING: Q1_Spectra resonance is lower than expected. Verify the physical extraction.")

if __name__ == "__main__":
    validate()