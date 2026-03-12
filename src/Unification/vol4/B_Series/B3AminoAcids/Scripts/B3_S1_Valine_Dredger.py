# B3_S1_Valine_Dredger.py
# LADDER STEP: 1 - INGESTION
# Source https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/valine/SDF?record_type=3d save as Raw B3_Valine_5876.sd
import json
import os

def dredge_valine_geometry(input_path):
    coordinates = []
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    with open(input_path, 'r') as f:
        lines = f.readlines()
        # Valine CID 5876 has 16 atoms (V2000 block lines 4-19)
        for i in range(3, 19): 
            parts = lines[i].split()
            if len(parts) >= 4:
                x, y, z = float(parts[0]), float(parts[1]), float(parts[2])
                atom_type = parts[3]
                coordinates.append({"atom": atom_type, "x": x, "y": y, "z": z})
    
    output_path = "../Lake/B3_S1_Valine_5876.jsonl"
    with open(output_path, "w") as out:
        out.write(json.dumps({"cid": 5876, "name": "Valine", "coords": coordinates}) + "\n")
    
    print(f"Sovereign Ingestion Complete: {output_path}")

dredge_valine_geometry("../Raw/B3_Valine_5876.sd")