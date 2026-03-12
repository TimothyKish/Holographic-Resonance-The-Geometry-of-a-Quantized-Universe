# B1_S1_Full_Mirror_Ingester.py
# LADDER STEP: 1 - FULL MIRROR INGESTION & SANITIZATION

import json, os, time, requests

# The Chiral Mirror Set
MIRROR_AMINO_ACIDS = {
    "D-Alanine": 71080, "D-Arginine": 71591, "D-Asparagine": 71107, 
    "D-Aspartic Acid": 71081, "D-Cysteine": 71098, "D-Glutamic Acid": 71082, 
    "D-Glutamine": 71110, "D-Histidine": 71113, "D-Isoleucine": 71548, 
    "D-Leucine": 71101, "D-Lysine": 71114, "D-Methionine": 71102, 
    "D-Phenylalanine": 71103, "D-Proline": 71481, "D-Serine": 71077, 
    "D-Threonine": 71087, "D-Tryptophan": 71105, "D-Tyrosine": 71106, 
    "D-Valine": 71546
}

def ingest_full_mirror():
    raw_dir = "../Raw/"
    lake_dir = "../Lake/"
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(lake_dir, exist_ok=True)

    for api_name, cid in MIRROR_AMINO_ACIDS.items():
        # Sanitize for local storage: D-Aspartic Acid -> D_Aspartic_Acid
        clean_name = api_name.replace(" ", "_").replace("-", "_")
        lake_path = os.path.join(lake_dir, f"B1_S1_{clean_name}_lake.jsonl")
        
        if os.path.exists(lake_path):
            print(f"[-] {clean_name} already in Lake. Skipping.")
            continue

        # API Call needs the space (encoded as %20 by requests)
        print(f"[+] Ingesting Mirror: {api_name} (CID {cid})...")
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{api_name}/SDF?record_type=3d"
        
        try:
            r = requests.get(url)
            if r.status_code == 200:
                # Save Raw SD with underscores
                raw_filename = f"B1_{clean_name}_{cid}.sd"
                with open(os.path.join(raw_dir, raw_filename), 'wb') as f:
                    f.write(r.content)
                
                # Immediate Dredge to Lake
                lines = r.text.splitlines()
                num_atoms = int(lines[3][:3].strip())
                coords = []
                for i in range(4, 4 + num_atoms):
                    p = lines[i].split()
                    coords.append({"atom": p[3], "x": float(p[0]), "y": float(p[1]), "z": float(p[2])})
                
                with open(lake_path, "w") as out:
                    out.write(json.dumps({"cid": cid, "name": clean_name, "coords": coords}) + "\n")
                
                print(f"    Successfully anchored {clean_name}.")
                time.sleep(0.5)
            else:
                print(f"    Error: Could not retrieve {api_name}. Check API naming.")
        except Exception as e:
            print(f"    Network error for {api_name}: {e}")

if __name__ == "__main__":
    ingest_full_mirror()