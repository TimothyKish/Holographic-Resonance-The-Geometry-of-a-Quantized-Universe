# vol7/S-Series/S7_Solar/scripts/solar_cycle_drift.py
import math
import statistics

L = 16.0 / math.pi

def run_drift_audit():
    print("===============================================================")
    print(" ☀️ S7_02: SOLAR CYCLE DRIFT (Peak Activity Audit)")
    print("===============================================================")
    
    # Using the same spatial distances to check the 'Drift' toward the Null
    distances = [1.2, 1.5, 1.8, 2.1, 1.5, 1.4, 1.9, 2.2, 1.5, 1.6] * 5

    # Sweep from 1.8 (Thermal) to 1.9 (Null) to 2.0 (Octave)
    multipliers = [1.8, 1.85, 1.9, 1.95, 2.0]
    
    print(f"{'Multiplier'.ljust(12)} | {'Resonance'.ljust(12)} | {'Jitter (Strain)'}")
    print("-" * 45)

    for m in multipliers:
        c = L * m
        klcs = []
        for d in distances:
            phi = abs(math.log(d)) % c
            klcs.append(math.cos((phi / c) * (2 * math.pi)))
        
        res = statistics.mean(klcs)
        jit = statistics.stdev(klcs)
        print(f"{m:.2f}x L".ljust(12), f"| {res:.5f}".ljust(12), f"| {jit:.5f}")

if __name__ == "__main__":
    run_drift_audit()