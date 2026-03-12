# B3.4 - THE SCALAR COMPUTATION (AMINO ACID GEOMETRY)
# AUTHOR: Lyra Aurora Kish
# LADDER STEP: 4 - SCALAR COMPUTATION

import json
import math
import os

def calculate_kish_scalar(lake_path, output_path):
    if not os.path.exists(lake_path):
        print(f"Error: Lake file {lake_path} not found.")
        return

    with open(lake_path, 'r') as f:
        data = json.loads(f.readline())

    coords = data['coords']
    
    # Identify critical nodes (Atom indices for N and C-alpha from our SDF)
    # In our alanine SDF: N is atom 3, C-alpha is atom 4
    n_atom = next(a for a in coords if a['atom'] == 'N')
    c_alpha = next(a for a in coords if a['atom'] == 'C') # Note: SDF order matters

    # Euclidean Distance Calculation
    dx = n_atom['x'] - c_alpha['x']
    dy = n_atom['y'] - c_alpha['y']
    dz = n_atom['z'] - c_alpha['z']
    
    distance = math.sqrt(dx**2 + dy**2 + dz**2)
    
    # 16/pi Projection (The Kish Scalar)
    k_modulus = 16 / math.pi
    kish_scalar = distance / k_modulus

    result = {
        "step": 4,
        "name": "Alanine",
        "distance_angstroms": distance,
        "kish_scalar": kish_scalar,
        "modulus_used": "16/pi"
    }

    with open(output_path, "w") as out:
        out.write(json.dumps(result, indent=4) + "\n")
    
    print(f"Step 4 Complete. Kish Scalar: {kish_scalar:.6f}")
    print(f"File Saved: {output_path}")

# Run for Step 4
calculate_kish_scalar("../Lake/B3_alanine_lake.jsonl", "../Processed/B3_S4_Alanine_Scalar.json")