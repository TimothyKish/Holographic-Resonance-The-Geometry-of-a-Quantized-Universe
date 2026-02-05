# ==============================================================================
# SOVEREIGN COPYRIGHT (C) 2026 KISH LATTICE 16PI INITIATIVES LLC
# SCRIPT: pilot_wave_sim.py
# TARGET: The Double Slit Resolution (The Boat and the Wake)
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt

def run_pilot_wave_sim():
    print("[*] INITIALIZING 16/PI PILOT WAVE RESOLVER")
    
    # 1. SETUP THE EXPERIMENT
    screen_x = np.linspace(-10, 10, 1000)
    slit_1_pos = -2.0
    slit_2_pos = 2.0
    dist_to_screen = 20.0
    
    # 2. UNIVERSAL CONSTANTS
    # The Lattice Stiffness defines the wave frequency
    kish_stiffness = 16.0 / np.pi 
    k = kish_stiffness # Wave Number

    # 3. CALCULATE DISTANCES (GEOMETRY)
    # The particle goes through ONE slit, but the Lattice Wave goes through BOTH.
    d1 = np.sqrt((screen_x - slit_1_pos)**2 + dist_to_screen**2)
    d2 = np.sqrt((screen_x - slit_2_pos)**2 + dist_to_screen**2)

    # 4. MODE A: UNOBSERVED (Lattice Resonance / The Wake)
    # The waves from both slits interfere. The particle "surfs" this pattern.
    wake_1 = np.cos(k * d1)
    wake_2 = np.cos(k * d2)
    interference_pattern = (wake_1 + wake_2)**2
    # Normalize for plotting
    interference_pattern = interference_pattern / np.max(interference_pattern)

    # 5. MODE B: OBSERVED (Lattice Damping / The Stiff Grid)
    # Measurement (Photon Impact) "calms" the water. No ripples = No interference.
    # The particle travels straight (Ballistic Gaussian).
    ballistic_1 = np.exp(-0.5 * ((screen_x - slit_1_pos * 2.5) / 1.5)**2)
    ballistic_2 = np.exp(-0.5 * ((screen_x - slit_2_pos * 2.5) / 1.5)**2)
    observed_pattern = ballistic_1 + ballistic_2
    observed_pattern = observed_pattern / np.max(observed_pattern)

    # 6. VISUALIZATION
    fig, axes = plt.subplots(2, 1, figsize=(10, 10))
    
    # Plot A: The Surfer
    axes[0].plot(screen_x, interference_pattern, color='blue', linewidth=2)
    axes[0].fill_between(screen_x, 0, interference_pattern, color='blue', alpha=0.3)
    axes[0].set_title(f"MODE A: UNOBSERVED (The Wake)\nParticle Surfs the 16/pi Lattice Vibration", fontsize=12, fontweight='bold')
    axes[0].set_ylabel("Impact Probability")
    axes[0].set_yticks([])
    axes[0].text(-9, 0.9, "Hydrodynamic Interference", style='italic')

    # Plot B: The Ballistic
    axes[1].plot(screen_x, observed_pattern, color='red', linewidth=2, linestyle='--')
    axes[1].fill_between(screen_x, 0, observed_pattern, color='red', alpha=0.3)
    axes[1].set_title(f"MODE B: OBSERVED (Lattice Damping)\nMeasurement Stiffens the Grid -> Ballistic Travel", fontsize=12, fontweight='bold')
    axes[1].set_xlabel("Screen Position")
    axes[1].set_ylabel("Impact Probability")
    axes[1].set_yticks([])

    plt.tight_layout()
    plt.savefig('pilot_wave_proof.png')
    print("[*] PROOF GENERATED: pilot_wave_proof.png")

if __name__ == "__main__":
    run_pilot_wave_sim()