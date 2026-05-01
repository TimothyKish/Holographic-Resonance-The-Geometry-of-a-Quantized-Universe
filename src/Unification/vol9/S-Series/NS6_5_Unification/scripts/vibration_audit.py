# vol5/S-Series/NS6_5_Unification/scripts/vibration_audit.py
import json
import math
import statistics
from pathlib import Path

SOURCE_LAKE = Path("../../S6_Galactic/lake/s6_galactic_sovereign_raw.jsonl")
LATTICE = 16.0 / math.pi
ANCHOR = 6.6069e10

def run_vibration_audit():
    print("===============================================================")
    print(" 🛡️ NS6_15: THE VIBRATION AUDIT (Measuring the Jitter)")
    print("===============================================================")
    
    galaxies = []
    with open(SOURCE_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            galaxies.append(json.loads(line))

    klc_values = []
    for gal in galaxies:
        L = 10**((25 - gal["magnitude_r"]) / 2.5)
        val = (gal["v_dispersion_kms"]**4) / (L * ANCHOR)
        log_val = abs(math.log(val))
        klc = math.cos((log_val % LATTICE) * (2 * math.pi / LATTICE))
        klc_values.append(klc)
    
    avg_klc = statistics.mean(klc_values)
    stdev_klc = statistics.stdev(klc_values)
    
    # The "Jitter Factor": High variance means the 'Spring' is active.
    print(f"Mean Lattice Resonance: {avg_klc:.5f}")
    print(f"Lattice Phase Jitter:  {stdev_klc:.5f}")
    print("-" * 45)
    
    if stdev_klc > 0.2:
        print("[+] VERDICT: HIGH JITTER DETECTED.")
        print("    The galaxies are 'Wound' at different tensions.")
    else:
        print("[!] VERDICT: STATIC LOCK.")
        print("    The data is too uniform to see the Egg Timer drift.")

if __name__ == "__main__":
    run_vibration_audit()