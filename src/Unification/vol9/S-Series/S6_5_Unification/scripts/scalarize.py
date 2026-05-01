# vol5/S-Series/S6_5_Unification/scripts/scalarize.py
import json
import math
import os
from pathlib import Path

# DATA INPUT: The Sweep-Verified promoted data (Anchor: 6.6069e10)
PROMOTED_LAKE = Path("../lake/s6_5_promoted.jsonl")
SCALARIZE_LAKE = Path("../lake/s6_5_scalarized.jsonl")

# THE UNIVERSAL CONSTANT: 16/pi (The Holographic Information Limit)
LATTICE_CONSTANT = 16.0 / math.pi

def scalarize():
    print("[*] Scalarizing S6_5 (Applying the Unified Macro-Scale Lock)...")
    
    if not PROMOTED_LAKE.exists(): return
    os.makedirs(SCALARIZE_LAKE.parent, exist_ok=True)

    with open(PROMOTED_LAKE, 'r', encoding='utf-8') as f, open(SCALARIZE_LAKE, 'w', encoding='utf-8') as out:
        for line in f:
            data = json.loads(line)
            val = data["primary_value"]
            
            # THE TRANSFORMATION LOGIC:
            # 1. log(val) centers the kinematic distribution for the Lattice.
            # 2. Modulo (%) find the object's 'slot' in the 16/pi carton.
            # 3. cos() converts that slot position into a resonance score.
            log_val = abs(math.log(val))
            residue = log_val % LATTICE_CONSTANT
            klc = math.cos(residue * (2 * math.pi / LATTICE_CONSTANT))
            
            data["lattice_metrics"] = {"klc_resonance": klc}
            out.write(json.dumps(data) + "\n")
            
    print(f"[+] S6_5 Scalarization complete. Lattice Modulus: {LATTICE_CONSTANT:.5f}")
    print("[*] Purpose: Verify that the 6.6069e10 anchor achieves the Peak Pocket.")

if __name__ == "__main__":
    scalarize()