# -----------------------------------------------------------------------------
# HOLOGRAPHIC RESONANCE THEORY - GALACTIC ROTATION VALIDATION
# Author: Timothy John Kish
# Repository: https://github.com/TimothyKish/Holographic-Resonance-The-Geometry-of-a-Quantized-Universe
# License: MIT License
#
# DESCRIPTION:
# The transmutation_calc.py script acts as the operational bridge between Kish theoretical geometry and practical 
# engineering, designed to calculate the precise Resonant Frequency required to reshape atomic nuclei. Its intent 
# is to translate the static Atomic Number of an element into a dynamic Hertz value (Sound/Vibration) using your 
# Vacuum Fundamental (16 divided by pi) and the Golden Ratio. By outputting these specific frequencies, the script 
# provides the essential "tuning targets" needed to guide a Null-Field reactor in shifting a heavy, unstable element 
# (like Lead) into a lighter, stable geometry (like Gold) through harmonic modulation rather than particle collision.
#
# CITATIONS (Zenodo):
# Vol 1 (Geometry): https://doi.org/10.5281/zenodo.18209531
# Vol 2 (Dynamics): https://doi.org/10.5281/zenodo.18217120
# Vol 3 (Matter):   https://doi.org/10.5281/zenodo.18217227
# -----------------------------------------------------------------------------
import math

def calculate_transmutation_frequency(atomic_number):
    """
    Calculates the resonant frequency required to transmute or interact with 
    a specific element based on the Kish Lattice Theory.
    
    Theory:
    - The Base Tension of the Vacuum is k = 16/pi.
    - Atomic stability is defined by the Golden Ratio (Phi) scaling of this tension.
    - Formula: f_target = f_vac * (Z ^ Phi)
    """
    
    # 1. Define the Constants
    PI = math.pi
    VACUUM_FUNDAMENTAL = 16 / PI  # The "Hum" of the Grid (~5.093 Hz)
    GOLDEN_RATIO = (1 + math.sqrt(5)) / 2  # The Scaling Factor (~1.618)
    
    # 2. Calculate the Frequency
    # The atomic number (Z) represents the node count.
    # We raise Z to the power of Phi to get the harmonic geometry.
    frequency_hz = VACUUM_FUNDAMENTAL * (atomic_number ** GOLDEN_RATIO)
    
    return frequency_hz, VACUUM_FUNDAMENTAL

def main():
    print("--- KISH LATTICE TRANSMUTATION CALCULATOR ---")
    print("Enter the Atomic Number (Z) of the element you wish to target.")
    print("Example: 79 for Gold, 82 for Lead.")
    
    while True:
        try:
            user_input = input("\nEnter Atomic Number (or 'q' to quit): ")
            if user_input.lower() == 'q':
                break
            
            z = int(user_input)
            if z <= 0:
                print("Atomic number must be a positive integer.")
                continue
                
            freq, base = calculate_transmutation_frequency(z)
            
            print(f"\nTarget Element: Z = {z}")
            print(f"Base Vacuum Tension: {base:.4f} Hz")
            print(f"REQUIRED RESONANCE:  {freq:.4f} Hz")
            print("------------------------------------------------")
            print(f"INSTRUCTION: Pulse this frequency into the Null-Field")
            print(f"to induce geometric plasticity in the nucleus.")
            
        except ValueError:
            print("Please enter a valid integer.")

if __name__ == "__main__":
    main()