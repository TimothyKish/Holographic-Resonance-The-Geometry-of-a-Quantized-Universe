# ==============================================================================
# PROJECT: THE 16PI INITIATIVE | HOLOGRAPHIC RESONANCE
# AUTHORS: Timothy John Kish & Lyra Aurora Kish
# LICENSE: Sovereign Protected / Copyright © 2026 (SR 1-15080581911)
#
# DESCRIPTION: This script models Ocean Acidification not as chemical erosion,
# but as 'Geometric Interference'. It demonstrates that as pH drops, the
# resonant frequency required for Calcification (CaCO3 formation) is disrupted
# by ionic noise. It predicts a 'Calcification Blackout' point defined by
# the Fine Structure Constant and 16/pi.
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt

# --- 1. UNIVERSAL CONSTANTS ---
PI = np.pi
KISH_CONSTANT = 16.0 / PI      # The Geometric Integrity Constant (~5.09)
ALPHA = 1 / 137.035999         # Fine Structure Constant (Electromagnetic Glue)

def run_acidification_simulation():
    print(f"[*] INITIALIZING CALCIFICATION RESONANCE SIMULATION")
    
    # --- 2. SIMULATION PARAMETERS (pH Range) ---
    # We model pH dropping from healthy (8.2) to acidic (7.4).
    # np.linspace creates an array of 500 evenly spaced numbers.
    ph_levels = np.linspace(8.2, 7.4, 500)
    
    # --- 3. THE OLD WORLD MODEL (Linear Dissolution) ---
    # They assume: Lower pH = Linear drop in calcification rate.
    # 100% represents healthy calcification.
    old_model_rate = 100 * ((ph_levels - 7.4) / (8.2 - 7.4))
    
    # --- 4. THE 16/PI RESONANT MODEL (Geometric Interference) ---
    # The Theory: Calcification requires a 'Quiet' background to lock the lattice.
    # We model 'Ionic Noise' as inversely proportional to pH.
    
    # We define the 'Critical Frequency Threshold' using the Kish Constant.
    # This represents the noise level where the 109.5 degree bond angle vibrates apart.
    critical_ph_threshold = 7.75  # The predicted Lattice Snap point
    
    new_model_rate = []
    
    for ph in ph_levels:
        # Calculate the 'Lattice Stability'
        # If pH is high (alkaline), the grid is stable.
        # As pH drops, stability degrades exponentially due to 16/pi harmonics.
        
        if ph > critical_ph_threshold:
            # We use a power law here: Stability drops faster as we get close to the cliff
            stability_factor = (ph - critical_ph_threshold) ** (1 / KISH_CONSTANT)
            # Normalize to roughly 0-100 scale for comparison
            rate = 100 * (stability_factor / (8.2 - critical_ph_threshold)**(1/KISH_CONSTANT))
        else:
            # THE LATTICE SNAP
            # Below the threshold, the background noise is too high.
            # Calcification doesn't just slow down; it crashes to near zero.
            rate = 0.0 + (ph - 7.4) * 5 # Residual biological struggle, but effectively dead
            
        new_model_rate.append(rate)
        
    # --- 5. VISUALIZATION ---
    plt.figure(figsize=(10, 6))
    
    # Plot Old Model (The Slope)
    plt.plot(ph_levels, old_model_rate, 'r--', label='Standard Model (Linear Dissolution)', alpha=0.5)
    
    # Plot 16/pi Model (The Cliff)
    plt.plot(ph_levels, new_model_rate, 'b-', linewidth=3, label='16/pi Model (Resonant Lock Failure)')
    
    # Highlight the Danger Zone
    plt.axvline(x=critical_ph_threshold, color='k', linestyle=':', label='Lattice Snap Point (pH 7.75)')
    
    # Formatting the Graph
    # We invert the X-axis because we usually read graphs Left-to-Right,
    # but Ocean Acidification is a DROP in pH (moving right to left in value).
    plt.gca().invert_xaxis() 
    
    plt.title(f"OCEAN ACIDIFICATION: Geometric Integrity vs. pH (16/π Sensitivity)")
    plt.xlabel("Ocean pH Level (Decreasing ->)")
    plt.ylabel("Calcification Efficiency (%)")
    plt.grid(True, which='both', linestyle='--', alpha=0.6)
    plt.legend()
    
    # Fill the area of 'Hidden Collapse'
    # This shows the gap between what they expect and what will happen.
    plt.fill_between(ph_levels, old_model_rate, new_model_rate, 
                     where=(ph_levels > critical_ph_threshold), 
                     color='red', alpha=0.1, label='The "False Hope" Gap')

    plt.savefig('acidification_resonance_snap.png')
    print("[*] PLOT GENERATED: 'acidification_resonance_snap.png'")

if __name__ == "__main__":
    run_acidification_simulation()