# vol7/S-Series/S7_Solar/scripts/thermal_leak.py
import math

L = 16.0 / math.pi
THERMAL = L * 1.8
OCTAVE = L * 2.0

def run_leak_audit():
    print("===============================================================")
    print(" ☀️ S7_05: THE THERMAL LEAK (The Exhaust Port)")
    print("===============================================================")
    
    # Active Sun data (Turbulent/Flare-like variances)
    # These distances are 'stretched' by magnetic activity
    active_dist = [1.5, 1.8, 1.2, 1.9, 1.4, 2.1, 1.1, 1.5, 1.6, 1.5]

    for label, c in [("1.8x THERMAL GATE", THERMAL), ("2.0x OCTAVE SHIELD", OCTAVE)]:
        print(f"\n--- {label} (C = {c:.3f}) ---")
        bins = [0] * 10
        for d in active_dist:
            phi = abs(math.log(d)) % c
            idx = int((phi / c) * 10)
            if idx >= 10: idx = 9
            bins[idx] += 1
        
        # Output the occupancy to see the 'Leak'
        for i, count in enumerate(bins):
            if count > 0:
                bar = "█" * count
                print(f"Bin {i}: {bar.ljust(12)} ({count})")
            else:
                print(f"Bin {i}: {'-'.ljust(12)} (0)")

if __name__ == "__main__":
    run_leak_audit()