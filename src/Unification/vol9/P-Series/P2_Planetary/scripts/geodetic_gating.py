# vol5/P-Series/P2_Planetary/scripts/geodetic_gating.py
import math
import statistics

# The Universal Lattice Constant
L = 16.0 / math.pi  # ~5.093
# Geostationary Radius (The Earth's "Center of Gravity" for the Lattice)
GEODETIC_ANCHOR = 42164.0 

def run_geodetic_audit():
    print("===============================================================")
    print(" 🌍 P2_01: GEODETIC GATING (The 441k Redline)")
    print("===============================================================")
    
    # Critical Earth-Moon distances (km)
    # Perigee (Closest), Mean (Average), Apogee (Farthest), Redline (Snap Point)
    data = {
        "Lunar Perigee": 363300,
        "Lunar Mean": 384400,
        "Lunar Apogee": 405500,
        "441k Redline": 441000
    }
    
    gates = [
        ("LATTICE ROOT", L),
        ("THERMAL BRIDGE", L * 1.8),
        ("OCTAVE REDLINE", L * 2.0)
    ]

    for label, c in gates:
        print(f"\n--- Testing {label} (C = {c:.3f}) ---")
        bins = [0] * 10
        results = []
        
        for name, d in data.items():
            # Normalize distance by the Geostationary Anchor
            val = d / GEODETIC_ANCHOR
            # The Invariant Transform
            phi = abs(math.log(val)) % c
            idx = int((phi / c) * 10)
            if idx >= 10: idx = 9
            bins[idx] += 1
            results.append((name, idx))
        
        # Visualize the 'Banding'
        for i, count in enumerate(bins):
            bar = "█" * count if count > 0 else "-"
            # Label which specific distance landed in which bin
            occupants = [r[0] for r in results if r[1] == i]
            occupant_str = f" [{', '.join(occupants)}]" if occupants else ""
            print(f"Bin {i}: {bar.ljust(12)} ({count}){occupant_str}")

if __name__ == "__main__":
    run_geodetic_audit()