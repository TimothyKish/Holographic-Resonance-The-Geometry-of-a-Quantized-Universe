# B-Series/B1_Biology/scripts/neural_frequency.py
import math

L = 16.0 / math.pi
OCTAVE = L * 2.0

def run_neural_audit():
    print("===============================================================")
    print(" 🧬 B1_03: NEURAL FREQUENCY (The Alpha-Octave Check)")
    print("===============================================================")
    
    # Brainwave Frequencies (Hz)
    # Delta (0.5-4), Theta (4-8), Alpha (8-13), Beta (13-32)
    brain_waves = {
        "Delta (Sleep)": 2.0,
        "Theta (Deep)": 6.0,
        "Alpha (Relax)": 10.0,
        "Beta (Active)": 20.0
    }

    print(f"{'Brain State'.ljust(18)} | {'Phase Value'.ljust(12)} | {'Lattice State'}")
    print("-" * 60)

    for name, f in brain_waves.items():
        phi = abs(math.log(f)) % OCTAVE
        phase_pos = phi / OCTAVE
        
        # We look for the "Alpha Lock" at the Octave
        state = "LOCKED" if phase_pos < 0.1 or phase_pos > 0.9 else "PROCESSING"
        
        bar = "█" * int(phase_pos * 40)
        print(f"{name.ljust(18)} | {phase_pos:.5f}".ljust(35), f"| {state.ljust(12)} {bar}")

if __name__ == "__main__":
    run_neural_audit()