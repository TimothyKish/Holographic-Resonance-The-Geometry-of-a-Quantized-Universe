import json
import math
from pathlib import Path

PROMOTED_LAKE = Path("../lake/q1_spectra_promoted.jsonl")
SCALARIZE_LAKE = Path("../lake/q1_spectra_scalarized.jsonl")
LATTICE_CONSTANT = 16.0 / math.pi

def scalarize():
    print("[*] Applying 16/pi Lattice Scalarization to Q1_Spectra...")
    
    with open(PROMOTED_LAKE, 'r', encoding='utf-8') as f, open(SCALARIZE_LAKE, 'w', encoding='utf-8') as out:
        for line in f:
            data = json.loads(line)
            
            # The Quantum Geometric Payload
            val = data["primary_value"] * data["secondary_value"]
            
            # Modulus projection against the Lattice
            if val == 0: continue
            log_val = abs(math.log(val))
            residue = log_val % LATTICE_CONSTANT
            klc = math.cos(residue * (2 * math.pi / LATTICE_CONSTANT))
            
            data["lattice_metrics"] = {
                "log_value": log_val,
                "residue": residue,
                "klc_resonance": klc
            }
            out.write(json.dumps(data) + "\n")
            
    print("[+] Scalarization complete. Quantum states mapped to the geometric floor.")

if __name__ == "__main__":
    scalarize()