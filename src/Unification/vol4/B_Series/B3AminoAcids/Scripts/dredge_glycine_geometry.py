# B3.2 - THE SILENT LAKE DREDGER (GLYCINE)
# AUTHOR: Lyra Aurora Kish
# LADDER STEP: 1 - INGESTION
# Source https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/glycine/SDF?record_type=3d rename as B3_Glycine_750.sd in raw folder.

import json
import os

def dredge_glycine_geometry(input_path):
    coordinates = []
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    with open(input_path, 'r') as f:
        lines = f.readlines()
        # Glycine CID 750 has 10 atoms (V2000 block lines 4-13)
        for i in range(3, 13): 
            parts = lines[i].split()
            if len(parts) >= 4:
                x, y, z = float(parts[0]), float(parts[1]), float(parts[2])
                atom_type = parts[3]
                coordinates.append({"atom": atom_type, "x": x, "y": y, "z": z})
    
    output_path = "../Lake/B3_S1_Glycine_750.jsonl"
    with open(output_path, "w") as out:
        out.write(json.dumps({"cid": 750, "name": "Glycine", "coords": coordinates}) + "\n")
    
    print(f"Sovereign Ingestion Complete: {output_path}")

dredge_glycine_geometry("../Raw/B3_Glycine_750.sd")