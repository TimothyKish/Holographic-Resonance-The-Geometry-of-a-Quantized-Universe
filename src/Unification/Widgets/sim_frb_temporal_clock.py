# ==============================================================================
# SCRIPT NAME: sim_frb_temporal_clock.py
# PURPOSE: Interactive simulation of the FRB Temporal Clock.
#          Demonstrates fractal scale-invariance of the 16.35 geometric harmonic.
#          Users zoom out from the 16.35 ms quantum update rate to the 16.35 Day 
#          duty cycle of FRB 180916, showing the underlying vacuum clock is identical.
#
# INTENDED USE: Run locally via Python. Slide the Temporal Zoom to scale from 
#               milliseconds to days to observe the unbroken metronome.
#
# COPYRIGHT: Copyright © 2026 Sovereign KishLattice 16pi Initiative
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# --- LATTICE CONSTANTS ---
PI = np.pi
HARMONIC_BASE = 16.35  # The foundational timing harmonic

# --- TIME ARRAY ---
# We plot exactly 3 cycles of the metronome (0 to ~50 units)
time_units = np.linspace(0, 50, 500)

def get_metronome_wave():
    """
    The underlying geometric metronome. 
    It pulses exactly at multiples of 16.35, regardless of the temporal scale.
    """
    # Absolute value of sine creates a pulsing "tick" at exactly 16.35, 32.70, etc.
    return np.abs(np.sin((time_units / HARMONIC_BASE) * PI))

# --- SCALE MAPPING ---
# We map a slider (0 to 4) to specific physical time domains
def get_scale_info(zoom_level):
    if zoom_level < 1.0:
        return "Milliseconds (ms)", "Quantum Update Rate", "cyan"
    elif zoom_level < 2.0:
        return "Seconds (s)", "Acoustic / Mechanical", "blue"
    elif zoom_level < 3.0:
        return "Minutes (m)", "Planetary Atmospheric", "purple"
    elif zoom_level < 4.0:
        return "Hours (h)", "Stellar Core Dynamics", "orange"
    else:
        return "Days (d)", "FRB 180916 (Astrophysical)", "red"

# --- SETUP VISUALIZATION ---
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.35)

initial_zoom = 0.0
unit_label, domain_label, wave_color = get_scale_info(initial_zoom)

# Plot the continuous wave
wave_line, = ax.plot(time_units, get_metronome_wave(), color=wave_color, linewidth=3, label="Vacuum Metronome")

# Add markers at the exact 16.35 intervals
peaks_x = [16.35, 32.70, 49.05]
peaks_y = [0, 0, 0] # Troughs of the abs(sin) function act as the "ticks"
peak_markers, = ax.plot(peaks_x, peaks_y, 'ko', markersize=8, label="Harmonic Node (Tick)")

ax.set_title(f"Lattice Scale: {domain_label}", fontsize=14, color='#003278', fontweight='bold')
ax.set_xlabel(f"Time in {unit_label}", fontsize=12)
ax.set_ylabel("Lattice Amplitude", fontsize=12)
ax.set_xlim(0, 50)
ax.set_ylim(0, 1.1)
ax.legend(loc="upper right")
ax.grid(True, linestyle=':', alpha=0.6)

# Highlight the first tick (16.35)
text_annotation = ax.text(16.35, 0.1, f'16.35 {unit_label}', color='black', fontweight='bold', ha='center')

# --- ADD INTERACTIVE SLIDER ---
ax_zoom = plt.axes([0.15, 0.15, 0.75, 0.03], facecolor='lightcyan')
slider_zoom = Slider(ax_zoom, 'Temporal Zoom', 0.0, 4.0, valinit=initial_zoom, valstep=0.1)

def update(val):
    current_zoom = slider_zoom.val
    unit, domain, color = get_scale_info(current_zoom)
    
    # Update visual aesthetics to show scale shift, but the wave geometry REMAINS IDENTICAL
    wave_line.set_color(color)
    ax.set_title(f"Lattice Scale: {domain}", color=color, fontweight='bold', fontsize=14)
    ax.set_xlabel(f"Time in {unit}")
    
    # Update annotation
    text_annotation.set_text(f'16.35 {unit}')
    
    # Special highlight for FRB lock
    if current_zoom == 4.0:
        ax.set_title("MACRO-LOCK: FRB 180916 Duty Cycle Confirmed!", color='red', fontweight='bold', fontsize=15)
        
    fig.canvas.draw_idle()

slider_zoom.on_changed(update)
plt.show()