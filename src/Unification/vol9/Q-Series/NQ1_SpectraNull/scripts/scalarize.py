# vol5/Q-Series/NQ1_SpectraNull/scripts/scalarize.py
import json
import math
from pathlib import Path

PROMOTED_LAKE = Path("../lake/nq1_spectra_promoted.jsonl")
SCALARIZE_LAKE = Path("../lake/nq1_spectra_scalarized.jsonl")
LATTICE_CONSTANT = 16.0 / math.pi

def scalarize():
    print("===============================================================")
    print(" 🪞 SCALARIZING NQ1_SPECTRA_NULL (Testing the Null Geometry)")
    print("===============================================================")
    
    if not PROMOTED_LAKE.exists():
        print(f"[-] ERROR: Promoted lake not found at {PROMOTED_LAKE}")
        return

    records_processed = 0
    with open(PROMOTED_LAKE, 'r', encoding='utf-8') as f, open(SCALARIZE_LAKE, 'w', encoding='utf-8') as out:
        for line in f:
            try:
                data = json.loads(line)
                
                # The Quantum Geometric Payload: Wavelength * Energy difference
                # (In a physical system, this yields hc, a constant. Here, it should yield noise)
                val = data["primary_value"] * data["secondary_value"]
                
                if val <= 0: 
                    continue
                    
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
            
    print(f"[+] Scalarization complete. {records_processed} null records mapped to the geometric floor.")

if __name__ == "__main__":
    scalarize()