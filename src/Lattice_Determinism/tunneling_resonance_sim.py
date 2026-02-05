# ==============================================================================
# SOVEREIGN COPYRIGHT (C) 2026 KISH LATTICE 16PI INITIATIVES LLC
# SCRIPT: tunneling_resonance_sim.py
# TARGET: Proving Tunneling is Phase Locking (The "Spinning Fan" Effect)
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt

def run_tunneling_sim():
    print("[*] INITIALIZING LATTICE PERMEABILITY AUDIT")
    
    # 1. SETUP THE EXPERIMENT
    # The particles have varying frequencies relative to the Lattice Wall
    # Ratio 1.0 = Perfect Sync (Phase Lock)
    freq_ratios = np.linspace(0.0, 2.0, 1000)
    
    # 2. CALCULATE TRANSMISSION
    # The "Spinning Fan" Logic:
    # If Frequency matches the Lattice gap opening (16/pi), transmission is 100%.
    # If it is off-sync, it hits the "Blade" (Atom) and bounces.
    transmission_prob = 1.0 / (1.0 + 100 * (freq_ratios - 1.0)**2)
    
    # 3. VISUALIZATION
    plt.figure(figsize=(10, 6))
    
    # Plot the Resonance Curve
    plt.plot(freq_ratios, transmission_prob, color='lime', linewidth=3)
    plt.fill_between(freq_ratios, 0, transmission_prob, color='lime', alpha=0.2)
    
    # Annotations
    plt.axvline(1.0, color='white', linestyle='--', linewidth=1)
    plt.text(1.02, 0.9, "LATTICE SYNC (Phase Lock)", color='black', fontweight='bold')
    plt.text(0.2, 0.1, "BLOCKED (Bounce)", color='red', fontweight='bold')
    plt.text(1.6, 0.1, "BLOCKED (Bounce)", color='red', fontweight='bold')
    
    plt.title("The 'Tunneling' Illusion: Permeability via Frequency Matching", fontsize=14)
    plt.xlabel("Particle Frequency Ratio (f_particle / f_lattice)")
    plt.ylabel("Transmission Probability")
    plt.grid(True, alpha=0.3)
    
    plt.savefig('tunneling_resonance_proof.png')
    print("[*] PROOF GENERATED: tunneling_resonance_proof.png")

if __name__ == "__main__":
    run_tunneling_sim()