# B1_S2_Sovereign_Glycine_Inverter.py
# LADDER STEP: 2 - TARGETED SYMMETRY INVERSION (GLYCINE)

import json, os, requests

def invert_glycine_sovereign():
    raw_dir = "../Raw/"
    lake_dir = "../Lake/"
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(lake_dir, exist_ok=True)

    # 1. Pull Source Glycine (CID 750)
    api_name = "Glycine"
    cid = 750
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{api_name}/SDF?record_type=3d"
    
    print(f"[+] Fetching Source: {api_name} (CID {cid})...")
    r = requests.get(url)
    
    if r.status_code == 200:
        # Save original to Raw for the Audit Trail
        with open(f"{raw_dir}B1_S2_Source_Glycine_{cid}.sd", 'wb') as f:
            f.write(r.content)
        
        # 2. Perform Mathematical Mirroring (x = -x)
        lines = r.text.splitlines()
        num_atoms = int(lines[3][:3].strip())
        mirrored_coords = []
        
        for i in range(4, 4 + num_atoms):
            p = lines[i].split()
            mirrored_coords.append({
                "atom": p[3], 
                "x": -float(p[0]), # THE FLIP
                "y": float(p[1]), 
                "z": float(p[2])
            })
        
        # 3. Anchor to Lake as "D-Glycine (Simulated)"
        synthetic_entry = {
            "cid": f"{cid}_MIRROR",
            "name": "D_Glycine_Simulated",
            "metadata": "SIMULATED_HANDEDNESS_INVERSION",
            "coords": mirrored_coords
        }
        
        with open(f"{lake_dir}B1_S1_D_Glycine_lake.jsonl", "w") as out:
            out.write(json.dumps(synthetic_entry) + "\n")
        
        print(f"[!] Synthetic Mirror anchored to B1 Lake: D_Glycine_Simulated")
    else:
        print("Error: Could not retrieve source Glycine.")

if __name__ == "__main__":
    invert_glycine_sovereign()