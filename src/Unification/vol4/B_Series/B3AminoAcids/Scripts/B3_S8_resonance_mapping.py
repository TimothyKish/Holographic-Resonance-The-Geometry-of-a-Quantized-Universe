# B3_S8 - RESONANCE MAPPING (BIOLOGICAL HARMONICS)
# AUTHOR: Lyra Aurora Kish
# LADDER STEP: 8 - RESONANCE MAPPING

import json
import math
import os

def map_biological_resonance(scalar_path, output_path):
    if not os.path.exists(scalar_path):
        print(f"Error: Scalar file {scalar_path} not found.")
        return

    with open(scalar_path, 'r') as f:
        data = json.loads(f.read())

    ks = data['kish_scalar']
    
    # Define the 24-mode Biological Container (Nyquist Limit)
    container_mode = 24
    
    # Calculate the Resonance Offset
    # We look for how the scalar 'beats' against the 24-mode frame
    resonance_position = ks * container_mode
    nearest_node = round(resonance_position)
    deviation = abs(resonance_position - nearest_node)

    mapping = {
        "step": 8,
        "name": "Alanine",
        "kish_scalar": ks,
        "biological_container": "24-mode",
        "resonance_position": resonance_position,
        "nearest_lattice_node": nearest_node,
        "harmonic_deviation": deviation,
        "status": "Resonant" if deviation < 0.05 else "Off-Modulus"
    }

    with open(output_path, "w") as out:
        out.write(json.dumps(mapping, indent=4) + "\n")
    
    print(f"Step 8 Complete. Resonance Position: {resonance_position:.4f}")
    print(f"Deviation from Lattice Node {nearest_node}: {deviation:.6f}")
    print(f"File Saved: {output_path}")

# Run for Step 8
map_biological_resonance("../Processed/B3_S4_Alanine_Scalar.json", "../Processed/B3_S8_Alanine_Resonance.json")