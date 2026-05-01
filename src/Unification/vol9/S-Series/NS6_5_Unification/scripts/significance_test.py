# vol5/S-Series/NS6_5_Unification/scripts/significance_test.py
import json
import math
import statistics
import random
from pathlib import Path

SOURCE_LAKE = Path("../../S6_Galactic/lake/s6_galactic_sovereign_raw.jsonl")
LATTICE = 16.0 / math.pi
ANCHOR = 6.6069e10

def get_jitter(group):
    klcs = []
    for gal in group:
        val = ((gal["v_dispersion_kms"]**4) / (10**((25 - gal["magnitude_r"]) / 2.5))) / ANCHOR
        klcs.append(math.cos((abs(math.log(val)) % LATTICE) * (2 * math.pi / LATTICE)))
    return statistics.stdev(klcs)

def run_significance_test():
    print("===============================================================")
    print(" 🛡️ NS6_17: MONTE CARLO SIGNIFICANCE (The Final Probability)")
    print("===============================================================")
    
    galaxies = []
    with open(SOURCE_LAKE, 'r', encoding='utf-8') as f:
        for line in f: galaxies.append(json.loads(line))

    # 1. Observed Gap (Red Jitter - Blue Jitter)
    galaxies.sort(key=lambda x: (x["v_dispersion_kms"]**4) / (10**((25 - x["magnitude_r"]) / 2.5)))
    mid = len(galaxies) // 2
    obs_red_jitter = get_jitter(galaxies[mid:])
    obs_blue_jitter = get_jitter(galaxies[:mid])
    observed_gap = obs_red_jitter - obs_blue_jitter

    # 2. Permutation Test (Shuffle 1000 times)
    hit_count = 0
    iterations = 1000
    for _ in range(iterations):
        random.shuffle(galaxies)
        random_gap = get_jitter(galaxies[mid:]) - get_jitter(galaxies[:mid])
        if random_gap >= observed_gap:
            hit_count += 1
            
    p_value = hit_count / iterations
    
    print(f"Observed Jitter Gap: {observed_gap:.5f}")
    print(f"P-Value (Probability of Chance): {p_value:.5f}")
    print("-" * 63)
    
    if p_value < 0.05:
        print("[+] VERDICT: STATISTICALLY SIGNIFICANT (Lattice Torque)")
        print("    The Red galaxies are uniquely unstable.")
    else:
        print("[!] VERDICT: NOT SIGNIFICANT (Phoenix is Right)")
        print("    This gap could be a random quirk of the sample.")

if __name__ == "__main__":
    run_significance_test()