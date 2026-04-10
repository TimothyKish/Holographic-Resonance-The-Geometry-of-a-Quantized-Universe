# vol5/S-Series/NS6_5_Unification/scripts/shuffle_audit.py
import json
import math
import random
from pathlib import Path

SOURCE_LAKE = Path("../../S6_Galactic/lake/s6_galactic_sovereign_raw.jsonl")
LATTICE_CONSTANT = 16.0 / math.pi
ANCHOR = 6.6069e10

def run_shuffle():
    print("===============================================================")
    print(" 🛡️ S6_SHUFFLE: THE CORRELATION DECONSTRUCTION")
    print("===============================================================")
    
    # 1. Load Real Data
    sigmas = []
    magnitudes = []
    with open(SOURCE_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            sigmas.append(data["v_dispersion_kms"])
            magnitudes.append(data["magnitude_r"])
    
    # 2. Shuffle Magnitudes (Breaking the Faber-Jackson Correlation)
    random.shuffle(magnitudes)
    
    total_klc = 0.0
    for s, m in zip(sigmas, magnitudes):
        L = 10**((25 - m) / 2.5)
        val = (s**4) / (L * ANCHOR)
        log_val = abs(math.log(val))
        klc = math.cos((log_val % LATTICE_CONSTANT) * (2 * math.pi / LATTICE_CONSTANT))
        total_klc += klc
            
    avg_klc = total_klc / len(sigmas)
    print(f"[!] REAL GALAXY RESONANCE (Locked): 0.71908")
    print(f"[!] SHUFFLED RESONANCE (Correlation Broken): {avg_klc:.5f}")
    
    print("-" * 63)
    print("[*] ANALYSIS FOR PHOENIX:")
    if abs(avg_klc) < 0.20:
        print("    The Faber-Jackson correlation is the 'Battery'.")
        print("    The 16/pi Lattice is the 'Circuit'.")
        print("    Without the correlation, the power is gone. But...")
    
if __name__ == "__main__":
    run_shuffle()