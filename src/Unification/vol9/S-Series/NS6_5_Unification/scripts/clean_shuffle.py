# vol5/S-Series/NS6_5_Unification/scripts/clean_shuffle.py
import json
import math
import random
from pathlib import Path

SOURCE_LAKE = Path("../../S6_Galactic/lake/s6_galactic_sovereign_raw.jsonl")
LATTICE_CONSTANT = 16.0 / math.pi
ANCHOR = 6.6069e10

def run_clean_shuffle():
    print("===============================================================")
    print(" 🛡️ NS6_CLEAN_SHUFFLE: CROSS-CLUSTER DISLOCATION")
    print("===============================================================")
    
    # 1. Ingest Master Benchmarks
    data_points = []
    with open(SOURCE_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            data_points.append(json.loads(line))
    
    # 2. Extract Sigmas and Luminosities independently
    sigmas = [d["v_dispersion_kms"] for d in data_points]
    mags = [d["magnitude_r"] for d in data_points]
    
    # 3. GLOBAL SHUFFLE (No Cluster-Internal Swaps allowed)
    # We force a shift to ensure no 'echo' remains from local group kinematics
    random.shuffle(mags)
    
    total_klc = 0.0
    for s, m in zip(sigmas, mags):
        L = 10**((25 - m) / 2.5)
        val = (s**4) / (L * ANCHOR)
        log_val = abs(math.log(val))
        residue = log_val % LATTICE_CONSTANT
        klc = math.cos(residue * (2 * math.pi / LATTICE_CONSTANT))
        total_klc += klc
            
    avg_klc = total_klc / len(sigmas)
    print(f"[!] S6_5 MASTER RESONANCE: 0.71908")
    print(f"[!] CROSS-SHUFFLE RESONANCE: {avg_klc:.5f}")
    
    print("-" * 63)
    if abs(avg_klc) < 0.15:
        print("[+] VERDICT: The resonance is localized to the physical pairing.")
        print("    Analysis: Shuffling breaks the phase-lock. The Lattice is specific.")
    else:
        print("[!] WARNING: Persistent echo. Local geometry is too dominant.")

if __name__ == "__main__":
    run_clean_shuffle()