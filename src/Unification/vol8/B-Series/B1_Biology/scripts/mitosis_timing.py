# B-Series/B1_Biology/scripts/mitosis_timing.py
import math

L = 16.0 / math.pi
C = L * 2.0 # The Octave Gate

def run_mitosis_audit():
    print("===============================================================")
    print(" 🧬 B1_04: MITOSIS TIMING (The Replication Snap)")
    print("===============================================================")
    
    # Standard biological cycle times (Hours)
    # Cell Cycle (24), Circadian Rhythm (24), Protein Folding (ms -> converted)
    cycles = {
        "Standard Cell Cycle": 24.0,
        "Circadian Rhythm": 24.0,
        "Rapid Yeast Div": 2.0,
        "Protein Folding (Rel)": 0.001 
    }

    print(f"{'Biological Cycle'.ljust(22)} | {'Phase Value'.ljust(12)} | {'Lattice State'}")
    print("-" * 65)

    for name, t in cycles.items():
        phi = abs(math.log(t)) % C
        phase_pos = phi / C
        
        # Checking for the "Life Lock"
        state = "LOCKED" if 0.21 <= phase_pos <= 0.24 else "DRIFTING"
        
        bar = "█" * int(phase_pos * 40)
        print(f"{name.ljust(22)} | {phase_pos:.5f}".ljust(35), f"| {state.ljust(12)} {bar}")

if __name__ == "__main__":
    run_mitosis_audit()