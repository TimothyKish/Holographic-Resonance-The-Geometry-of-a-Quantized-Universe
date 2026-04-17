# vol5/P-Series/NP1_2_NormalizedNull/scripts/scalarize.py
import json
import math
from pathlib import Path

PROMOTED_LAKE = Path("../lake/np1_2_promoted.jsonl")
SCALARIZE_LAKE = Path("../lake/np1_2_scalarized.jsonl")
LATTICE_CONSTANT = 16.0 / math.pi

def scalarize():
    print("[*] Scalarizing NP1_2 Null...")
    with open(PROMOTED_LAKE, 'r', encoding='utf-8') as f, open(SCALARIZE_LAKE, 'w', encoding='utf-8') as out:
        for line in f:
            data = json.loads(line)
            val = data["primary_value"]
            if val <= 0: continue
            log_val = abs(math.log(val))
            residue = log_val % LATTICE_CONSTANT
            klc = math.cos(residue * (2 * math.pi / LATTICE_CONSTANT))
            data["lattice_metrics"] = {"klc_resonance": klc}
            out.write(json.dumps(data) + "\n")
    print("[+] Scalarization complete.")

if __name__ == "__main__":
    scalarize()