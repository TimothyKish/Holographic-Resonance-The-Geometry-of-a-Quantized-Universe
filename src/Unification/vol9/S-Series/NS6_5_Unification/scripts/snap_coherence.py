# vol5/S-Series/NS6_5_Unification/scripts/snap_coherence.py
import json
import math
import statistics
from pathlib import Path

SOURCE_LAKE = Path("../../S6_Galactic/lake/s6_galactic_sovereign_raw.jsonl")
LATTICE = 16.0 / math.pi
ANCHOR = 6.6069e10

def run_coherence_audit():
    print("===============================================================")
    print(" 🛡️ NS6_16: THE SNAP-COHERENCE AUDIT")
    print("===============================================================")
    
    galaxies = []
    with open(SOURCE_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            g = json.loads(line)
            g["stiffness"] = (g["v_dispersion_kms"]**4) / (10**((25 - g["magnitude_r"]) / 2.5))
            galaxies.append(g)

    galaxies.sort(key=lambda x: x["stiffness"])
    mid = len(galaxies) // 2
    groups = [("BLUE (Low Torque)", galaxies[:mid]), ("RED (High Torque)", galaxies[mid:])]

    for label, group in groups:
        klcs = []
        for gal in group:
            val = gal["stiffness"] / ANCHOR
            log_val = abs(math.log(val))
            klcs.append(math.cos((log_val % LATTICE) * (2 * math.pi / LATTICE)))
        
        jitter = statistics.stdev(klcs)
        print(f"{label.ljust(20)} | Jitter (StDev): {jitter:.5f}")

if __name__ == "__main__":
    run_coherence_audit()