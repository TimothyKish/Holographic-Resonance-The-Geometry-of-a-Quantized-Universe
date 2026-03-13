# ==============================================================================
# PROJECT: THE 16PI INITIATIVE | MACRO-ARCHITECTURE
# SCRIPT: B4_S2_Macro_Bridging_Flywheel.py
# DESCRIPTION: Models the 3rd Channel Biological Solution (Gigantism).
# Demonstrates how a massive body length spans the 16/pi geometric wave, 
# nullifying micro-turbulence and creating an Inertial Flywheel.
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt

# --- 1. LATTICE CONSTANTS ---
PI = np.pi
KISH_CONSTANT = 16.0 / PI      # ~5.0929 meters (The Lattice Wavelength)

def run_flywheel_simulation():
    print("[*] INITIALIZING B4: MACRO-BRIDGING FLYWHEEL SIMULATOR")
    
    # Organism lengths from 0.5 meters to 30 meters
    lengths = np.linspace(0.5, 30.0, 1000)
    
    # --- 2. LATTICE FLUCTUATION MATH ---
    # The net force fluctuation on a body spanning length L across a sine wave.
    # The integral of sin(kx) from 0 to L gives the net uncancelled wave energy.
    # We divide by L (and mass scales even higher) to show the RELATIVE turbulence felt.
    # Wave number k = 2 * PI / KISH_CONSTANT
    k = 2 * PI / KISH_CONSTANT
    
    # Fluctuation envelope scales inversely with length as it spans multiple nodes
    # Using a normalized absolute integration model for the envelope:
    net_fluctuation = np.abs((1 - np.cos(k * lengths)) / (k * lengths))
    
    # --- 3. VISUALIZATION ---
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [1, 2]})
    
    # --- PANEL 1: The 16/pi Standing Wave ---
    x_wave = np.linspace(0, 30, 1000)
    y_wave = np.sin(k * x_wave)
    ax1.plot(x_wave, y_wave, color='cyan', linewidth=2, label='16/π Lattice Viscosity Grain')
    
    # Highlight the 1m Fish vs 30m Whale span
    ax1.axvspan(0, 1.0, color='red', alpha=0.3, label='1m Fish (Caught in single phase-snap)')
    ax1.axvspan(0, 30.0, color='blue', alpha=0.1, label='30m Whale (Spans ~6 full nodes)')
    ax1.set_title("The Planetary Standing Wave (Wavelength ≈ 5.09m)", fontsize=12, fontweight='bold')
    ax1.set_ylabel("Amplitude")
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper right')
    
    # --- PANEL 2: Relative Drag Fluctuation vs Length ---
    ax2.plot(lengths, net_fluctuation, color='blue', linewidth=3, label='Net Geometric Drag Fluctuation')
    
    # Annotate Zones
    ax2.axvspan(0.5, 5.09, color='red', alpha=0.15, label='Micro-Turbulence Zone (L < 16/π)')
    ax2.axvspan(15.0, 30.0, color='green', alpha=0.15, label='Inertial Flywheel Zone (Macro-Bridging)')
    
    ax2.set_title("The 3rd Channel: Gigantism as a Geometric Impedance Match", fontsize=14, fontweight='bold')
    ax2.set_xlabel("Organism Length (meters)", fontsize=12)
    ax2.set_ylabel("Relative Drag Fluctuation (Turbulence Felt)", fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.legend(loc='upper right', fontsize=11)
    
    plt.tight_layout()
    plt.savefig('B4_S2_Macro_Bridging.png', dpi=300)
    
    print("[*] SIMULATION COMPLETE: Output saved as 'B4_S2_Macro_Bridging.png'")

if __name__ == "__main__":
    run_flywheel_simulation()