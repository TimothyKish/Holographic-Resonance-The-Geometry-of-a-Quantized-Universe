# vol5/S-Series/NS6_5_Unification/scripts/torque_audit.py
import json
import math
from pathlib import Path

SOURCE_LAKE = Path("../../S6_Galactic/lake/s6_galactic_sovereign_raw.jsonl")
LATTICE = 16.0 / math.pi
ANCHOR = 6.6069e10

def run_torque_audit():
    print("===============================================================")
    print(" 🛡️ NS6_14_v2: THE TORQUE AUDIT (The Balanced Egg Timer)")
    print("===============================================================")
    
    galaxies = []
    if not SOURCE_LAKE.exists(): return
    with open(SOURCE_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            g = json.loads(line)
            # Calculate a 'Stiffness' proxy for sorting
            g["stiffness"] = (g["v_dispersion_kms"]**4) / (10**((25 - g["magnitude_r"]) / 2.5))
            galaxies.append(g)

    # Sort by stiffness to ensure we have a balanced split
    galaxies.sort(key=lambda x: x["stiffness"])
    mid = len(galaxies) // 2
    
    blue_galaxies = galaxies[:mid]  # Lower relative stiffness (Younger/Lower Torque)
    red_galaxies = galaxies[mid:]   # Higher relative stiffness (Older/High Torque)

    print(f"Auditing Phase-Drift: {len(blue_galaxies)} Blue vs {len(red_galaxies)} Red...")
    print("-" * 55)

    for label, group in [("BLUE (Low Torque)", blue_galaxies), ("RED (High Torque)", red_galaxies)]:
        if len(group) == 0: continue
        
        total_klc = 0.0
        for gal in group:
            val = gal["stiffness"] / ANCHOR
            log_val = abs(math.log(val))
            klc = math.cos((log_val % LATTICE) * (2 * math.pi / LATTICE))
            total_klc += klc
        
        avg_klc = total_klc / len(group)
        print(f"{label.ljust(20)} | Avg Resonance: {avg_klc:.5f}")

if __name__ == "__main__":
    run_torque_audit()