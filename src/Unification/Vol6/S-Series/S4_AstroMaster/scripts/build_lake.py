# vol5/S-Series/S4_AstroMaster/scripts/build_lake.py
import urllib.request
import os
import json
import time

# Sovereign Source: HyperLEDA (The Reliable Mirror)
# Parameters: vdis (Velocity Dispersion), itc (Corrected Mag), objname, z
URL = "http://leda.univ-lyon1.fr/f7.cgi?n=5000&c=o&p=vdis,itc,objname,z"

RAW_LAKE = "../lake/s4_galactic_master_raw.jsonl"

def build_lake():
    print("===============================================================")
    print(" 🌌 INITIALIZING S4_GALACTIC (HyperLEDA Master Ingestion)")
    print("===============================================================")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(URL, headers=headers)
    
    try:
        print("[*] Accessing Lyon-Meudon Galactic Mirror...")
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read().decode('utf-8')
            lines = content.strip().split('\n')
            
            os.makedirs("../lake", exist_ok=True)
            records_count = 0
            
            with open(RAW_LAKE, 'w', encoding='utf-8') as out_f:
                for line in lines:
                    if line.startswith('#') or not line.strip(): continue
                    
                    parts = line.split('|')
                    if len(parts) < 4: continue
                    
                    try:
                        # Indexing: 0:Name, 1:vdis, 2:mag, 3:z
                        v_disp = float(parts[1].strip())
                        mag = float(parts[2].strip())
                        
                        if v_disp > 40 and mag != 0: # Filtering for quality
                            entry = {
                                "entity_id": f"LEDA_{parts[0].strip()}",
                                "v_dispersion_kms": v_disp,
                                "magnitude_r": mag,
                                "z": float(parts[3].strip())
                            }
                            out_f.write(json.dumps(entry) + "\n")
                            records_count += 1
                    except: continue
            
            print(f"[+] S4_Galactic Master Lake built. {records_count} galaxies ingested.")
            
    except Exception as e:
        print(f"[-] HyperLEDA Bypass Failed: {e}")
        print("[!] All major observatories are dark. Proceeding to Local Calibration check.")

if __name__ == "__main__":
    build_lake()