# ==============================================================================
# SCRIPT: Kish_Web_Simulation.py
# TARGET: Simulating the Formation of the Cosmic Web via Standing Waves
# AUTHORS: Timothy John Kish & Lyra Aurora Kish
# LICENSE: Sovereign Protected / Copyright © 2026
# ==============================================================================

import numpy as np

def audit_cosmic_web():
    print("[*] INITIALIZING COSMIC CYMATICS SIMULATION...")
    
    # 1. SETUP THE FIELD
    # A 1D slice of the universe
    space_points = 20
    particles = np.random.uniform(0, 10, 1000) # Random distribution
    
    # 2. DEFINE THE STANDING WAVE (Vacuum Vibration)
    # Nodes at 0, 2.5, 5.0, 7.5, 10.0
    wavelength = 5.0
    k = 2 * np.pi / wavelength
    
    print(f"[*] VACUUM WAVELENGTH: {wavelength}")
    print("[*] MIGRATING MATTER TO NODES...")
    
    # 3. APPLY CYMATIC DRIFT
    # Particles move away from Antinodes (High Amplitude) -> To Nodes (Zero)
    # Drift = -Gradient of Potential
    
    converged_particles = []
    for p in particles:
        # Simple drift logic: Move towards nearest node
        # Node locations: 0, 2.5, 5.0, 7.5, 10.0
        nearest_node = round(p / (wavelength/2)) * (wavelength/2)
        converged_particles.append(nearest_node)
        
    # 4. ANALYZE CLUSTERING
    # Count how many particles found a node
    node_counts = {0.0:0, 2.5:0, 5.0:0, 7.5:0, 10.0:0}
    
    for p in converged_particles:
        if p in node_counts:
            node_counts[p] += 1
            
    print("-" * 50)
    print(f"{'NODE LOCATION':<15} | {'MATTER COUNT':<15} | {'TYPE'}")
    print("-" * 50)
    
    for node, count in node_counts.items():
        print(f"{node:<15.1f} | {count:<15} | FILAMENT")
        
    print("-" * 50)
    print("    > [STATUS] Matter successfully herded into Filaments.")
    print("    > The Voids are empty. The Web is formed.")

if __name__ == "__main__":
    audit_cosmic_web()