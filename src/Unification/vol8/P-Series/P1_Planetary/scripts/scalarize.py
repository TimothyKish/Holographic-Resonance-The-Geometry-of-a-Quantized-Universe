# vol5/P-Series/P1_Planetary/scripts/scalarize.py
import json
import math
from pathlib import Path

PROMOTED_LAKE = Path("../lake/p1_planetary_promoted.jsonl")
SCALARIZE_LAKE = Path("../lake/p1_planetary_scalarized.jsonl")
LATTICE_CONSTANT = 16.0 / math.pi

def scalarize():
    print("===============================================================")
    print(" 🪐 SCALARIZING P1_PLANETARY (Testing Orbital Resonance)")
    print("===============================================================")
    
    with open(PROMOTED_LAKE, 'r', encoding='utf-8') as f, open(SCALARIZE_LAKE, 'w', encoding='utf-8') as out:
        for line in f:
            try:
                data = json.loads(line)
                val = data["primary_value"]
                
                if val <= 0: continue
                log_val = abs(math.log(val))
                residue = log_val % LATTICE_CONSTANT
                klc = math.cos(residue * (2 * math.pi / LATTICE_CONSTANT))
                
                data["lattice_metrics"] = {
                    "log_value": log_val,
                    "residue": residue,
                    "klc_resonance": klc
                }
                out.write(json.dumps(data) + "\n")
            except Exception: continue
            
    print("[+] Scalarization complete. The Solar System and Exoplanets are mapped.")

if __name__ == "__main__":
    scalarize()