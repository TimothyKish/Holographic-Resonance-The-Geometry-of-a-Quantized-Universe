# ==============================================================================
# PROJECT: THE 16PI INITIATIVE | MACRO-ARCHITECTURE
# SCRIPT: B4_S0_AMOC_Lattice_Grain.py
# DESCRIPTION: Visualizes the quantized 16/pi viscosity grain of the AMOC.
# Demonstrates that ocean currents are not continuous fluids, but structured
# geometric grids governed by the vacuum stiffness modulus.
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt

# --- LATTICE CONSTANTS ---
PI = np.pi
KISH_CONSTANT = 16.0 / PI      # ~5.0929 meters (The Viscosity Grain Wavelength)

def run_amoc_grain_simulation():
    print("[*] INITIALIZING B4: AMOC VISCOSITY GRAIN DIAGNOSTIC")
    
    # Look at a 30-meter stretch of the ocean current (Scale of a Whale)
    distance = np.linspace(0, 30.0, 1000)
    
    # 1. OLD WORLD: Standard Continuous Fluid Dynamics
    # Standard physics assumes a smooth, continuous kinematic viscosity
    standard_viscosity = np.ones_like(distance) * 1.0 
    
    # 2. NEW WORLD: The 16/pi Lattice Grain
    # The ocean has a quantized geometric structure. Viscosity violently 
    # spikes at the phase-snaps (nodes) of the 16/pi grid.
    # We use absolute sine to show the high-tension boundary layers of the grid.
    lattice_tension = np.abs(np.sin(PI * distance / KISH_CONSTANT))
    
    # The actual geometric resistance felt by an organism moving through the water
    # Base viscosity + the 16/pi lattice structural spikes
    geometric_viscosity = 0.5 + (1.5 * lattice_tension)
    
    # --- VISUALIZATION ---
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot Old World Physics
    ax.plot(distance, standard_viscosity, 'r--', linewidth=2, alpha=0.6, 
            label='Old World (Continuous Fluid Viscosity)')
    
    # Plot New World Physics
    ax.plot(distance, geometric_viscosity, 'cyan', linewidth=3, 
            label='New World (16/π Lattice Grain)')
    
    # Highlight the 5.09m Harmonic Nodes (The Phase-Snaps)
    for i in range(1, 6):
        node = i * KISH_CONSTANT
        ax.axvline(x=node, color='white', linestyle=':', alpha=0.5)
        if i == 1:
            ax.text(node + 0.2, 1.8, f'Harmonic Node\n(~{KISH_CONSTANT:.2f}m)', 
                    color='white', fontsize=10, fontweight='bold')

    # Formatting and Aesthetic Styling
    ax.set_facecolor('#0a0f1a') # Deep ocean dark background
    fig.patch.set_facecolor('#0a0f1a')
    
    ax.set_title("THE AMOC LATTICE: Quantized Viscosity Grain ($16/\pi$)", color='white', fontsize=14, fontweight='bold')
    ax.set_xlabel("Distance through Fluid (meters)", color='white', fontsize=12)
    ax.set_ylabel("Relative Geometric Resistance", color='white', fontsize=12)
    
    ax.tick_params(colors='white')
    ax.grid(True, color='#1c2841', linestyle='-', alpha=0.7)
    
    # Custom legend for dark mode
    legend = ax.legend(loc='lower right', facecolor='#0a0f1a', edgecolor='white', fontsize=11)
    for text in legend.get_texts():
        text.set_color("white")
        
    ax.set_ylim(0, 2.5)
    ax.set_xlim(0, 30)
    
    plt.tight_layout()
    plt.savefig('B4_S0_AMOC_Lattice_Grain.png', dpi=300, facecolor='#0a0f1a')
    
    print("[*] SIMULATION COMPLETE: Output saved as 'B4_S0_AMOC_Lattice_Grain.png'")

if __name__ == "__main__":
    run_amoc_grain_simulation()