# vol7/S-Series/S7_Solar/scripts/magnetic_snap.py
import math

L = 16.0 / math.pi
OCTAVE = L * 2.0

def run_snap_audit():
    print("===============================================================")
    print(" ☀️ S7_04: MAGNETIC SNAP (The Release Valve)")
    print("===============================================================")
    
    # "Quiet Sun" Distances (The 100% Lock we just saw)
    quiet_dist = [1.5] * 10 
    
    # "Flare/Active Sun" Distances (Simulating magnetic turbulence)
    # These distances represent the lattice "stretching" under magnetic torque
    active_dist = [1.5, 1.8, 1.2, 1.9, 1.4, 2.1, 1.1, 1.5, 1.6, 1.5]

    for label, data in [("QUIET SUN (Lattice Crystal)", quiet_dist), ("ACTIVE SUN (Lattice Strain)", active_dist)]:
        print(f"\n--- {label} ---")
        bins = [0] * 10
        for d in data:
            phi = abs(math.log(d)) % OCTAVE
            idx = int((phi / OCTAVE) * 10)
            bins[idx if idx < 10 else 9] += 1
        
        for i, count in enumerate(bins):
            if count > 0:
                print(f"Bin {i}: {'█' * count} ({count})")

if __name__ == "__main__":
    run_snap_audit()