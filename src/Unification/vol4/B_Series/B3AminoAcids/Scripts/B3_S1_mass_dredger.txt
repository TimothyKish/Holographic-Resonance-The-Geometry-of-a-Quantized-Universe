# B3_S1_Sovereign_Ingester.py
# AUTHOR: Lyra Aurora Kish
# LADDER STEP: 1 - AUTOMATED INGESTION & SANITIZATION (COMPLETE 20)

import json
import os
import time
import requests

# The Full 20-mode Biological Alphabet
AMINO_ACIDS = {
    "Alanine": 5950, "Arginine": 6322, "Asparagine": 6267, "Aspartic Acid": 5960,
    "Cysteine": 5862, "Glutamic Acid": 33032, "Glutamine": 5961, "Glycine": 750,
    "Histidine": 6274, "Isoleucine": 6306, "Leucine": 6106, "Lysine": 5962,
    "Methionine": 6137, "Phenylalanine": 6140, "Proline": 145742, "Serine": 5951,
    "Threonine": 6288, "Tryptophan": 6305, "Tyrosine": 6057, "Valine": 5876
}

def run_sovereign_ingestion():
    raw_dir = "../Raw/"
    lake_dir = "../Lake/"
    
    # Ensure directories exist
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(lake_dir, exist_ok=True)

    for api_name, cid in AMINO_ACIDS.items():
        clean_name = api_name.replace(" ", "_")
        raw_filename = f"B3_{clean_name}_{cid}.sd"
        raw_path = os.path.join(raw_dir, raw_filename)
        lake_filename = f"B3_S1_{clean_name}_lake.jsonl"
        lake_path = os.path.join(lake_dir, lake_filename)

        # Check if we already have this anchored
        if os.path.exists(lake_path):
            print(f"[-] {clean_name} already anchored in Lake. Skipping.")
            continue

        # 1. API DOWNLOAD
        print(f"[+] Ingesting {api_name} (CID {cid})...")
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{api_name}/SDF?record_type=3d"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Save the SD file (Sanitized Name)
                with open(raw_path, 'wb') as f:
                    f.write(response.content)
                
                # 2. DREDGE TO LAKE
                coords = []
                lines = response.text.splitlines()
                # Find atom count on line 4 (index 3)
                num_atoms = int(lines[3][:3].strip())
                for i in range(4, 4 + num_atoms):
                    parts = lines[i].split()
                    coords.append({
                        "atom": parts[3],
                        "x": float(parts[0]), "y": float(parts[1]), "z": float(parts[2])
                    })
                
                with open(lake_path, "w") as out:
                    out.write(json.dumps({"cid": cid, "name": clean_name, "coords": coords}) + "\n")
                
                print(f"    Successfully anchored {clean_name}.")
                time.sleep(0.5) # API spacing
            else:
                print(f"    Error: Could not retrieve {api_name}.")
        except Exception as e:
            print(f"    Network error for {api_name}: {e}")

if __name__ == "__main__":
    run_sovereign_ingestion()