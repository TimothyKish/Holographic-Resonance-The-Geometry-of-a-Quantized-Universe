# vol7/S-Series/S7_Solar/scripts/granule_frequency.py
import math
import statistics

L = 16.0 / math.pi

def run_frequency_audit():
    print("===============================================================")
    print(" ☀️ S7_03: GRANULE FREQUENCY (The Phase-Lock Precision)")
    print("===============================================================")
    
    distances = [1.2, 1.5, 1.8, 2.1, 1.5, 1.4, 1.9, 2.2, 1.5, 1.6] * 5
    c_target = L * 2.0 # Testing the "Quiet" Octave Ridge

    bins = 10
    occupancy = [0] * bins
    for d in distances:
        phi = abs(math.log(d)) % c_target
        bin_idx = int((phi / c_target) * bins)
        if bin_idx == bins: bin_idx -= 1
        occupancy[bin_idx] += 1

    print(f"--- OCTAVE GATE (2.0L) (C = {c_target:.3f}) ---")
    max_occ = max(occupancy)
    for i, count in enumerate(occupancy):
        bar = "█" * int((count / max_occ) * 20) if max_occ > 0 else ""
        print(f"Bin {i}: {bar.ljust(21)} ({count} granules)")

if __name__ == "__main__":
    run_frequency_audit()