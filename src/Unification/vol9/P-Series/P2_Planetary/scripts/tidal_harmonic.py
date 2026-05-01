# vol5/P-Series/P2_Planetary/scripts/tidal_harmonic.py
import math

L = 16.0 / math.pi
GEODETIC_ANCHOR = 42164.0 
OCTAVE = L * 2.0

def run_tidal_audit():
    print("===============================================================")
    print(" 🌍 P2_03: TIDAL HARMONIC (The Hydraulic Lock)")
    print("===============================================================")
    
    # Tidal wave frequencies vs Geodetic tension
    # We are checking if the 'Pulse' of the ocean matches the 'Gate' of the Moon
    tidal_data = {
        "M2 Principal Lunar": 12.42, # Hours
        "S2 Principal Solar": 12.00,
        "N2 Larger Elliptic": 12.66,
        "441k Redline Pulse": 13.00  # Theoretical limit
    }

    print(f"{'Tidal Component'.ljust(20)} | {'Phase Value'.ljust(12)} | {'Lattice Match'}")
    print("-" * 60)

    for name, t in tidal_data.items():
        # Treat time-frequency as a spatial-scalar for the audit
        phi = abs(math.log(t)) % OCTAVE
        phase_pos = phi / OCTAVE
        
        # Check if it falls into the same 0.21 - 0.23 corridor
        match = "MATCH [LOCKED]" if 0.21 <= phase_pos <= 0.24 else "FLUID"
        
        bar = "█" * int(phase_pos * 40)
        print(f"{name.ljust(20)} | {phase_pos:.5f}".ljust(35), f"| {match.ljust(15)} {bar}")

if __name__ == "__main__":
    run_tidal_audit()