# vol5/S-Series/S6_3_DeepLock/scripts/scalarize.py
import json
import math
import os
from pathlib import Path

# DATA INPUT: The phase-shifted galactic invariants
PROMOTED_LAKE = Path("../lake/s6_3_promoted.jsonl")
SCALARIZE_LAKE = Path("../lake/s6_3_scalarized.jsonl")

# THE UNIVERSAL MODULUS: Derived from Vacuum Energy Information Density
LATTICE_CONSTANT = 16.0 / math.pi

def scalarize():
    print("[*] Scalarizing S6_3 (Testing DeepLock Resonance)...")
    
    if not PROMOTED_LAKE.exists(): return
    os.makedirs(SCALARIZE_LAKE.parent, exist_ok=True)

    with open(PROMOTED_LAKE, 'r', encoding='utf-8') as f, open(SCALARIZE_LAKE, 'w', encoding='utf-8') as out:
        for line in f:
            data = json.loads(line)
            val = data["primary_value"]
            
            # THE TRANSFORMATION: 
            # 1. Log-scale to linearize the power-law (Faber-Jackson)
            # 2. Modulo by Lattice Constant to find position in the 'Egg Carton'
            # 3. Cosine transform to find resonance (-1 = Ridge, +1 = Pocket)
            log_val = abs(math.log(val))
            residue = log_val % LATTICE_CONSTANT
            klc = math.cos(residue * (2 * math.pi / LATTICE_CONSTANT))
            
            data["lattice_metrics"] = {"klc_resonance": klc}
            out.write(json.dumps(data) + "\n")
            
    print(f"[+] S6_3 Scalarization complete. Mapping mapped to {LATTICE_CONSTANT:.4f}")

if __name__ == "__main__":
    scalarize()