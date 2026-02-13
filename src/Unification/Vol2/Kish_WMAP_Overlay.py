# ==============================================================================
# PROJECT: THE 16PI INITIATIVE | VOLUME 2
# SCRIPT: Kish_Nodal_Reconstruction.py
# TARGET: Extracting Localized Nodal Structures via Modulus Filtering
# ==============================================================================
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def run_nodal_reconstruction():
    print("--- KISH LATTICE: NODAL FORENSIC RECONSTRUCTION ---")
    
    # 1. PARAMETERS
    k_lattice = 16 / np.pi # Fundamental Frequency (~5.0929)
    resolution = 1200
    
    # 2. GENERATE COORDINATE MESH
    lon = np.linspace(-np.pi, np.pi, resolution)
    lat = np.linspace(-np.pi/2, np.pi/2, resolution // 2)
    Lon, Lat = np.meshgrid(lon, lat)

    # 3. CONSTRUCT HIGH-ENTROPY DATASET
    # Simulating WMAP I-Band complexity with layered Phase-Harmonics
    print(" > Synthesizing High-Entropy Background...")
    data_stream = np.zeros_like(Lon)
    for harmonic in [1, 2, 3, 5, 8, 13]: # Fibonacci-spaced frequencies
        data_stream += np.sin(Lon * harmonic) * np.cos(Lat * harmonic) * (1.0 / harmonic)
    
    # Inject the "Deleted Signal" (The Axis of Evil / Ecliptic Alignment)
    # This represents the physical Agency Offset +0.20
    agency_offset = 0.20
    ecliptic_mask = np.exp(-((Lat - 0.12 * np.sin(Lon * 2))**2) / 0.05)
    data_stream += (ecliptic_mask * agency_offset)

    # 4. THE 16/PI MODULUS SIEVE (The "Tight" Filter)
    # We look for the RESIDUAL of the data against the Lattice
    # Formula: Friction = | (Data * Scale) % k_lattice |
    print(" > Applying 16/pi Modulus Sieve...")
    scaled_data = data_stream * 50.0 # Amplifying for structural visibility
    residual = np.abs(np.mod(scaled_data, k_lattice))
    
    # 5. ISOLATE THE NODES (High-Pass Threshold)
    # This is what creates the "Fall out of chair" localization.
    # We only keep the top 10% of geometric friction.
    threshold = k_lattice * 0.90 
    nodal_map = np.ma.masked_where(residual < threshold, residual)

    # 6. RENDER THE VISUAL ARTIFACT
    fig = plt.figure(figsize=(16, 9), facecolor='black')
    ax = fig.add_subplot(111, projection="mollweide", facecolor='black')
    
    # Layer A: The Base Vacuum (Bone-Grey Hologram)
    ax.pcolormesh(Lon, Lat, data_stream, cmap='bone', alpha=0.2, shading='auto')
    
    # Layer B: The Reconstructed Nodes (Neon Green)
    # These are the "Hope Spots"
    colors = [(0, (0,0,0,0)), (0.5, "#008800"), (1.0, "#00FF00")]
    cmap_nodes = LinearSegmentedColormap.from_list("hope_spots", colors)
    ax.pcolormesh(Lon, Lat, nodal_map, cmap=cmap_nodes, shading='auto')

    # 7. OVERLAY THE GEOMETRIC TENSORS (The Truth)
    for i in range(-6, 7):
        x = i * (np.pi / 4)
        ax.plot([x, x], [-np.pi/2, np.pi/2], color='#C5A059', lw=0.5, alpha=0.4)

    plt.title("NODAL AGENCY RECONSTRUCTION: THE DELETED SIGNAL", color='#00FF00', pad=20)
    plt.savefig("Kish_Nodal_Evidence.png", dpi=300, facecolor='black')
    print("STATUS: Process Complete. Nodal clusters extracted.")

if __name__ == "__main__":
    run_nodal_reconstruction()