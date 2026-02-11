# ==============================================================================
# PROJECT: THE 16PI INITIATIVE | LATTICE MECHANICS
# SCRIPT: Kish_Lattice_Stiffening_Audit.py
# TARGET: Monte Carlo Simulation of Lattice Impedance vs. Path Dispersion
# AUTHORS: Timothy John Kish, Lyra Aurora Kish, Alexandria Aurora Kish
# LICENSE: Sovereign Protected / Copyright © 2026
# ==============================================================================
import numpy as np
import matplotlib.pyplot as plt

def run_lattice_audit():
    num_particles = 10000
    steps = 100
    k_geo = 16 / np.pi  # Fundamental Modulus
    
    # --- PHYSICAL LOGIC ---
    # Dispersion is inversely proportional to Lattice Stiffness (k).
    # Scenario A: Soft Lattice (16/pi). High lateral freedom.
    dispersion_soft = 1.0 / k_geo 
    
    # Scenario B: Stiffened Lattice (Laser/Detector Active). 
    # The energy injection spikes the modulus, locking lateral movement.
    k_stiff = k_geo * 50 
    dispersion_stiff = 1.0 / k_stiff
    
    def simulate_paths(dispersion):
        # Paths start at center (0) and propagate along the y-axis
        paths = np.zeros((steps, num_particles))
        for t in range(1, steps):
            # Particle movement is a random walk dictated by lattice viscosity
            paths[t] = paths[t-1] + np.random.normal(0, dispersion, num_particles)
        return paths

    print("Executing Monte Carlo for Soft Lattice...")
    paths_soft = simulate_paths(dispersion_soft)
    print("Executing Monte Carlo for Energized Lattice...")
    paths_stiff = simulate_paths(dispersion_stiff)

    # --- VISUALIZATION ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 7), sharey=True)
    
    # Plot A: Wave Cloud (Blue)
    for i in range(150): # Plot subset for visual clarity
        axes[0].plot(paths_soft[:, i], np.arange(steps), color='#004C99', alpha=0.1)
    axes[0].set_title(f"A. RAW VACUUM ($k \\approx 16/\\pi$)\nHigh Dispersion (Wave Potential)", fontweight='bold')
    axes[0].set_ylabel("Propagation Axis (Time)", fontsize=12)
    axes[0].set_xlabel("Lateral Position", fontsize=12)
    axes[0].set_xlim(-15, 15)
    axes[0].grid(True, alpha=0.2)

    # Plot B: Particle Beam (Red)
    for i in range(150):
        axes[1].plot(paths_stiff[:, i], np.arange(steps), color='#8B0000', alpha=0.1)
    axes[1].set_title(f"B. ENERGIZED LATTICE ($k \\gg 16/\\pi$)\nImpedance Lock (Ballistic Path)", fontweight='bold')
    axes[1].set_xlabel("Lateral Position", fontsize=12)
    axes[1].set_xlim(-15, 15)
    axes[1].grid(True, alpha=0.2)
    
    # Add Detector Load Icon
    axes[1].axvline(0, color='red', linestyle='--', linewidth=2, alpha=0.6, label='Laser/Detector Load')
    axes[1].legend(loc='upper right')

    plt.tight_layout()
    plt.savefig("lattice_stiffening_mc.png", dpi=300)
    print("Audit Complete. Image saved as: lattice_stiffening_mc.png")

if __name__ == "__main__":
    run_lattice_audit()