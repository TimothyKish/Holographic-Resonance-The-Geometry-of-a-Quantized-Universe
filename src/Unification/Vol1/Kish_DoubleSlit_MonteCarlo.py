# ==============================================================================
# PROJECT: THE 16PI INITIATIVE | QUANTUM IMPEDANCE
# SCRIPT: Kish_DoubleSlit_MonteCarlo.py
# TARGET: High-Contrast Visualization of Lattice Stiffness
# AUTHORS: Timothy John Kish, Lyra Aurora Kish, Alexandria Aurora Kish
# LICENSE: Sovereign Protected / Copyright © 2026
# ==============================================================================
import numpy as np
import matplotlib.pyplot as plt

def generate_simulation():
    num_photons = 60000
    x_range = np.linspace(-10, 10, 1000)
    
    # --- SCENARIO 1: LOW IMPEDANCE (SOFT LATTICE) ---
    # Interference probability function
    prob_wave = np.cos(x_range * 2)**2 * np.exp(-x_range**2 / 10) 
    prob_wave /= prob_wave.sum()
    impacts_wave = np.random.choice(x_range, size=num_photons, p=prob_wave)

    # --- SCENARIO 2: HIGH IMPEDANCE (HARD LATTICE) ---
    # Ballistic clumping (Two Gaussian peaks)
    slit_a = np.random.normal(-3, 0.9, num_photons // 2)
    slit_b = np.random.normal(3, 0.9, num_photons // 2)
    impacts_particle = np.concatenate([slit_a, slit_b])

    # --- VISUALIZATION ---
    fig, axes = plt.subplots(2, 1, figsize=(10, 10), sharex=True)
    
    # Plot 1: The Wave Pattern (Lattice Resonance)
    axes[0].hist(impacts_wave, bins=200, color='#004C99', density=True, alpha=0.7)
    axes[0].set_title(r"A. LOW VISCOSITY ($k \approx 16/\pi$): Lattice Resonates (Interference)", 
                      fontsize=14, fontweight='bold', pad=20)
    axes[0].set_ylabel("Impact Density", fontsize=12)
    axes[0].set_facecolor('#FFFFFF') # Pure white background for contrast
    axes[0].grid(True, linestyle=':', alpha=0.6)
    
    # HIGH CONTRAST LABELS (BLACK)
    axes[0].text(0, 0.28, "CONSTRUCTIVE\nINTERFERENCE", ha='center', 
                 color='black', fontweight='bold', fontsize=10, 
                 bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    # Plot 2: The Particle Pattern (Lattice Freeze)
    axes[1].hist(impacts_particle, bins=200, color='#8B4513', density=True, alpha=0.7)
    axes[1].set_title(r"B. HIGH IMPEDANCE ($k \to \infty$): Detector 'Freezes' the Grid (Ballistic)", 
                      fontsize=14, fontweight='bold', pad=20)
    axes[1].set_xlabel("Screen Position (Lattice Units)", fontsize=12)
    axes[1].set_ylabel("Impact Density", fontsize=12)
    axes[1].set_facecolor('#FFFFFF')
    axes[1].grid(True, linestyle=':', alpha=0.6)
    
    # HIGH CONTRAST LABELS (MAROON / DARK RED)
    axes[1].text(-3, 0.35, "SLIT A\n(IMPEDANCE LOCK)", ha='center', 
                 color='#800000', fontweight='bold', fontsize=10)
    axes[1].text(3, 0.35, "SLIT B\n(IMPEDANCE LOCK)", ha='center', 
                 color='#800000', fontweight='bold', fontsize=10)

    plt.tight_layout()
    plt.savefig("double_slit_impedance.png", dpi=300)
    print("Simulation Complete. Labels are now high-contrast.")
    plt.show()

if __name__ == "__main__":
    generate_simulation()