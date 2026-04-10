# vol5/Q-Series/Q2_Molecular/scripts/scalarize.py
import json
import math
from pathlib import Path

PROMOTED_LAKE = Path("../lake/q2_molecular_promoted.jsonl")
SCALARIZE_LAKE = Path("../lake/q2_molecular_scalarized.jsonl")
LATTICE_CONSTANT = 16.0 / math.pi

def scalarize():
    print("===============================================================")
    print(" 🔬 SCALARIZING Q2_MOLECULAR (Testing the Lattice)")
    print("===============================================================")
    
    if not PROMOTED_LAKE.exists():
        print(f"[-] ERROR: Promoted lake not found at {PROMOTED_LAKE}")
        return

    records_processed = 0
    with open(PROMOTED_LAKE, 'r', encoding='utf-8') as f, open(SCALARIZE_LAKE, 'w', encoding='utf-8') as out:
        for line in f:
            try:
                data = json.loads(line)
                
                # The Physical Geometric Payload
                val = data["primary_value"]
                if val <= 0: continue
                    
                # Modulus projection against the Lattice
                log_val = abs(math.log(val))
                residue = log_val % LATTICE_CONSTANT
                klc = math.cos(residue * (2 * math.pi / LATTICE_CONSTANT))
                
                data["lattice_metrics"] = {
                    "log_value": log_val,
                    "residue": residue,
                    "klc_resonance": klc
                }
                out.write(json.dumps(data) + "\n")
                records_processed += 1
            except Exception as e:
                continue
            
    print(f"[+] Scalarization complete. {records_processed} molecular geometries mapped to the 16/pi floor.")

if __name__ == "__main__":
    scalarize()