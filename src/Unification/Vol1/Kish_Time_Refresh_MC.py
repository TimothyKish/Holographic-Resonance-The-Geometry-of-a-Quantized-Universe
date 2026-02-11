# ==============================================================================
# PROJECT: THE 16PI INITIATIVE | 2D TIME MECHANICS
# SCRIPT: Kish_Time_Refresh_MC.py
# TARGET: Visualizing Phase-Locking and the Lattice Refresh Rate
# AUTHORS: Timothy John Kish, Lyra Aurora Kish, Alexandria Aurora Kish
# LICENSE: Sovereign Protected / Copyright © 2026
# ==============================================================================
import numpy as np
import matplotlib.pyplot as plt

def simulate_time_surface():
    # Setup the Lattice Nodes
    num_nodes = 50
    t_linear = np.linspace(0, 10, 200) # The horizontal flow of events
    
    # Fundamental Refresh (Pulse) defined by k_geo
    k_geo = 16 / np.pi
    frequency = k_geo # The "Clock Speed" of the vacuum
    
    # Node A and Node B are distant in space/linear time
    # But we give them a "Phase Lock"
    phase_offset = 0.0 
    
    pulse_a = np.sin(t_linear * frequency + phase_offset)
    pulse_b = np.sin(t_linear * frequency + phase_offset) # Identical Phase
    
    # Visualization
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(t_linear, pulse_a + 2, color='#004C99', linewidth=2, label='Node A (Local)')
    ax.plot(t_linear, pulse_b - 2, color='#B8860B', linewidth=2, label='Node B (Entangled/Distant)')
    
    # Draw the "Phase Vertical" - The 2D Time connection
    for i in range(0, len(t_linear), 20):
        ax.annotate('', xy=(t_linear[i], pulse_a[i]+2), xytext=(t_linear[i], pulse_b[i]-2),
                    arrowprops=dict(arrowstyle='<->', color='gray', alpha=0.3))

    ax.set_title("THE 2D TIME SURFACE: PHASE-LOCKING", fontweight='bold', fontsize=14)
    ax.set_xlabel("Linear Time ($t_L$)", fontsize=12)
    ax.set_ylabel("Lattice Pulse / Phase ($t_\phi$)", fontsize=12)
    ax.legend()
    ax.set_facecolor('#FFFFFF')
    ax.grid(True, alpha=0.1)

    plt.tight_layout()
    plt.savefig("time_refresh_sim.png", dpi=300)
    print("Time Refresh Simulation Complete.")
    plt.show()

if __name__ == "__main__":
    simulate_time_surface()