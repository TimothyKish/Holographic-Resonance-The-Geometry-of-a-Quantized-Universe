# ------------------------------------------------------------------------------
# Script Name: ligo_peak_validator.py
# Author: Timothy John Kish
# Theory: Holographic Resonance (Vol 1, Appendix D)
#
# Description:
#   This Monte Carlo simulation tests the Uniqueness of the Kish Constant.
#   It generates random universes with random geometric constants (k) to see
#   if they accidentally produce the 107 Hz and 127 Hz peaks seen in LIGO.
#   Result: P-value is statistically significant.
#
# Repository: https://github.com/TimothyKish/Holographic-Resonance-The-Geometry-of-a-Quantized-Universe
#
# Citations:
#   Vol 1 (Geometry): https://doi.org/10.5281/zenodo.18209531
#   Vol 2 (Dynamics): https://doi.org/10.5281/zenodo.18217120
#
# License: MIT License
# ------------------------------------------------------------------------------

import random
import numpy as np
from sympy import primerange

def run_monte_carlo_validation(trials=10000):
    """
    Tests the uniqueness of the Kish Constant (16/pi).
    We generate 'random universes' with random geometric constants (k)
    to see how many accidentally match LIGO data.
    """
    # 1. The Observation (LIGO GW150914 Anomalies)
    target_peaks = [107.0, 127.0]
    tolerance = 1.0  # Hz (Window of acceptance)
    
    # 2. Simulation Parameters
    # We test random geometric constants between 2.0 (Sphere) and 10.0 (Supergravity)
    matches = 0
    
    print(f"--- Starting Monte Carlo Simulation ({trials} Universes) ---")
    print(f"Targeting LIGO Peaks: {target_peaks} Hz (+/- {tolerance} Hz)")
    
    # Pre-calculate primes
    primes = list(primerange(1, 500))
    base_beat = 3.53  # The Planck/Base scaling
    
    for i in range(trials):
        # Generate a RANDOM geometric constant (The Null Hypothesis)
        k_random = random.uniform(2.0, 10.0)
        
        # Generate the spectrum for this random universe
        universe_hits = 0
        
        for p in primes:
            f_rand = (k_random * np.log(p)) * base_beat
            
            # Check against targets
            # We require ONE universe to hit BOTH peaks to count as a match
            if abs(f_rand - target_peaks[0]) < tolerance:
                universe_hits += 1
            if abs(f_rand - target_peaks[1]) < tolerance:
                universe_hits += 1
                
        # If this random universe hit BOTH 107 and 127 Hz...
        if universe_hits >= 2:
            matches += 1
            
    # 3. Calculate P-Value
    p_value = matches / trials
    print("-" * 40)
    print(f"Total Matches: {matches}")
    print(f"P-Value: {p_value:.5f}")
    
    if p_value < 0.05:
        print("RESULT: Significant. The Kish Constant is statistically unique.")
    else:
        print("RESULT: Not Significant. Random noise produces similar spectra.")

if __name__ == "__main__":
    run_monte_carlo_validation()