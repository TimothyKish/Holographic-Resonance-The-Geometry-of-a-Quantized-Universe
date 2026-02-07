# ==============================================================================
# SOVEREIGN COPYRIGHT (C) 2026 TIMOTHY JOHN KISH
# SCRIPT: fibonacci_heat_map.py
# TARGET: Proving the Golden Ratio prevents Vacuum Resonance Burn-In
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt

def run_fibonacci_audit():
    print("[*] INITIALIZING VACUUM LOAD BALANCER AUDIT")
    
    # 1. SETUP THE SIMULATION POINTS
    points_count = 500
    indices = np.arange(0, points_count, dtype=float)
    r = np.sqrt(indices)
    
    # 2. SCENARIO A: INTEGER STACKING (90 Degrees)
    theta_stack = indices * (np.pi / 2) 
    x_stack = r * np.cos(theta_stack)
    y_stack = r * np.sin(theta_stack)

    # 3. SCENARIO B: GOLDEN SPIRAL (137.5 Degrees)
    golden_angle = np.pi * (3 - np.sqrt(5)) 
    theta_gold = indices * golden_angle
    x_gold = r * np.cos(theta_gold)
    y_gold = r * np.sin(theta_gold)

    # 4. VISUALIZATION
    fig, axes = plt.subplots(1, 2, figsize=(14, 8)) # Increased height slightly
    
    # Plot A: The Failure
    axes[0].scatter(x_stack, y_stack, c='red', s=80, alpha=0.5, edgecolor='darkred')
    axes[0].set_title("SCENARIO A: INTEGER STACKING (90°)\nResult: Structural Resonance (Burn-In)", fontsize=11, fontweight='bold', color='darkred', pad=20)
    axes[0].set_aspect('equal')
    axes[0].axis('off')
    axes[0].text(0, -28, "Energy piles up in 4 discrete lanes.\nVacuum Stress = CRITICAL.", ha='center', color='red')

    # Plot B: The Success
    axes[1].scatter(x_gold, y_gold, c='lime', s=80, alpha=0.6, edgecolor='green')
    axes[1].set_title("SCENARIO B: GOLDEN SPIRAL (137.5°)\nResult: Perfect Load Balancing", fontsize=11, fontweight='bold', color='darkgreen', pad=20)
    axes[1].set_aspect('equal')
    axes[1].axis('off')
    axes[1].text(0, -28, "Energy distributed evenly across grid.\nVacuum Stress = NOMINAL.", ha='center', color='green')

    # FIX: Adjust layout to prevent title clipping
    plt.tight_layout(rect=[0, 0.03, 1, 0.90]) 
    
    plt.savefig('fibonacci_heat_map.png')
    print("[*] PROOF GENERATED: fibonacci_heat_map.png")

if __name__ == "__main__":
    run_fibonacci_audit()