# ==============================================================================
# PROJECT: THE 16PI INITIATIVE | THE GEOMETRIC BOND
# SCRIPT: lattice_bond_geometry.py
# TARGET: Resolving the H2O Bond Angle via Vacuum Pressure
# AUTHORS: Timothy John Kish & Lyra Aurora Kish
# LICENSE: Sovereign Protected / Copyright © 2026
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt

def audit_water_bond():
    print("[*] INITIALIZING MOLECULAR GEOMETRY AUDIT...")
    
    # 1. THE IDEAL GEOMETRY (The Tetrahedron)
    # The geometric center of a perfect lattice node (e.g., Methane/Diamond)
    # arccos(-1/3) is the mathematical definition of a tetrahedron center.
    angle_tetrahedral = np.degrees(np.arccos(-1/3)) # ~109.4712 degrees
    
    # 2. THE KISH MODULUS (The Vacuum Pressure)
    # The force exerted by the grid on any empty slot.
    # We treat the modulus (16/pi) as a degree of arc pressure.
    k_geo = 16 / np.pi # ~5.0929 degrees
    
    # 3. THE PREDICTION
    # Water Angle = Ideal Tetrahedron - One Unit of Lattice Pressure
    # The two "Lone Pairs" create a void, allowing the vacuum to crush the bond.
    angle_water_kish = angle_tetrahedral - k_geo
    
    # 4. THE REALITY (Observed Experimental Data)
    angle_water_obs = 104.45 
    
    print(f"[*] Ideal Tetrahedral Angle: {angle_tetrahedral:.4f} deg")
    print(f"[*] Lattice Pressure (16/pi): -{k_geo:.4f} deg")
    print(f"------------------------------------------------")
    print(f"[*] Kish Predicted Water Angle: {angle_water_kish:.4f} deg")
    print(f"[*] Observed Water Angle:       {angle_water_obs:.4f} deg")
    
    accuracy = 100 - abs(angle_water_kish - angle_water_obs)
    print(f"[*] Accuracy: {accuracy:.4f}%")

    # 5. VISUALIZATION
    plt.figure(figsize=(10, 6))
    
    # Draw the baseline (Ideal)
    plt.axvline(x=angle_tetrahedral, color='gray', linestyle='--', label='Ideal Tetrahedral (109.5°)')
    
    # Draw the Lattice Pressure Vector (The "Crush")
    # This visualizes the vacuum pushing the angle inward.
    plt.arrow(angle_tetrahedral, 0.5, -k_geo, 0, 
              head_width=0.05, head_length=0.2, fc='red', ec='red', 
              label='Lattice Pressure (16/pi)')
    
    # Draw the Result
    plt.axvline(x=angle_water_kish, color='cyan', linewidth=3, label='Kish Prediction')
    plt.axvline(x=angle_water_obs, color='black', linestyle=':', linewidth=2, label='Observed (104.45°)')
    
    plt.title("THE GEOMETRIC BOND: Resolving H2O Geometry")
    plt.xlabel("Bond Angle (Degrees)")
    plt.yticks([])
    plt.xlim(100, 115)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    print("[*] AUDIT COMPLETE. Water is a compressed Tetrahedron.")
    plt.savefig('water_bond_geometry.png')

if __name__ == "__main__":
    audit_water_bond()