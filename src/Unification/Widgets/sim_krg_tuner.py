# ==============================================================================
# SCRIPT NAME: sim_krg_tuner.py
# PURPOSE: Interactive simulation of the Kish Resonant Gyroscope (KRG).
#          Demonstrates that tapping into the vacuum requires BOTH frequency 
#          alignment (305.6 RPM) and phase-locking to the Universal Prime Clock 
#          (LIGO Stratum 0). Sweeping the frequency alone yields 0% coupling.
#
# INTENDED USE: Run locally via Python. Adjust both sliders to align the KRG 
#               rotor wave with the 16/π Prime Clock wave to achieve resonance.
#
# COPYRIGHT: Copyright © 2026 Sovereign KishLattice 16pi Initiative
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# --- LATTICE CONSTANTS ---
PI = np.pi
K_GEO_HZ = 16.0 / PI                 # 5.092958 Hz
TARGET_RPM = K_GEO_HZ * 60.0         # Approx 305.577 RPM

# --- TIME ARRAY ---
time = np.linspace(0, 1, 500) # 1 second window

def get_prime_clock_wave():
    """The absolute reference wave: Stratum 0 Universal Time."""
    return np.sin(2 * PI * K_GEO_HZ * time)

def get_krg_rotor_wave(rpm, phase_degrees):
    """The user's mechanical gyroscope wave."""
    freq_hz = rpm / 60.0
    phase_radians = phase_degrees * (PI / 180.0)
    return np.sin(2 * PI * freq_hz * time + phase_radians)

def calculate_coupling_strength(rpm, phase_degrees):
    """Calculates the resonant coupling % based on frequency and phase alignment."""
    # Frequency penalty (Gaussian drop-off)
    freq_diff = abs(rpm - TARGET_RPM)
    freq_factor = np.exp(-(freq_diff**2) / 5.0) 
    
    # Phase penalty (Cosine drop-off)
    phase_radians = phase_degrees * (PI / 180.0)
    phase_factor = (np.cos(phase_radians) + 1) / 2.0 
    
    # Total coupling is the product of both
    coupling = freq_factor * phase_factor * 100.0
    return coupling

# --- SETUP VISUALIZATION ---
fig, (ax_wave, ax_bar) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})
plt.subplots_adjust(bottom=0.35, hspace=0.4)

prime_wave = get_prime_clock_wave()
initial_rpm = 250.0
initial_phase = 90.0

# Wave Plot
ax_wave.plot(time, prime_wave, 'k--', linewidth=2, alpha=0.5, label="2 Zeta Prime Clock (Stratum 0)")
krg_line, = ax_wave.plot(time, get_krg_rotor_wave(initial_rpm, initial_phase), 'r-', linewidth=2.5, label="KRG Rotor Status")
ax_wave.set_title("KRG Alignment vs. Universal Prime Clock", fontsize=14, color='#003278', fontweight='bold')
ax_wave.set_xlabel("Time (seconds)")
ax_wave.set_ylabel("Amplitude")
ax_wave.set_ylim(-1.5, 1.5)
ax_wave.legend(loc="upper right")
ax_wave.grid(True, linestyle=':', alpha=0.6)

# Coupling Bar Chart
coupling_bar = ax_bar.barh(['Lattice Coupling'], [calculate_coupling_strength(initial_rpm, initial_phase)], color='red')
ax_bar.set_xlim(0, 100)
ax_bar.set_xlabel("Impedance Match / Resonant Coupling (%)", fontweight='bold')

# --- ADD INTERACTIVE SLIDERS ---
ax_rpm = plt.axes([0.15, 0.15, 0.75, 0.03], facecolor='lightgoldenrodyellow')
ax_phase = plt.axes([0.15, 0.10, 0.75, 0.03], facecolor='lightcyan')

slider_rpm = Slider(ax_rpm, 'Rotor (RPM)', 280.0, 330.0, valinit=initial_rpm, valstep=0.1)
slider_phase = Slider(ax_phase, 'Phase Offset (°)', -180.0, 180.0, valinit=initial_phase, valstep=1.0)

def update(val):
    current_rpm = slider_rpm.val
    current_phase = slider_phase.val
    
    # Update Waveform
    krg_line.set_ydata(get_krg_rotor_wave(current_rpm, current_phase))
    
    # Update Coupling Bar
    coupling = calculate_coupling_strength(current_rpm, current_phase)
    coupling_bar[0].set_width(coupling)
    
    # Visual Feedback for Phase-Lock
    if coupling > 95.0:
        krg_line.set_color('green')
        coupling_bar[0].set_color('green')
        ax_wave.set_title("STRATUM 0 PHASE-LOCK ACHIEVED!", color='green', fontweight='bold', fontsize=15)
    elif coupling > 50.0:
        krg_line.set_color('orange')
        coupling_bar[0].set_color('orange')
        ax_wave.set_title("Partial Harmonic Overlap - Adjust Phase", color='orange', fontweight='bold', fontsize=14)
    else:
        krg_line.set_color('red')
        coupling_bar[0].set_color('red')
        ax_wave.set_title("KRG Alignment vs. Universal Prime Clock", color='#003278', fontweight='bold', fontsize=14)
        
    fig.canvas.draw_idle()

slider_rpm.on_changed(update)
slider_phase.on_changed(update)

plt.show()