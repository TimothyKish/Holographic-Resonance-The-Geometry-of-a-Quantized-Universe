# vol5/P-Series/P2_Planetary/scripts/atmospheric_drag.py
import math

L = 16.0 / math.pi
OCTAVE = L * 2.0

def run_atmospheric_audit():
    print("===============================================================")
    print(" 🌍 P2_04: ATMOSPHERIC DRAG (The Final Gradient)")
    print("===============================================================")
    
    # Atmospheric scale heights and orbital decay periods (Hours)
    layers = {
        "Troposphere Scale": 8.5, 
        "Stratosphere Scale": 20.0,
        "Low Earth Orbit": 1.5,
        "441k Redline Limit": 13.0
    }

    print(f"{'Atmospheric Layer'.ljust(20)} | {'Phase Value'.ljust(12)} | {'Lattice Position'}")
    print("-" * 60)

    for name, val in layers.items():
        phi = abs(math.log(val)) % OCTAVE
        phase_pos = phi / OCTAVE
        
        # Mapping the Gradient
        state = "CORE" if phase_pos < 0.20 else "CAGE" if phase_pos < 0.23 else "FLUID"
        
        bar = "█" * int(phase_pos * 40)
        print(f"{name.ljust(20)} | {phase_pos:.5f}".ljust(35), f"| {state.ljust(10)} {bar}")

if __name__ == "__main__":
    run_atmospheric_audit()