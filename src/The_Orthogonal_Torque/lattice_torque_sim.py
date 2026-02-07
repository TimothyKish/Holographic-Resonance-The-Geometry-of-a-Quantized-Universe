# ==============================================================================
# SOVEREIGN COPYRIGHT (C) 2026 KISH LATTICE 16PI INITIATIVES LLC
# SCRIPT: lattice_torque_sim.py
# TARGET: Simulating Linear-to-Orthogonal Energy Conversion
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt

def simulate_lattice_torque():
    # 1. SETUP THE GRID
    x, y = np.meshgrid(np.arange(-5, 5, 1), np.arange(-5, 5, 1))
    u = np.zeros_like(x) 
    v = np.zeros_like(y) 

    # 2. APPLY THE LINEAR PUSH (Current Strength)
    current_strength = 10.0
    
    # 3. CALCULATE THE ORTHOGONAL TWIST
    # The Lattice twists to conserve angular momentum under stress.
    for i in range(len(x)):
        for j in range(len(y)):
            dist = np.sqrt(x[i,j]**2 + y[i,j]**2)
            if dist > 0:
                v[i,j] = (x[i,j] / dist) * current_strength * (16/np.pi)
                u[i,j] = -(y[i,j] / dist) * current_strength * (16/np.pi)

    # 4. VISUALIZE THE TORQUE
    plt.figure(figsize=(8, 8))
    plt.quiver(x, y, u, v, color='cyan', pivot='mid')
    plt.title(f"Lattice Torsion: Orthogonal Torque (Modulus 16/pi)")
    plt.grid(True, color='gray', alpha=0.3)
    
    print("[SYSTEM] TORQUE VECTOR FIELD GENERATED.")
    plt.savefig('lattice_torque_proof.png')

if __name__ == "__main__":
    simulate_lattice_torque()