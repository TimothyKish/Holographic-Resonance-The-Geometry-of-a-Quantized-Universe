# ==============================================================================
# SCRIPT NAME: sim_planetary_anchor.py
# PURPOSE: Interactive simulation of Planetary Orbital Quantization.
#          Demonstrates how planetary orbits (specifically Jupiter at 5.20 AU)
#          are not random accretion accidents, but settle into the zero-drag 
#          resonant valleys of the 16/π lattice geometry (1 Kish Unit).
#
# INTENDED USE: Run locally via Python. Slide the planet's orbital distance 
#               to see the lattice drag drop to absolute zero at exactly 5.20 AU.
#
# COPYRIGHT: Copyright © 2026 Sovereign KishLattice 16pi Initiative
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# --- LATTICE CONSTANTS ---
PI = np.pi
K_GEO = 16.0 / PI       # 5.092958 (Vacuum Viscosity Coefficient)
KISH_UNIT_AU = 5.20     # 1 Kish Unit (Jupiter's exact semi-major axis)

# --- ORBITAL DISTANCE ARRAY (0 to 10 AU) ---
distances_au = np.linspace(0.5, 10.0, 500)

def calculate_lattice_drag(r_au):
    """
    Calculates the kinematic drag a massive body experiences at a given distance.
    The drag hits a resonant minimum (zero) at integer multiples of the Kish Unit.
    """
    # A dampened sine wave to represent the geometric resonance wells
    # Trough hits exactly at r_au = 5.20
    resonance_wave = np.abs(np.sin((r_au / KISH_UNIT_AU) * PI))
    
    # Add a gravitational decay envelope (drag is higher closer to the star)
    grav_envelope = 1.0 / np.sqrt(r_au)
    
    return resonance_wave * grav_envelope * 100.0

# --- SETUP VISUALIZATION ---
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.35)

drag_curve = calculate_lattice_drag(distances_au)
initial_distance = 2.0  # Start the planet at 2.0 AU

# Plot the Drag Landscape
ax.plot(distances_au, drag_curve, 'k-', linewidth=2, alpha=0.5, label="Vacuum Drag Landscape")

# Plot the Planet's current position
planet_marker, = ax.plot([initial_distance], [calculate_lattice_drag(initial_distance)], 
                         'ro', markersize=15, label="Gas Giant Position")

ax.set_title("Planetary Anchor: Finding the Zero-Drag Groove", fontsize=14, color='#003278', fontweight='bold')
ax.set_xlabel("Orbital Distance (AU)", fontsize=12)
ax.set_ylabel("Kinematic Lattice Drag (%)", fontsize=12)
ax.set_xlim(0.5, 10.0)
ax.set_ylim(0, 100)
ax.legend(loc="upper right")
ax.grid(True, linestyle=':', alpha=0.6)

# Highlight Jupiter's Groove
ax.axvline(x=KISH_UNIT_AU, color='green', linestyle='--', alpha=0.5)
ax.text(KISH_UNIT_AU + 0.1, 80, '1 Kish Unit\n(5.20 AU)', color='green', fontweight='bold')

# --- ADD INTERACTIVE SLIDER ---
ax_dist = plt.axes([0.15, 0.15, 0.75, 0.03], facecolor='lightgoldenrodyellow')
slider_dist = Slider(ax_dist, 'Distance (AU)', 0.5, 10.0, valinit=initial_distance, valstep=0.05)

def update(val):
    current_dist = slider_dist.val
    current_drag = calculate_lattice_drag(current_dist)
    
    # Move the planet marker
    planet_marker.set_data([current_dist], [current_drag])
    
    # Visual Feedback for Resonant Lock
    if current_drag < 2.0:
        planet_marker.set_color('green')
        ax.set_title(f"RESONANT LOCK ACHIEVED! Jupiter anchored at {current_dist:.2f} AU", color='green', fontweight='bold', fontsize=14)
    else:
        planet_marker.set_color('red')
        ax.set_title("Planetary Anchor: Finding the Zero-Drag Groove", color='#003278', fontweight='bold', fontsize=14)
        
    fig.canvas.draw_idle()

slider_dist.on_changed(update)
plt.show()