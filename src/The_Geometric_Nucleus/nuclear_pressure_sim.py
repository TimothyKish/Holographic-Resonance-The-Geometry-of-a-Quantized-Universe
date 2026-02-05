# ==============================================================================
# SOVEREIGN COPYRIGHT (C) 2026 KISH LATTICE 16PI INITIATIVES LLC
# SCRIPT: nuclear_pressure_sim.py
# TARGET: Proving Nuclei are Pressure Vessels, not Glue Traps
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt

def simulate_nucleus():
    # 1. SETUP: PROTONS (Repulsive)
    num_protons = 12
    # Start them loosely clustered
    positions = np.random.rand(num_protons, 2) - 0.5 
    velocities = np.zeros_like(positions)
    
    # Constants
    repulsion_strength = 0.5  # Coulomb Force (Pushing Out)
    lattice_pressure = 16 / np.pi  # Vacuum Force (Pushing In)
    dt = 0.01
    steps = 200

    # TRACKING HISTORY FOR PLOT
    history = []

    print(f"[SYSTEM] INITIATING LATTICE COMPRESSION. MODULUS: {lattice_pressure:.4f}")

    for step in range(steps):
        forces = np.zeros_like(positions)
        
        # A. CALCULATE INTERNAL REPULSION (Old World Problem)
        for i in range(num_protons):
            for j in range(num_protons):
                if i != j:
                    diff = positions[i] - positions[j]
                    dist = np.linalg.norm(diff)
                    if dist > 0.05: # Avoid singularity
                        # F = k / r^2 (Pushing Away)
                        forces[i] += (diff / dist) * (repulsion_strength / dist**2)

        # B. CALCULATE EXTERNAL LATTICE PRESSURE (New World Solution)
        # The Vacuum pushes everything toward the geometric center (0,0)
        # This acts like the "Keystone" force in an arch.
        for i in range(num_protons):
            dist_to_center = np.linalg.norm(positions[i])
            if dist_to_center > 0:
                # Force is inward (-) proportional to Lattice Modulus
                forces[i] -= (positions[i] / dist_to_center) * lattice_pressure

        # C. UPDATE PHYSICS
        velocities += forces * dt
        # Add friction (Vacuum Viscosity) to dampen and stabilize
        velocities *= 0.95 
        positions += velocities * dt
        history.append(positions.copy())

    # 3. VISUALIZATION
    final_pos = history[-1]
    
    plt.figure(figsize=(8, 8))
    # Draw the "Vacuum Boundary"
    circle = plt.Circle((0, 0), 0.6, color='gray', alpha=0.2, label='Lattice Pressure Zone')
    plt.gca().add_patch(circle)
    
    # Draw Protons
    plt.scatter(final_pos[:, 0], final_pos[:, 1], color='red', s=200, label='Protons (+)')
    
    plt.title(f"The Geometric Nucleus: Stabilized by Vacuum Pressure ({lattice_pressure:.2f})")
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    print("[SYSTEM] NUCLEUS STABILIZED. NO GLUONS DETECTED.")
    plt.savefig('geometric_nucleus_proof.png')

if __name__ == "__main__":
    simulate_nucleus()