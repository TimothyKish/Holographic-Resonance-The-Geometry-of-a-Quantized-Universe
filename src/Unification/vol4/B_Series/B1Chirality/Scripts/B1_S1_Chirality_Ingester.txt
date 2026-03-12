# B1_S1_Chirality_Ingester.py
# LADDER STEP: 1 - CHIRALITY LITMUS
# SOURCE: https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/[NAME]/SDF?record_type=3d

import json, os, time, requests

# Litmus test for D-Isomers
CHIRAL_TARGETS = {
    "D-Alanine": 71080, 
    "D-Valine": 71546, 
    "D-Serine": 71077
}

def ingest_mirror_alphabet():
    raw_dir = "../Raw/"
    lake_dir = "../Lake/"
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(lake_dir, exist_ok=True)
    
    for api_name, cid in CHIRAL_TARGETS.items():
        clean_name = api_name.replace("-", "_")
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{api_name}/SDF?record_type=3d"
        
        print(f"Ingesting Mirror: {api_name}...")
        try:
            r = requests.get(url)
            if r.status_code == 200:
                with open(f"{raw_dir}B1_{clean_name}_{cid}.sd", 'wb') as f:
                    f.write(r.content)
                
                # Immediate Dredge
                lines = r.text.splitlines()
                num_atoms = int(lines[3][:3].strip())
                coords = []
                for i in range(4, 4 + num_atoms):
                    p = lines[i].split()
                    coords.append({"atom": p[3], "x": float(p[0]), "y": float(p[1]), "z": float(p[2])})
                
                with open(f"{lake_dir}B1_S1_{clean_name}_lake.jsonl", "w") as out:
                    out.write(json.dumps({"cid": cid, "name": clean_name, "coords": coords}) + "\n")
                print(f"   Anchored {clean_name} to B1 Lake.")
                time.sleep(0.5)
        except Exception as e:
            print(f"   Failed {api_name}: {e}")

if __name__ == "__main__":
    ingest_mirror_alphabet()