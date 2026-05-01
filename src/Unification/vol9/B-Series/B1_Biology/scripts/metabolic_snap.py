# B-Series/B1_Biology/scripts/metabolic_snap.py
import math

L = 16.0 / math.pi
THERMAL = L * 1.8

def run_metabolic_audit():
    print("===============================================================")
    print(" 🧬 B1_02: THE METABOLIC SNAP (The 1.8x Thermal Engine)")
    print("===============================================================")
    
    # Biological Energy Metrics
    # ATP Energy (~30.5 kJ/mol), Human Body Temp (310.15 Kelvin)
    # Heart Rate (72 bpm -> 1.2 Hz)
    bio_energetics = {
        "ATP Hydrolysis": 30.5,
        "Body Temp (K)": 310.15,
        "Heart Rate (Hz)": 1.2
    }

    print(f"{'Metric'.ljust(18)} | {'Phase Value'.ljust(12)} | {'Lattice State'}")
    print("-" * 60)

    for name, val in bio_energetics.items():
        phi = abs(math.log(val)) % THERMAL
        phase_pos = phi / THERMAL
        
        # We look for the 1.8x "Thermal Lock"
        state = "LOCKED" if phase_pos < 0.1 or phase_pos > 0.9 else "THERMAL-TORQUE"
        
        bar = "█" * int(phase_pos * 40)
        print(f"{name.ljust(18)} | {phase_pos:.5f}".ljust(35), f"| {state.ljust(15)} {bar}")

if __name__ == "__main__":
    run_metabolic_audit()