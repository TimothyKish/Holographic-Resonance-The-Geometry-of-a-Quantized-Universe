# ==============================================================================
# SCRIPT NAME: sim_grays_paradox.py
# PURPOSE: Interactive simulation resolving Gray's Paradox using Kish Lattice Mechanics.
#          Demonstrates how physical body length phase-locking to the 16/π 
#          water grain exponentially reduces hydrodynamic drag.
# 
# INTENDED USE: Run locally via Python to visualize the lattice slipstream effect.
#               Requires 'numpy' and 'matplotlib'.
#
# COPYRIGHT: Copyright © 2026 Sovereign KishLattice 16pi Initiative
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# --- LATTICE CONSTANTS ---
PI = np.pi
K_GEO = 16.0 / PI  # The Kinematic Primary Modulus (approx 5.092958)
WATER_DENSITY = 1026  # kg/m^3 for seawater

def calculate_standard_drag(length, velocities):
    """
    Calculates the classical fluid dynamics drag (The Paradox).
    In the Old World model, power required scales with the cube of velocity 
    and the wetted surface area (approximated here by length).
    """
    # Simplified drag equation: D = 0.5 * rho * v^2 * Cd * A
    # We use a nominal drag coefficient and assume Area scales with length
    drag_coefficient = 0.004
    area_approx = length * 0.2 
    return 0.5 * WATER_DENSITY * (velocities**2) * area_approx * drag_coefficient

def calculate_lattice_slipstream(length, velocities):
    """
    Calculates the Kish Lattice Phase-Locked Drag (The Resolution).
    If the organism's length is a harmonic of the 16/π water grain, 
    the lattice tension drops, creating a resonant slipstream.
    """
    base_drag = calculate_standard_drag(length, velocities)
    
    # Calculate resonance: Approaches 0 when length is a multiple of K_GEO
    # We use a sine wave envelope to represent the geometric node spacing
    harmonic_resonance = np.abs(np.sin((length / K_GEO) * PI))
    
    # The slipstream engages: at perfect resonance (harmonic_resonance = 0), 
    # drag drops to 10% of standard (the 0.1 baseline friction).
    slipstream_multiplier = 0.1 + (0.9 * harmonic_resonance)
    
    return base_drag * slipstream_multiplier

# --- SETUP VISUALIZATION ---
# Initialize the figure and axis
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.35) # Make room for the slider

# Define the velocity range (1 to 15 m/s)
velocities = np.linspace(1, 15, 100)
initial_length = 2.5 # Starting length in meters

# Plot the initial curves
standard_line, = ax.plot(velocities, calculate_standard_drag(initial_length, velocities), 
                         'r--', linewidth=2, label="Old World Drag (Muscle Deficit)")
lattice_line, = ax.plot(velocities, calculate_lattice_slipstream(initial_length, velocities), 
                        'b-', linewidth=3, label="Lattice Slipstream (Actual Power)")

# Format the plot
ax.set_title("Gray's Paradox: Marine Locomotion vs. The 16/π Water Grain", fontsize=14, fontweight='bold', color='#003278')
ax.set_xlabel("Swimming Velocity (m/s)", fontsize=12)
ax.set_ylabel("Resistance / Power Required", fontsize=12)
ax.legend(loc="upper left")
ax.grid(True, linestyle=':', alpha=0.6)

# --- ADD INTERACTIVE SLIDER ---
# Create an axis for the slider
ax_length = plt.axes([0.2, 0.15, 0.65, 0.03], facecolor='lightgoldenrodyellow')
# Initialize the slider (Length from 1m to 12m)
slider_length = Slider(ax_length, 'Body Length (m)', 1.0, 12.0, valinit=initial_length, valstep=0.1)

# Function to run when the slider changes
def update(val):
    current_length = slider_length.val
    
    # Update the y-data of both curves
    standard_line.set_ydata(calculate_standard_drag(current_length, velocities))
    lattice_line.set_ydata(calculate_lattice_slipstream(current_length, velocities))
    
    # Dynamically adjust the y-axis limit based on max drag
    ax.set_ylim(0, max(calculate_standard_drag(current_length, velocities)) * 1.1)
    
    # Check for Phase-Lock (Is length a multiple of 16/pi?)
    resonance_check = np.abs(np.sin((current_length / K_GEO) * PI))
    if resonance_check < 0.05:
        ax.set_title(f"PHASE LOCK ACHIEVED! {current_length:.1f}m resonates with 16/π", color='green', fontweight='bold', fontsize=14)
        lattice_line.set_color('green')
    else:
        ax.set_title("Gray's Paradox: Marine Locomotion vs. The 16/π Water Grain", color='#003278', fontweight='bold', fontsize=14)
        lattice_line.set_color('blue')
        
    fig.canvas.draw_idle()

# Attach the update function to the slider
slider_length.on_changed(update)

# Render the application
plt.show()