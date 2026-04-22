# ==============================================================================
# SCRIPT NAME: sim_golden_damper_phi.py
# PURPOSE: Interactive simulation of Biological Load Balancing via Phi.
#          Demonstrates how the Golden Ratio (Phi) distributes structural load 
#          evenly across the 2D lattice, preventing "Lattice Snap". Rational 
#          fractions cause mass to stack on specific coordinates (structural collapse).
#
# COPYRIGHT: Copyright © 2026 Sovereign KishLattice 16pi Initiative
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
import math

# --- CONSTANTS ---
NODES = 1000 # Number of biological cells/seeds to pack

# Angles in radians
PHI = (1 + math.sqrt(5)) / 2
GOLDEN_ANGLE = 2 * math.pi * (1 - (1 / PHI)) # ~137.5 degrees
RATIONAL_ANGLE_8 = 2 * math.pi * (3 / 8)     # 135.0 degrees (Rational fraction)
NEAR_PHI_ANGLE = 2 * math.pi * (137.0 / 360) # 137.0 degrees (Close, but fails)

def calculate_growth_pattern(angle_step):
    """
    Calculates the radial distribution of nodes.
    Radius expands by sqrt(n) to maintain constant area per node.
    """
    radii = np.sqrt(np.arange(NODES))
    thetas = np.arange(NODES) * angle_step
    
    x = radii * np.cos(thetas)
    y = radii * np.sin(thetas)
    return x, y

# --- SETUP VISUALIZATION ---
fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(left=0.3, bottom=0.2)

ax.set_facecolor('#0a1118') # Deep lattice blue/black
fig.patch.set_facecolor('#1e1e1e')

# Initial plot (Starts with True Phi)
x_data, y_data = calculate_growth_pattern(GOLDEN_ANGLE)
scatter = ax.scatter(x_data, y_data, c=np.arange(NODES), cmap='YlOrBr', s=30, alpha=0.9, edgecolors='black', linewidth=0.5)

ax.set_title("True Phi: Perfect Load Balancing", fontsize=14, color='#00c8ff', fontweight='bold')
ax.set_xlim(-35, 35)
ax.set_ylim(-35, 35)
ax.set_xticks([])
ax.set_yticks([])

# --- INTERACTIVE CONTROLS ---
ax_radio = plt.axes([0.05, 0.4, 0.22, 0.2], facecolor='lightgray')
radio = RadioButtons(ax_radio, ('True Phi (137.5°)', 'Rational 3/8 (135°)', 'Near-Phi (137.0°)'))

def update(label):
    if label == 'Rational 3/8 (135°)':
        angle = RATIONAL_ANGLE_8
        ax.set_title("Rational 3/8: Structural Collapse\n(Mass stacks on 8 weak points)", color='#ff3333', fontweight='bold')
        scatter.set_cmap('Reds')
    elif label == 'Near-Phi (137.0°)':
        angle = NEAR_PHI_ANGLE
        ax.set_title("Near-Phi: Imbalanced Tension\n(Forms spiraling gaps, structural weakness)", color='#ffaa00', fontweight='bold')
        scatter.set_cmap('Wistia')
    else:
        angle = GOLDEN_ANGLE
        ax.set_title("True Phi: Perfect Load Balancing\n(Even distribution, no lattice overlap)", color='#00c8ff', fontweight='bold')
        scatter.set_cmap('YlOrBr')
        
    x_new, y_new = calculate_growth_pattern(angle)
    scatter.set_offsets(np.c_[x_new, y_new])
    fig.canvas.draw_idle()

radio.on_clicked(update)

fig.text(0.5, 0.05, "Rational angles cause biological mass to stack on identical lattice vectors, causing structural failure.\nPhi (the most irrational number) ensures every node has a unique vector, evenly damping the load.", 
         ha='center', color='white', fontsize=10, style='italic')

plt.show()