# vol5/S-Series/S1_Galactic/scripts/scalarize.py
import json
import math
from pathlib import Path

PROMOTED_LAKE = Path("../lake/s1_promoted.jsonl")
SCALARIZE_LAKE = Path("../lake/s1_scalarized.jsonl")
LATTICE_CONSTANT = 16.0 / math.pi

def scalarize():
    print("[*] Scalarizing S1 Galactic Kinematics...")
    with open(PROMOTED_LAKE, 'r', encoding='utf-8') as f, open(SCALARIZE_LAKE, 'w', encoding='utf-8') as out:
        for line in f:
            data = json.loads(line)
            val = data["primary_value"]
            log_val = abs(math.log(val))
            residue = log_val % LATTICE_CONSTANT
            klc = math.cos(residue * (2 * math.pi / LATTICE_CONSTANT))
            data["lattice_metrics"] = {"klc_resonance": klc}
            out.write(json.dumps(data) + "\n")
    print("[+] Scalarization complete.")

if __name__ == "__main__":
    scalarize()