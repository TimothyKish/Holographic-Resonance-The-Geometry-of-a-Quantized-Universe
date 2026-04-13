# ==============================================================================
# SCRIPT NAME: sim_frb_lattice_smear.py
# PURPOSE: Interactive simulation of FRB Lattice Slipstream and Dilation Smear.
#          Demonstrates how FRB signals start chaotic and phase-lock (smooth out) 
#          over vast distances in the 16/π lattice. Also shows how intervening mass 
#          and observer gravity (Earth) smear the packet via time dilation, 
#          requiring mathematical compensation to retrieve the original data.
#
# INTENDED USE: Run locally via Python. Use sliders to adjust distance, mass, 
#               gravity, and apply lattice compensation.
#
# COPYRIGHT: Copyright © 2026 Sovereign KishLattice 16pi Initiative
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# --- LATTICE CONSTANTS ---
PI = np.pi
K_GEO = 16.0 / PI
RESONANCE_DISTANCE_MPC = 500.0  # Distance required to fully "slipstream"

# --- TIME ARRAY (Milliseconds around the burst) ---
time_ms = np.linspace(-10, 20, 500)

def generate_original_packet():
    """The pure, unscattered burst directly at the source."""
    return np.exp(-(time_ms**2) / 2.0)  # Sharp Gaussian pulse

def calculate_received_signal(distance, mass_density, gravity, compensation):
    """
    Calculates the signal as seen by the telescope after lattice interactions.
    """
    original = generate_original_packet()
    
    # 1. THE SLIPSTREAM EFFECT (Distance)
    # Closer = scattered/noisy. Further = slipstreamed/smoothed by the lattice.
    slipstream_factor = np.clip(distance / RESONANCE_DISTANCE_MPC, 0.1, 1.0)
    noise_level = (1.0 - slipstream_factor) * 0.4
    chaos_noise = np.random.normal(0, noise_level, len(time_ms))
    
    # 2. THE SMEAR EFFECT (Mass & Gravity)
    # Mass and Earth Gravity cause time-dilation, stretching and smearing the packet.
    smear_width = 1.0 + (mass_density * 2.0) + (gravity * 1.5)
    
    # Apply smear (broaden the pulse and shift the tail slightly)
    smeared_pulse = np.exp(-((time_ms - (smear_width - 1.0))**2) / (2.0 * smear_width**2))
    
    # Combine effects
    degraded_signal = smeared_pulse + chaos_noise
    
    # 3. LATTICE COMPENSATION (De-smearing)
    # User applies math to reverse the smear and extract the original packet
    comp_factor = compensation / 100.0
    final_signal = (degraded_signal * (1.0 - comp_factor)) + (original * comp_factor)
    
    return final_signal

# --- SETUP VISUALIZATION ---
fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(left=0.1, bottom=0.45) # Make room for 4 sliders

initial_dist = 50.0   # Close (Scattered)
initial_mass = 0.5    # Moderate dust/plasma
initial_grav = 1.0    # Earth Gravity
initial_comp = 0.0    # No compensation

original_sig = generate_original_packet()
received_line, = ax.plot(time_ms, calculate_received_signal(initial_dist, initial_mass, initial_grav, initial_comp), 
                         'r-', linewidth=2, label="Received Signal")
original_line, = ax.plot(time_ms, original_sig, 'k:', linewidth=2, alpha=0.5, label="Original Packet Data")

ax.set_title("FRB Signal: Pre-Resonance Scattering & Gravity Smear", fontsize=14, color='#cc0000', fontweight='bold')
ax.set_xlabel("Time (ms)", fontsize=12)
ax.set_ylabel("Signal Amplitude", fontsize=12)
ax.set_xlim(-10, 20)
ax.set_ylim(-0.5, 1.5)
ax.legend(loc="upper right")
ax.grid(True, linestyle=':', alpha=0.6)

# --- ADD INTERACTIVE SLIDERS ---
ax_color = 'lightcyan'
ax_dist = plt.axes([0.15, 0.30, 0.75, 0.03], facecolor=ax_color)
ax_mass = plt.axes([0.15, 0.23, 0.75, 0.03], facecolor=ax_color)
ax_grav = plt.axes([0.15, 0.16, 0.75, 0.03], facecolor=ax_color)
ax_comp = plt.axes([0.15, 0.07, 0.75, 0.03], facecolor='lightgoldenrodyellow')

slider_dist = Slider(ax_dist, 'Distance (Mpc)', 10.0, 1000.0, valinit=initial_dist)
slider_mass = Slider(ax_mass, 'Intervening Mass', 0.0, 1.0, valinit=initial_mass)
slider_grav = Slider(ax_grav, 'Observer Gravity', 0.0, 1.0, valinit=initial_grav, valfmt='%0.2f (0=Space, 1=Earth)')
slider_comp = Slider(ax_comp, 'Apply Compensation %', 0.0, 100.0, valinit=initial_comp)

def update(val):
    d = slider_dist.val
    m = slider_mass.val
    g = slider_grav.val
    c = slider_comp.val
    
    received_line.set_ydata(calculate_received_signal(d, m, g, c))
    
    # Update Status Text
    if c > 90.0:
        ax.set_title("COMPENSATED: Original Packet Data Retrieved", color='green', fontweight='bold')
        received_line.set_color('green')
    elif d > RESONANCE_DISTANCE_MPC and m < 0.2 and g < 0.2:
        ax.set_title("LATTICE SLIPSTREAM: Signal is Phase-Locked and Smooth", color='#003278', fontweight='bold')
        received_line.set_color('blue')
    elif d < RESONANCE_DISTANCE_MPC:
        ax.set_title("FRB Signal: Pre-Resonance Scattering (Too Close to Source)", color='#cc0000', fontweight='bold')
        received_line.set_color('red')
    else:
        ax.set_title("FRB Signal: Time-Dilation Smear Detected", color='orange', fontweight='bold')
        received_line.set_color('orange')
        
    fig.canvas.draw_idle()

slider_dist.on_changed(update)
slider_mass.on_changed(update)
slider_grav.on_changed(update)
slider_comp.on_changed(update)

plt.show()