# ==============================================================================
# SCRIPT NAME: sim_planck_pixel_burn_in.py
# PURPOSE: Interactive simulation of Lattice "Burn-In" vs "Infinite Refresh".
#          Demonstrates how the irrationality of Pi prevents the 16-degree-of-freedom
#          kinematic engine from repeating its path, ensuring every Planck coordinate
#          is visited without geometric burn-in. Rational approximations (22/7, 355/113)
#          force the universe into a closed, repeating glitch.
#
# COPYRIGHT: Copyright © 2026 Sovereign KishLattice 16pi Initiative
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Slider

# --- LATTICE CONSTANTS ---
TRUE_PI = np.pi
RATIO_22_7 = 22.0 / 7.0
RATIO_355_113 = 355.0 / 113.0
KINEMATIC_DOF = 16.0  # The 16 degrees of freedom

# --- TIME ARRAY ---
# Simulating a long runtime to show the "screen saver" history
time_units = np.linspace(0, 200, 30000)

def calculate_lattice_path(pi_approximation):
    """
    Calculates the 2D interference pattern of the 16-engine against the Pi ratio.
    """
    # X-axis represents the integer 16 degrees of freedom
    x_path = np.cos(KINEMATIC_DOF * time_units)
    
    # Y-axis represents the coupled ratio
    y_path = np.sin((KINEMATIC_DOF / pi_approximation) * time_units)
    
    return x_path, y_path

# --- SETUP VISUALIZATION ---
fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(left=0.3, bottom=0.2)

# Set dark background to simulate the "Screen Saver"
ax.set_facecolor('black')
fig.patch.set_facecolor('#1e1e1e')

# Initial plot (Starts with the 22/7 Burn-In Glitch)
current_ratio = RATIO_22_7
x_data, y_data = calculate_lattice_path(current_ratio)

# We use a low alpha (opacity) so "burn-in" appears as bright, heavy lines,
# while "infinite refresh" appears as a smooth, perfectly filled luminous cloud.
lattice_line, = ax.plot(x_data, y_data, color='#00c8ff', alpha=0.1, linewidth=1.5)

ax.set_title("Lattice Geometry: 22/7 Glitch (Burn-In)", fontsize=14, color='red', fontweight='bold')
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.set_xticks([]) # Hide axes for the screen saver look
ax.set_yticks([])

# --- ADD INTERACTIVE CONTROLS ---
ax_radio = plt.axes([0.05, 0.4, 0.2, 0.2], facecolor='lightgray')
radio = RadioButtons(ax_radio, ('22/7 (Low Res)', '355/113 (High Res)', 'True Pi (Irrational)'))

def update(label):
    if label == '22/7 (Low Res)':
        ratio = RATIO_22_7
        lattice_line.set_color('red')
        ax.set_title("Lattice Geometry: 22/7 Glitch (Burn-In)", color='red', fontweight='bold')
    elif label == '355/113 (High Res)':
        ratio = RATIO_355_113
        lattice_line.set_color('orange')
        ax.set_title("Lattice Geometry: 355/113 (Delayed Burn-In)", color='orange', fontweight='bold')
    else:
        ratio = TRUE_PI
        lattice_line.set_color('#00c8ff')
        ax.set_title("Lattice Geometry: True Pi (Infinite Refresh)", color='#00c8ff', fontweight='bold')
        
    x_new, y_new = calculate_lattice_path(ratio)
    lattice_line.set_data(x_new, y_new)
    fig.canvas.draw_idle()

radio.on_clicked(update)

# Add informative text
fig.text(0.5, 0.05, "Rational numbers force the 16-DOF phase space into a closed loop, overwriting Planck pixels.\nTrue Pi ensures the path never repeats, rendering a perfectly smooth, self-refreshing geometric vacuum.", 
         ha='center', color='white', fontsize=10, style='italic')

plt.show()