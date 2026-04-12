# ==============================================================================
# SCRIPT NAME: sim_water_gate.py
# PURPOSE: Interactive simulation of the H2O Water Gate (104.45° Antenna).
#          Demonstrates how the vacuum lattice compresses the standard tetrahedral 
#          angle (109.5°) down into a zero-tension resonant trough at exactly 104.45°, 
#          tuning the water molecule to act as a transducer for the 16/π lattice.
#
# INTENDED USE: Run locally via Python. Slide the bond angle to see the lattice 
#               tension drop to absolute zero at exactly 104.45°.
#
# COPYRIGHT: Copyright © 2026 Sovereign KishLattice 16pi Initiative
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# --- LATTICE & CHEMICAL CONSTANTS ---
PI = np.pi
K_GEO = 16.0 / PI                # 5.092958
TETRAHEDRAL_ANGLE = 109.5        # Standard uncompressed angle (degrees)
RESONANT_ANGLE = 104.45          # The Water Gate lattice lock (degrees)

# --- ANGLE ARRAY (90° to 120°) ---
angles_deg = np.linspace(90.0, 120.0, 500)

def calculate_lattice_tension(angle):
    """
    Calculates the geometric tension on the molecule.
    The tension is high at the standard tetrahedral angle, but the lattice 
    forces the geometry down into a resonant zero-tension trough at 104.45°.
    """
    # A parabolic well centered exactly on the resonant angle
    # We scale it so tension is visually clear (0 to 100 scale)
    deviation = np.abs(angle - RESONANT_ANGLE)
    tension = (deviation ** 2) * 4.0 
    
    # Cap at 100% for the visualization
    return np.clip(tension, 0, 100)

# --- SETUP VISUALIZATION ---
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.35)

tension_curve = calculate_lattice_tension(angles_deg)
initial_angle = TETRAHEDRAL_ANGLE  # Start at the standard uncompressed angle

# Plot the Tension Landscape
ax.plot(angles_deg, tension_curve, 'k-', linewidth=2, alpha=0.5, label="Vacuum Tension Landscape")

# Plot the Molecule's current state
molecule_marker, = ax.plot([initial_angle], [calculate_lattice_tension(initial_angle)], 
                           'ro', markersize=15, label="H2O Bond Angle")

ax.set_title("The Water Gate: Compressing the Antenna", fontsize=14, color='#003278', fontweight='bold')
ax.set_xlabel("H-O-H Bond Angle (Degrees)", fontsize=12)
ax.set_ylabel("Lattice Geometric Tension (%)", fontsize=12)
ax.set_xlim(90.0, 120.0)
ax.set_ylim(0, 100)
ax.legend(loc="upper right")
ax.grid(True, linestyle=':', alpha=0.6)

# Highlight the Standard Tetrahedral Angle (Old World)
ax.axvline(x=TETRAHEDRAL_ANGLE, color='red', linestyle='--', alpha=0.5)
ax.text(TETRAHEDRAL_ANGLE + 0.5, 80, 'Uncompressed\n(109.5°)', color='red', fontweight='bold')

# Highlight the Kish Lattice Resonance (The Water Gate)
ax.axvline(x=RESONANT_ANGLE, color='green', linestyle='--', alpha=0.5)
ax.text(RESONANT_ANGLE - 4.5, 20, 'Lattice Lock\n(104.45°)', color='green', fontweight='bold')

# --- ADD INTERACTIVE SLIDER ---
ax_angle = plt.axes([0.15, 0.15, 0.75, 0.03], facecolor='lightcyan')
slider_angle = Slider(ax_angle, 'Bond Angle (°)', 90.0, 120.0, valinit=initial_angle, valstep=0.05)

def update(val):
    current_angle = slider_angle.val
    current_tension = calculate_lattice_tension(current_angle)
    
    # Move the molecule marker
    molecule_marker.set_data([current_angle], [current_tension])
    
    # Visual Feedback for Resonant Lock
    if current_tension < 2.0:
        molecule_marker.set_color('green')
        ax.set_title(f"ANTENNA TUNED! Resonance locked at {current_angle:.2f}°", color='green', fontweight='bold', fontsize=14)
    else:
        molecule_marker.set_color('red')
        ax.set_title("The Water Gate: Compressing the Antenna", color='#003278', fontweight='bold', fontsize=14)
        
    fig.canvas.draw_idle()

slider_angle.on_changed(update)
plt.show()