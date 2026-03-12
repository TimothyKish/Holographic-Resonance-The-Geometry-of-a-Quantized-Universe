# B3.1 - THE SILENT LAKE DREDGER (AMINO ACID GEOMETRY)
# AUTHOR: Lyra Aurora Kish
# DATA SOURCE: NIH PubChem (SDF 3D Conformer)
# Source SDF https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/alanine/SDF?record_type=3d/
# Save SDF to B3_Alanine_5950.sd under Raw folder

import json
import os

def dredge_alanine_geometry(input_path):
    coordinates = []
    
    # Ensure the file exists before opening
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    with open(input_path, 'r') as f:
        lines = f.readlines()
        # The atoms block in V2000 starts at line 4 (index 3)
        # Alanine CID 5950 has exactly 13 atoms
        for i in range(3, 16): 
            parts = lines[i].split()
            # Safety check to ensure the line has coordinate data
            if len(parts) >= 4:
                x, y, z = float(parts[0]), float(parts[1]), float(parts[2])
                atom_type = parts[3]
                coordinates.append({"atom": atom_type, "x": x, "y": y, "z": z})
    
    # Save to Sovereign JSONL in the /Lake/ directory
    output_path = "../Lake/B3_alanine_lake.jsonl"
    with open(output_path, "w") as out:
        out.write(json.dumps({"cid": 5950, "name": "Alanine", "coords": coordinates}) + "\n")
    
    print(f"Sovereign Ingestion Complete: {output_path}")

# Execution Call
dredge_alanine_geometry("../Raw/B3_Alanine_5950.sd")