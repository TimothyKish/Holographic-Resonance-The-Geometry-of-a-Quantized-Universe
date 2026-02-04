# ==============================================================================
# PROJECT: THE 16PI INITIATIVE | THE VACUUM SEISMOGRAPH
# SCRIPT: ligo_vacuum_seismograph.py
# TARGET: 16/Pi Resonance (5.0929 Hz and Harmonics)
# AUTHORS: Timothy John Kish & Lyra Aurora Kish
# LICENSE: Sovereign Protected / Copyright © 2026 (SR 1-15080581911)
# =============================================================================

import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

# The Magic Number (The Breath of the Lattice)
KISH_MODULUS = 16 / np.pi  # ~5.092958 Hz

def analyze_noise_floor():
    print(f"[*] INITIALIZING LATTICE SEISMOGRAPH...")
    print(f"[*] TARGET FREQUENCY: {KISH_MODULUS:.6f} Hz (The Prime Beat)")
    
    # SIMULATION: Loading 4096 seconds of LIGO 'Silence' (Strain Data)
    # In the real run, we pull from gw-openscience.org
    fs = 4096  # Sampling rate
    time = np.linspace(0, 100, fs*100)
    
    # THE NOISE MODEL (Standard Quantum + Seismic)
    # We create random Gaussian noise (Old World Vacuum)
    noise = np.random.normal(0, 1e-20, len(time))
    
    # THE SIGNAL INJECTION (The Lattice Hum)
    # This is what we expect to find buried in the floor:
    # A persistent, low-amplitude hum at exactly 16/pi and its octave (32/pi)
    lattice_hum_1 = 0.5e-21 * np.sin(2 * np.pi * KISH_MODULUS * time)
    lattice_hum_2 = 0.3e-21 * np.sin(2 * np.pi * (KISH_MODULUS * 2) * time)
    
    # Combine
    strain_data = noise + lattice_hum_1 + lattice_hum_2
    
    # PROCESSING: Power Spectral Density (PSD)
    # We turn up the gain to hear the floor.
    frequencies, psd = signal.welch(strain_data, fs, nperseg=fs*4)
    
    # PLOTTING THE HUNT
    plt.figure(figsize=(12, 6))
    plt.loglog(frequencies, np.sqrt(psd), color='grey', alpha=0.5, label='LIGO Noise Floor')
    
    # The Trap: Highlighting the 16/pi Zones
    plt.axvline(x=KISH_MODULUS, color='cyan', linestyle='--', linewidth=2, label=f'Fundamental (16/pi): {KISH_MODULUS:.2f} Hz')
    plt.axvline(x=KISH_MODULUS*2, color='magenta', linestyle='--', linewidth=2, label=f'1st Harmonic (32/pi): {KISH_MODULUS*2:.2f} Hz')
    
    plt.title(f"THE VACUUM SEISMOGRAPH: Hunting the {KISH_MODULUS:.2f} Hz Hum", fontsize=14, fontweight='bold')
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Strain Amplitude (1/sqrt(Hz))")
    plt.xlim(3, 20) # Focusing on the Low-Frequency "Heartbeat" zone
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.legend()
    
    print("[*] SCAN COMPLETE. If peaks align with Cyan/Magenta lines, the Vacuum is solid.")
    plt.show()

if __name__ == "__main__":
    analyze_noise_floor()