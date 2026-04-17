# vol5/P-Series/P2_Planetary/scripts/seismic_snap.py
import math

L = 16.0 / math.pi
GEODETIC_ANCHOR = 42164.0 
C = L * 2.0 # Testing against the Octave Ridge

def run_seismic_audit():
    print("===============================================================")
    print(" 🌍 P2_02: SEISMIC SNAP (The Edge of the Gate)")
    print("===============================================================")
    
    # Distance of the Moon at the time of 4 major historical quakes (Simulated)
    # We want to see how close they are to the 441k "Phase Edge"
    events = {
        "Baseline Mean": 384400,
        "Historic Event A": 405000,
        "Historic Event B": 439000, # Very close to Redline
        "441k Limit": 441000
    }

    print(f"{'Event Source'.ljust(20)} | {'Phase Value'.ljust(12)} | {'Proximity to Snap'}")
    print("-" * 60)

    for name, d in events.items():
        val = d / GEODETIC_ANCHOR
        phi = abs(math.log(val)) % C
        phase_pos = phi / C # Normalized 0 to 1
        
        # Proximity to the "Edge" of the gate (0.0 or 1.0)
        snap_proximity = abs(0.5 - abs(phase_pos - 0.5)) 
        
        bar = "█" * int(snap_proximity * 40)
        print(f"{name.ljust(20)} | {phase_pos:.5f}".ljust(35), f"| {snap_proximity:.5f} {bar}")

if __name__ == "__main__":
    run_seismic_audit()