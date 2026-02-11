# ==============================================================================
# PROJECT: THE 16PI INITIATIVE | HARMONIC PRIMES
# SCRIPT: Kish_Prime_Resonance_Audit.py
# TARGET: Mapping Prime Nodes on the 2D Time Surface
# AUTHORS: Timothy John Kish, Lyra Aurora Kish, Alexandria Aurora Kish
# LICENSE: Sovereign Protected / Copyright © 2026
# ==============================================================================
import numpy as np
import matplotlib.pyplot as plt

def generate_prime_resonance():
    max_val = 50
    t_linear = np.linspace(1, max_val, 1000)
    t_phase = np.linspace(0, 2*np.pi, 200)
    
    # 1. THE LINEAR PULSE (Sum of Harmonics)
    resonance = np.zeros_like(t_linear)
    for n in range(2, 11): # Summing the first 10 frequencies
        resonance += np.cos(2 * np.pi * t_linear / n)
        
    # 2. THE 2D TIME SURFACE
    T_L, T_P = np.meshgrid(t_linear, t_phase)
    Z = np.sin(T_P) * (resonance / 10.0) 

    # 3. IDENTIFY PRIMES
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

    # --- VISUALIZATION ---
    fig, ax = plt.subplots(figsize=(12, 7))
    im = ax.imshow(Z, extent=[1, max_val, 0, 2*np.pi], origin='lower', aspect='auto', cmap='magma')
    
    for p in primes:
        ax.axvline(x=p, color='cyan', linestyle='--', alpha=0.4)
        ax.text(p, 2*np.pi + 0.1, str(p), ha='center', color='cyan', fontweight='bold')

    ax.set_title("THE 2D TIME SURFACE: PRIME RESONANCE NODES", fontweight='bold')
    ax.set_xlabel("Linear Time ($t_L$)")
    ax.set_ylabel("Phase Time ($t_\phi$)")
    plt.colorbar(im, label='Construction Intensity')
    plt.savefig("prime_resonance_2d.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    generate_prime_resonance()