"""
------------------------------------------------------------------------------
THE GEOMETRIC ARCHITECTURE OF MATTER: MONTE CARLO VERIFICATION SCRIPT
------------------------------------------------------------------------------
Author:    Timothy John Kish
Copyright: (c) 2026 Timothy John Kish
License:   Creative Commons Attribution 4.0 International (CC BY 4.0)
Version:   1.0 (The "Silent Sea" Release)

DIGITAL REPOSITORY:
https://github.com/TimothyKish/Holographic-Resonance-The-Geometry-of-a-Quantized-Universe

RELATED DOIs:
- Vol 1 (Derivation): https://doi.org/10.5281/zenodo.18209530
- Vol 2 (Noise):      https://doi.org/10.5281/zenodo.18217119
- Vol 3 (Atomic):     https://doi.org/10.5281/zenodo.18217226
- Rosetta Stone:      https://doi.org/10.5281/zenodo.18235735

DESCRIPTION:
This script performs a Monte Carlo simulation to test the statistical probability
of "Lattice Resonance" (16/pi harmonics) occurring in random Gaussian noise.
It compares a synthetic "Prime-Lattice Template" against 1,000,000 random
noise floors to validate the "Signal vs. Noise" hypothesis presented in Volume 2.
------------------------------------------------------------------------------
"""

import numpy as np
from scipy.signal import correlate

# --- CONSTANTS: THE KISH GEOMETRY ---
LATTICE_RATIO = 16 / np.pi  # Approx 5.0929
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]

def generate_lattice_signal(length):
    """
    Generates a synthetic signal map based on Lattice Resonance.
    The 'Glitch' occurs at Prime * Ratio intervals.
    """
    signal = np.zeros(length)
    for p in PRIMES:
        # The Beat Location: Prime Number x Lattice Stiffness
        beat_index = int(p * LATTICE_RATIO)
        if beat_index < length:
            signal[beat_index] = 1.0  # Simulated Lattice Impact
    return signal

def monte_carlo_audit(trials=1000000):
    """
    Compares Random Gaussian Noise against the Lattice Signal.
    """
    print(f"--- INITIATING KISH LATTICE AUDIT ---")
    print(f"Target Ratio: 16/pi ({LATTICE_RATIO:.4f})")
    print(f"Running {trials} Monte Carlo simulations...")
    
    # 1. Create the 'Perfect' Lattice Template (The Signal we are looking for)
    lattice_template = generate_lattice_signal(1000)
    matches = 0
    
    for i in range(trials):
        # 2. Generate random detector noise (Standard Gaussian Distribution)
        # This simulates the "Background Noise" of the universe/detector.
        noise = np.random.normal(0, 1, 1000)
        
        # 3. Cross-Correlate noise with Lattice Template
        # This checks: "Does this random noise accidentally look like the Lattice?"
        correlation = correlate(noise, lattice_template)
        max_corr = np.max(correlation)
        
        # 4. Threshold Check (Simulating a 'Signal Discovery')
        # A correlation > 15.0 would indicate a false positive strong enough to trick a human.
        if max_corr > 15.0:
            matches += 1
            
        # Optional: Progress ticker every 100k trials
        if i % 100000 == 0 and i > 0:
            print(f"  ... {i} trials complete. Matches so far: {matches}")
            
    print(f"\n--- RESULTS ---")
    print(f"Total Trials: {trials}")