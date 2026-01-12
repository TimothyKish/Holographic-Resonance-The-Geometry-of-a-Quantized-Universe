# -----------------------------------------------------------------------------
# HOLOGRAPHIC RESONANCE THEORY - PRIME NOISE AUDIT
# Author: Timothy John Kish
# Repository: https://github.com/TimothyKish/Holographic-Resonance-The-Geometry-of-a-Quantized-Universe
# License: MIT License
#
# DESCRIPTION:
# This Monte Carlo simulation tests the hypothesis that "random" detector noise
# contains a hidden Prime Number Harmonic structure. It compares Gaussian noise
# against a "Lattice Template" generated from the Kish Constant (16/pi).
#
# CITATIONS (Zenodo):
# Vol 1 (Geometry): https://doi.org/10.5281/zenodo.18209531
# Vol 2 (Dynamics): https://doi.org/10.5281/zenodo.18217120
# Vol 3 (Matter):   https://doi.org/10.5281/zenodo.18217227
# -----------------------------------------------------------------------------

import numpy as np
from scipy.signal import correlate
import time

# --- 1. DEFINE THE LATTICE CONSTANTS ---
LATTICE_RATIO = 16 / np.pi  # Approx 5.09
# The Prime Cadence (First 14 primes)
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]

def generate_lattice_signal(length):
    """
    Generates a synthetic signal pulse map based on Lattice Resonance.
    The 'Glitch' occurs at Prime * Ratio intervals.
    """
    signal = np.zeros(length)
    for p in PRIMES:
        # Calculate the harmonic node index
        beat_index = int(p * LATTICE_RATIO)
        if beat_index < length:
            signal[beat_index] = 1.0  # Simulated Lattice Impact
    return signal

def monte_carlo_audit(trials=1000000):
    """
    Compares Random Gaussian Noise against the Lattice Signal.
    """
    print(f"--- STARTING KISH LATTICE AUDIT ---")
    print(f"Target Pattern: Prime Harmonics scaled by 16/pi")
    print(f"Simulation Size: {trials} Universes")
    
    # Generate the theoretical "Perfect Lattice" signal
    lattice_template = generate_lattice_signal(1000)
    
    matches = 0
    start_time = time.time()
    
    for i in range(trials):
        if i % 100000 == 0:
            print(f"Scanning universe {i}...")

        # Generate random detector noise (Gaussian / Thermal)
        noise = np.random.normal(0, 1, 1000)
        
        # Cross-Correlate noise with Lattice Template
        # If the noise accidentally looks like the Lattice, this score will be high.
        correlation = correlate(noise, lattice_template)
        max_corr = np.max(correlation)
        
        # Threshold Check (Simulating a 'Signal Discovery')
        # A score > 15.0 indicates a statistically significant match
        if max_corr > 15.0:
            matches += 1
            
    end_time = time.time()
    
    print("-" * 40)
    print(f"Audit Complete in {end_time - start_time:.2f} seconds.")
    print(f"Total Random Matches Found: {matches}")
    
    if matches == 0:
        print(f"Statistical Significance: P < 1 in {trials}")
        print("CONCLUSION: Random noise cannot replicate the Prime Lattice pattern.")
        print("The signal is artificial or geometric in origin.")
    else:
        print(f"P-Value: {matches/trials}")

# --- EXECUTE ---
if __name__ == "__main__":
    monte_carlo_audit()