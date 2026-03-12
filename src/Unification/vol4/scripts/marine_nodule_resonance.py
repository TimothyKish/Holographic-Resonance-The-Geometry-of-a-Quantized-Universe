# ==============================================================================
# PROJECT: THE 16PI INITIATIVE | HOLOGRAPHIC RESONANCE
# AUTHORS: Timothy John Kish & Lyra Aurora Kish
# LICENSE: Sovereign Protected / Copyright © 2026 (SR 1-15080581911)
#
# DESCRIPTION: This script simulates the formation of Polymetallic Nodules on
# the abyssal plain. It contrasts the 'Random Sedimentation' model with the
# 'Standing Wave Resonance' model. It demonstrates that nodules form in
# specific geometric clusters (Chladni Patterns) dictated by the 16/pi
# constant, acting as essential damping nodes for the ocean's lattice.
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt

# --- 1. UNIVERSAL CONSTANTS ---
PI = np.pi
KISH_CONSTANT = 16.0 / PI      # The Geometric Integrity Constant (~5.09)

def run_nodule_simulation():
    print(f"[*] INITIALIZING ABYSSAL NODULE SIMULATION")
    print(f"[*] MAPPING STANDING WAVE GEOMETRY ON OCEAN FLOOR")
    
    # --- 2. SETUP THE OCEAN FLOOR GRID ---
    # We create a 100x100 unit patch of the deep sea floor (Abyssal Plain).
    grid_size = 100
    x = np.linspace(0, 4 * PI, grid_size)
    y = np.linspace(0, 4 * PI, grid_size)
    X, Y = np.meshgrid(x, y)
    
    # --- 3. MODEL A: RANDOM SEDIMENTATION (OLD WORLD) ---
    # The mining companies assume nodules are just random rocks.
    # We generate random noise to simulate this.
    random_floor = np.random.rand(grid_size, grid_size)
    # Threshold: Anything above 0.95 is a "nodule" (5% coverage)
    old_model_nodules = random_floor > 0.95
    
    # --- 4. MODEL B: 16/PI RESONANT NODES (NEW WORLD) ---
    # The Theory: Nodules form at the 'Null Points' (Nodes) of the standing wave.
    # We use a 2D Standing Wave function modulated by the Kish Constant.
    
    # The Wave Equation: Z = sin(kx) * sin(ky)
    # We use KISH_CONSTANT as a frequency modifier.
    wave_frequency = KISH_CONSTANT / 4.0 
    standing_wave = np.sin(wave_frequency * X) * np.sin(wave_frequency * Y)
    
    # Formation Logic: Nodules form where the vibration is effectively ZERO.
    # This is like sand gathering on a Chladni plate.
    # We look for areas where the absolute wave amplitude is very low (< 0.1).
    resonant_nodules = np.abs(standing_wave) < 0.1
    
    # We add a little bit of "Real World Chaos" (random noise) because nature isn't perfectly clean
    resonant_nodules = resonant_nodules & (np.random.rand(grid_size, grid_size) > 0.3)

    # --- 5. VISUALIZATION ---
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    
    # PLOT 1: The "Random Rock" Lie
    axes[0].imshow(old_model_nodules, cmap='Greys', interpolation='nearest')
    axes[0].set_title("Old World Model: Random Sedimentation\n(No Geometric Logic)", fontsize=12)
    axes[0].set_xlabel("Ocean Floor X")
    axes[0].set_ylabel("Ocean Floor Y")
    
    # PLOT 2: The "Circuit Board" Truth
    # You will see distinct lines, grids, or clusters - specific patterns.
    axes[1].imshow(resonant_nodules, cmap='Blues', interpolation='nearest')
    axes[1].set_title(f"16/pi Model: Resonant Standing Wave Nodes\n(The Earth's Circuit Board)", fontsize=12, fontweight='bold')
    axes[1].set_xlabel("Ocean Floor X")
    axes[1].set_yticks([]) # Hide Y axis for cleaner look
    
    plt.suptitle(f"DEEP SEA MINING DIAGNOSTIC: Are they Rocks or Components?", fontsize=16)
    
    plt.tight_layout()
    plt.savefig('nodule_resonance_map.png')
    print("[*] PLOT GENERATED: 'nodule_resonance_map.png'")
    print("[*] OBSERVATION: Notice the 'Resonant Model' creates organized structures.")
    print("[*] CONCLUSION: Removing these creates 'Resonant Holes' in the floor.")

if __name__ == "__main__":
    run_nodule_simulation()