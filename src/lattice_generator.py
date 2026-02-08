# -----------------------------------------------------------------------------
# HOLOGRAPHIC RESONANCE THEORY - LATTICE FREQUENCY GENERATOR
# Author: Timothy John Kish
# Repository: https://github.com/TimothyKish/Holographic-Resonance-The-Geometry-of-a-Quantized-Universe
# License: MIT License
#
# DESCRIPTION:
# Generates the predicted resonant nodes of the vacuum based on the
# Kish Geometric Constant (16/pi). These nodes correspond to observed
# anomalies in LIGO data (Ghost Notes) and the CMB.
#
# CITATIONS (Zenodo):
# Vol 1 (Geometry): https://doi.org/10.5281/zenodo.18209531
# Vol 2 (Dynamics): https://doi.org/10.5281/zenodo.18217120
# Vol 3 (Matter):   https://doi.org/10.5281/zenodo.18217227
# -----------------------------------------------------------------------------

import numpy as np
import math

# Simple prime generator for standalone use
def get_primes(n):
    primes = []
    candidate = 2
    while len(primes) < n:
        is_prime = True
        for p in primes:
            if p * p > candidate:
                break
            if candidate % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 1
    return primes

class KishResonator:
    def __init__(self):
        # 1. Define the Geometric Constants
        self.LATTICE_DIM = 16.0       # 4^2 (Max Degrees of Freedom)
        self.CYCLIC_PHASE = np.pi     # Time Loop Phase
        
        # 2. Derive the Kish Constant (The Gear Ratio)
        self.k_geo = self.LATTICE_DIM / self.CYCLIC_PHASE
        
        # 3. Define the Base Beat (Planck Scaling)
        # Scaled to macroscopic Hz for observability (from Vol 1, Table 4.1)
        self.base_beat = 3.53 # Hz
        
    def generate_spectrum(self, min_freq, max_freq):
        """
        Generates resonant nodes based on Prime-Log harmonics
        modulated by the Kish Ratio.
        """
        print(f"--- Generating Kish Spectra ({min_freq} - {max_freq} Hz) ---")
        print(f"Kish Constant (k): {self.k_geo:.6f}")
        
        # Get first 2000 primes
        primes = get_primes(2000)
        hits = []
        
        for p in primes:
            # The Harmonic Function: f = k * ln(p) * base_beat
            # This represents constructive interference nodes in the grid
            log_val = np.log(p)
            frequency = (self.k_geo * log_val) * self.base_beat
            
            # Check if within requested bandwidth
            if min_freq <= frequency <= max_freq:
                hits.append((p, frequency))
                
        return hits

# --- EXECUTION BLOCK ---
if __name__ == "__main__":
    # Initialize the Universe Lattice
    universe = KishResonator()
    
    # CASE 1: The "Ghost Note" Band (LIGO Data GW150914)
    # Searching for the anomalous peaks at 107 Hz and 127 Hz
    print("\n[LIGO BAND ANALYSIS - GW150914]")
    print(f"{'Prime Source':<15} | {'Frequency (Hz)':<15}")
    print("-" * 35)
    
    ligo_data = universe.generate_spectrum(100, 150)
    
    for p, freq in ligo_data:
        mark = ""
        if abs(freq - 107.0) < 1.0: mark = "<< MATCH (107 Hz)"
        if abs(freq - 127.0) < 1.0: mark = "<< MATCH (127 Hz)"
        print(f"{p:<15} | {freq:.4f} {mark}")

    # CASE 2: The Planck Pulse (Low Frequency)
    print("\n[FUNDAMENTAL RESONANCE]")
    base_data = universe.generate_spectrum(0, 10)
    for p, freq in base_data:
        print(f"Prime {p}: {freq:.4f} Hz")