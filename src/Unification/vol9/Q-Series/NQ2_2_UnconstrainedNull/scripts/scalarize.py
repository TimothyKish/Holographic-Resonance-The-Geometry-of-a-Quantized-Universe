# vol5/Q-Series/NQ2_2_UnconstrainedNull/scripts/scalarize.py
import json
import math
from pathlib import Path

PROMOTED_LAKE = Path("../lake/nq2_2_unconstrained_promoted.jsonl")
SCALARIZE_LAKE = Path("../lake/nq2_2_unconstrained_scalarized.jsonl")
LATTICE_CONSTANT = 16.0 / math.pi

def scalarize():
    print("[*] Applying Lattice Modulus to Unconstrained NQ2_2 Data...")
    with open(PROMOTED_LAKE, 'r', encoding='utf-8') as f, open(SCALARIZE_LAKE, 'w', encoding='utf-8') as out:
        for line in f:
            data = json.loads(line)
            val = data["primary_value"]
            if val <= 0: continue
            
            log_val = abs(math.log(val))
            residue = log_val % LATTICE_CONSTANT
            klc = math.cos(residue * (2 * math.pi / LATTICE_CONSTANT))
            
            data["lattice_metrics"] = {"log_value": log_val, "residue": residue, "klc_resonance": klc}
            out.write(json.dumps(data) + "\n")
    print("[+] Scalarization complete. Infinite scalar noise mapped to the floor.")

if __name__ == "__main__":
    scalarize()