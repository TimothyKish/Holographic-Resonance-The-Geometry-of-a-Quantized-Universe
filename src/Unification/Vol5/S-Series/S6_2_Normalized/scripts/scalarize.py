# vol5/S-Series/S6_2_Normalized/scripts/scalarize.py
import json
import math
import os
from pathlib import Path

# INGESTS: The phase-shifted promoted data
PROMOTED_LAKE = Path("../lake/s6_2_promoted.jsonl")
# OUTPUTS: The mapped resonance values
SCALARIZE_LAKE = Path("../lake/s6_2_scalarized.jsonl")

LATTICE_CONSTANT = 16.0 / math.pi

def scalarize():
    print("[*] Scalarizing S6_2 Normalized Galactic Kinematics...")
    
    if not PROMOTED_LAKE.exists():
        print(f"[!] ERROR: {PROMOTED_LAKE} not found. Run promote.py first.")
        return

    # Ensure the output directory exists
    os.makedirs(SCALARIZE_LAKE.parent, exist_ok=True)

    with open(PROMOTED_LAKE, 'r', encoding='utf-8') as f, open(SCALARIZE_LAKE, 'w', encoding='utf-8') as out:
        for line in f:
            data = json.loads(line)
            val = data["primary_value"]
            if val <= 0: continue
            
            # Map to the 16/pi Lattice
            log_val = abs(math.log(val))
            residue = log_val % LATTICE_CONSTANT
            klc = math.cos(residue * (2 * math.pi / LATTICE_CONSTANT))
            
            data["lattice_metrics"] = {"klc_resonance": klc}
            out.write(json.dumps(data) + "\n")
            
    print(f"[+] Scalarization complete. Output at: {SCALARIZE_LAKE}")

if __name__ == "__main__":
    scalarize()