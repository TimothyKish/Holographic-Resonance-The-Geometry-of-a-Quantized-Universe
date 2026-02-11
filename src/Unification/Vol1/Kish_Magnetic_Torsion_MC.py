# ==============================================================================
# PROJECT: THE 16PI INITIATIVE | LATTICE TORSION
# SCRIPT: Kish_Magnetic_Torsion_MC.py
# TARGET: Visualizing Magnetism as Rotational Pressure in the Grid
# AUTHORS: Timothy John Kish, Lyra Aurora Kish, Alexandria Aurora Kish
# LICENSE: Sovereign Protected / Copyright © 2026
# ==============================================================================
import numpy as np
import matplotlib.pyplot as plt

def run_magnetic_sim():
    # Grid Setup
    grid_size = 30
    x = np.linspace(-10, 10, grid_size)
    y = np.linspace(-10, 10, grid_size)
    X, Y = np.meshgrid(x, y)

    # Fundamental Modulus (16/pi)
    k_geo = 16 / np.pi

    # Define two "Magnetic Poles" (Torsional Sources)
    pos_a = [-4, 0]
    pos_b = [4, 0]

    def get_torsion(pos, center, strength=1.0):
        dx = pos[0] - center[0]
        dy = pos[1] - center[1]
        r2 = dx**2 + dy**2 + 1e-9
        # Torsion is the "curl" of the displacement attenuated by k_geo
        tx = -strength * dy / (r2 * k_geo)
        ty =  strength * dx / (r2 * k_geo)
        return tx, ty

    # --- Scenario 1: Attraction (Opposite Spins Interlocking) ---
    U_attr, V_attr = np.zeros_like(X), np.zeros_like(Y)
    for i in range(grid_size):
        for j in range(grid_size):
            tx1, ty1 = get_torsion([X[i,j], Y[i,j]], pos_a, strength=5.0)
            tx2, ty2 = get_torsion([X[i,j], Y[i,j]], pos_b, strength=-5.0)
            U_attr[i,j], V_attr[i,j] = tx1 + tx2, ty1 + ty2

    # --- Scenario 2: Repulsion (Same Spins Grinding) ---
    U_rep, V_rep = np.zeros_like(X) , np.zeros_like(Y)
    for i in range(grid_size):
        for j in range(grid_size):
            tx1, ty1 = get_torsion([X[i,j], Y[i,j]], pos_a, strength=5.0)
            tx2, ty2 = get_torsion([X[i,j], Y[i,j]], pos_b, strength=5.0)
            U_rep[i,j], V_rep[i,j] = tx1 + tx2, ty1 + ty2

    # --- VISUALIZATION ---
    fig, axes = plt.subplots(1, 2, figsize=(15, 7))

    # Plot Attraction
    axes[0].streamplot(X, Y, U_attr, V_attr, color='#004C99', linewidth=1.5, density=1.2)
    axes[0].plot(pos_a[0], pos_a[1], 'go', markersize=10, label='Pole A (CW)')
    axes[0].plot(pos_b[0], pos_b[1], 'bo', markersize=10, label='Pole B (CCW)')
    axes[0].set_title("A. ATTRACTION\nLattice Gears Mesh", fontweight='bold')
    axes[0].legend()
    axes[0].set_facecolor('#F0F8FF')

    # Plot Repulsion
    axes[1].streamplot(X, Y, U_rep, V_rep, color='#8B0000', linewidth=1.5, density=1.2)
    axes[1].plot(pos_a[0], pos_a[1], 'go', markersize=10, label='Pole A (CW)')
    axes[1].plot(pos_b[0], pos_b[1], 'ro', markersize=10, label='Pole B (CW)')
    axes[1].set_title("B. REPULSION\nLattice Gears Clash", fontweight='bold')
    axes[1].legend()
    axes[1].set_facecolor('#FFF5EE')

    plt.tight_layout()
    plt.savefig("magnetic_torsion_visual.png", dpi=300)
    print("Simulation complete. Image saved as magnetic_torsion_visual.png")

if __name__ == "__main__":
    run_magnetic_sim()