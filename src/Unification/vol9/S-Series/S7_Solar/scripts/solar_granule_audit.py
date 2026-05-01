# vol7/S-Series/S7_Solar/scripts/solar_granule_audit.py
import math
import statistics

# Lattice Constants
L = 16.0 / math.pi
THERMAL_GATE = L * 1.8  # 9.167

def run_solar_audit():
    print("===============================================================")
    print(" ☀️ S7_01: SOLAR GRANULATION (The Thermal Fingerprint)")
    print("===============================================================")
    
    # We are auditing the "Typical" size of a solar granule (~1.5 arcsec)
    # in relation to the Lattice Constant.
    
    # Simulated spatial distances (d) in a high-resolution HMI crop
    # These represent the 'voids' between convection cells.
    simulated_distances = [1.2, 1.5, 1.8, 2.1, 1.5, 1.4, 1.9, 2.2, 1.5, 1.6] * 5 

    gates = [
        ("BASE LATTICE", L),
        ("SOLAR THERMAL", THERMAL_GATE)
    ]

    for label, c in gates:
        print(f"\n--- Testing {label} (C = {c:.3f}) ---")
        klcs = []
        for d in simulated_distances:
            # We treat the distance as a log-spatial frequency
            phi = abs(math.log(d)) % c
            klc = math.cos((phi / c) * (2 * math.pi))
            klcs.append(klc)
        
        avg_res = statistics.mean(klcs)
        jitter = statistics.stdev(klcs)
        print(f"Resonance: {avg_res:.5f}")
        print(f"Jitter:    {jitter:.5f}")

if __name__ == "__main__":
    run_solar_audit()