# ==============================================================================
# PROJECT: THE 16PI INITIATIVE | MACRO-ARCHITECTURE
# SCRIPT: B4_S1_Grays_Paradox_Resolver.py
# DESCRIPTION: Models Gray's Paradox by comparing standard turbulent drag 
# against a 16/pi Lattice-Corrected slipstream for a marine organism.
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt

# --- 1. UNIVERSAL & PHYSICAL CONSTANTS ---
PI = np.pi
KISH_CONSTANT = 16.0 / PI      # ~5.0929 (The Geometric Impedance)
WATER_DENSITY = 1026.0         # kg/m^3 (Seawater)
DOLPHIN_AREA = 0.4             # m^2 (Approximate frontal area)

# Maximum theoretical sustained muscle power for a dolphin (Watts)
# Sir James Gray noted that required power vastly exceeded this limit.
MAX_MUSCLE_POWER = 2000.0      

def run_grays_paradox_simulation():
    print("[*] INITIALIZING B4: GRAY'S PARADOX LATTICE RESOLVER")
    
    # Velocity range from 0 to 12 m/s (approx 0 to 26 mph)
    velocities = np.linspace(0.1, 12.0, 500)
    
    # --- 2. OLD WORLD MODEL (Standard Turbulent Fluid Dynamics) ---
    # Standard Drag Coefficient for a streamlined body in turbulent water (~0.03)
    standard_cd = 0.03 
    
    # Power = Force_drag * Velocity = (0.5 * density * v^2 * Cd * Area) * v
    old_world_power = 0.5 * WATER_DENSITY * (velocities**3) * standard_cd * DOLPHIN_AREA
    
    # --- 3. NEW WORLD MODEL (16/pi Lattice-Corrected Slipstream) ---
    # In the framework, compliant skin acts as a resonant dampener.
    # We apply the Kish Modulus to effectively reduce the drag coefficient 
    # by allowing the organism to "ride the grain" of the lattice.
    lattice_correction_factor = 1.0 / KISH_CONSTANT 
    lattice_cd = standard_cd * lattice_correction_factor
    
    new_world_power = 0.5 * WATER_DENSITY * (velocities**3) * lattice_cd * DOLPHIN_AREA

    # --- 4. IDENTIFYING THE PARADOX THRESHOLD ---
    # Find the speed where Old World physics exceeds biological reality
    paradox_index = np.argmax(old_world_power > MAX_MUSCLE_POWER)
    paradox_velocity = velocities[paradox_index]
    
    print(f"[*] STANDARD DRAG EXCEEDS MUSCLE LIMIT AT: {paradox_velocity:.2f} m/s")
    print(f"[*] LATTICE CORRECTION FACTOR APPLIED: {lattice_correction_factor:.4f}")

    # --- 5. VISUALIZATION ---
    plt.figure(figsize=(12, 7))
    
    # Plot Old World
    plt.plot(velocities, old_world_power, 'r--', linewidth=2, 
             label='Old World (Standard Turbulent Drag)')
    
    # Plot New World
    plt.plot(velocities, new_world_power, 'b-', linewidth=3, 
             label=f'New World (16/π Lattice Slipstream)')
    
    # Plot Biological Limit
    plt.axhline(y=MAX_MUSCLE_POWER, color='g', linestyle='-.', linewidth=2, 
                label='Biological Muscle Power Limit (Gray\'s Baseline)')
    
    # Highlight the "Paradox Zone"
    plt.fill_between(velocities, old_world_power, MAX_MUSCLE_POWER, 
                     where=(old_world_power > MAX_MUSCLE_POWER), 
                     color='red', alpha=0.15, label='Gray\'s Paradox (Impossible Zone)')
    
    plt.title("GRAY'S PARADOX RESOLVED: Fluid Dynamics vs. Lattice Impedance", fontsize=14, fontweight='bold')
    plt.xlabel("Velocity (m/s)", fontsize=12)
    plt.ylabel("Required Sustained Power (Watts)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(loc='upper left', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('B4_S1_Grays_Paradox.png')
    
    print("[*] SIMULATION COMPLETE: Output saved as 'B4_S1_Grays_Paradox.png'")

if __name__ == "__main__":
    run_grays_paradox_simulation()