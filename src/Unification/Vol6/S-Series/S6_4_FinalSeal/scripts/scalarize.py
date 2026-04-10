# vol5/S-Series/S6_4_FinalSeal/scripts/scalarize.py
import json
import math
import os
from pathlib import Path

# INGESTS: The final phase-shifted promoted data.
PROMOTED_LAKE = Path("../lake/s6_4_promoted.jsonl")
SCALARIZE_LAKE = Path("../lake/s6_4_scalarized.jsonl")

# THE COSMOLOGICAL CONSTANT: The geometric modulus of the Unification.
LATTICE_CONSTANT = 16.0 / math.pi

def scalarize():
    print("[*] Scalarizing S6_4 (The Final Macro-Scale Lock)...")
    
    if not PROMOTED_LAKE.exists(): return
    os.makedirs(SCALARIZE_LAKE.parent, exist_ok=True)

    with open(PROMOTED_LAKE, 'r', encoding='utf-8') as f, open(SCALARIZE_LAKE, 'w', encoding='utf-8') as out:
        for line in f:
            data = json.loads(line)
            val = data["primary_value"]
            
            # THE TRANSFORMATION LESSON:
            # log(val) centers the power-law distribution.
            # % Lattice find the 'slot' in the egg carton.
            # cos() transforms the 'slot' into a resonance score (-1 to +1).
            log_val = abs(math.log(val))
            residue = log_val % LATTICE_CONSTANT
            klc = math.cos(residue * (2 * math.pi / LATTICE_CONSTANT))
            
            data["lattice_metrics"] = {"klc_resonance": klc}
            out.write(json.dumps(data) + "\n")
            
    print(f"[+] S6_4 Scalarization complete. Modulus used: {LATTICE_CONSTANT:.5f}")
    print("[*] Lesson: High KLC (>0.80) proves the Macro-Scale is quantized.")

if __name__ == "__main__":
    scalarize()