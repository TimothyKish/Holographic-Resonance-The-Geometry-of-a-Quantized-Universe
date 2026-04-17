# B-Series/B1_Biology/scripts/helical_lock.py
import math

L = 16.0 / math.pi
# DNA constants in Angstroms (A)
DNA_RISE = 3.32  # Rise per base pair
DNA_TURN = 33.2  # Full helical turn (10 base pairs)
DNA_WIDTH = 20.0 # Diameter of the helix

def run_biological_audit():
    print("===============================================================")
    print(" 🧬 B1_01: THE HELICAL LOCK (DNA Lattice Audit)")
    print("===============================================================")
    
    biometric_data = {
        "DNA Base Rise": DNA_RISE,
        "DNA Helical Turn": DNA_TURN,
        "DNA Helix Width": DNA_WIDTH
    }

    # We test against the Root and the Octave
    gates = [
        ("BIOLOGIC ROOT", L),
        ("GENETIC OCTAVE", L * 2.0)
    ]

    for label, c in gates:
        print(f"\n--- Testing {label} (C = {c:.3f}) ---")
        for name, val in biometric_data.items():
            # Log-Modulo Transform
            phi = abs(math.log(val)) % c
            phase_pos = phi / c
            
            # Identify the State
            state = "LOCKED" if phase_pos < 0.1 or phase_pos > 0.9 else "IN-FLIGHT"
            
            bar = "█" * int(phase_pos * 40)
            print(f"{name.ljust(18)} | Phase: {phase_pos:.5f} | {state.ljust(10)} {bar}")

if __name__ == "__main__":
    run_biological_audit()