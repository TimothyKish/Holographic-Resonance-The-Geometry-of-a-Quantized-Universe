# vol5/S-Series/NS6_5_Unification/scripts/domain_test.py
import math
import random

LATTICE = 16.0 / math.pi
ANCHOR = 6.6069e10

def get_klc(val_list, c):
    total_klc = 0.0
    for v in val_list:
        log_val = abs(math.log(v))
        klc = math.cos((log_val % c) * (2 * math.pi / c))
        total_klc += klc
    return total_klc / len(val_list)

def run_domain_test():
    print("===============================================================")
    print(" 🛡️ NS6_12: DOMAIN SPECIFICITY (The Phoenix Trap)")
    print("===============================================================")
    
    # 1. THE RANDOM WALK (Phoenix's claim: "Any data works")
    # We simulate 50 "Stock Prices" following a random walk
    random_data = [100.0]
    for _ in range(49):
        random_data.append(random_data[-1] * (1 + random.uniform(-0.05, 0.05)))
    
    # 2. THE LATTICE HARMONICS
    test_points = [1.0, 1.8, 2.0]
    
    print(f"{'Multiplier'.ljust(15)} | {'Random Data KLC'}")
    print("-" * 35)
    
    for m in test_points:
        c = LATTICE * m
        res = get_klc(random_data, c)
        print(f"{str(m).ljust(15)} | {res:.5f}")

if __name__ == "__main__":
    run_domain_test()