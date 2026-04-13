# vol5/S-Series/S3_GalacticNASA/scripts/build_lake.py
import urllib.request
import urllib.parse
import json
import os
import time
import socket

socket.setdefaulttimeout(60)

# NASA/IPAC Extragalactic Database (NED) TAP Service
# Selecting galaxies with Measured Velocity Dispersion (sigma)
# We pull: Object Name, Velocity Dispersion, Redshift, and Magnitude
NED_TAP_URL = "https://ned.ipac.caltech.edu/tap/sync"

# SQL-like ADQL Query for NED
QUERY = """
SELECT TOP 5000 
    prename, velocity_dispersion, redshift, flux_out_mag
FROM ned_obj_spectral_data
WHERE velocity_dispersion IS NOT NULL 
    AND redshift > 0.001
    AND flux_out_mag IS NOT NULL
"""

RAW_LAKE = "../lake/s3_galactic_nasa_raw.jsonl"

def build_lake():
    print("===============================================================")
    print(" 🌌 INITIALIZING S3_GALACTIC (NASA/IPAC NED Ingestion)")
    print("===============================================================")
    
    params = {
        "request": "doQuery",
        "lang": "ADQL",
        "format": "json",
        "query": QUERY
    }
    
    encoded_params = urllib.parse.urlencode(params).encode('utf-8')
    
    try:
        print("[*] Contacting NASA/IPAC Extragalactic Database...")
        req = urllib.request.Request(NED_TAP_URL, data=encoded_params)
        
        with urllib.request.urlopen(req) as response:
            raw_response = response.read().decode('utf-8')
            data = json.loads(raw_response)
            
            # NED TAP JSON structure: data['data'] is the list of rows
            records = data.get('data', [])
            
            os.makedirs("../lake", exist_ok=True)
            records_count = 0
            
            with open(RAW_LAKE, 'w', encoding='utf-8') as out_f:
                for row in records:
                    # row index mapping based on SELECT: 
                    # 0: name, 1: sigma, 2: z, 3: mag
                    try:
                        entry = {
                            "entity_id": f"NED_{row[0]}",
                            "v_dispersion_kms": float(row[1]),
                            "magnitude_r": float(row[3]),
                            "z": float(row[2])
                        }
                        out_f.write(json.dumps(entry) + "\n")
                        records_count += 1
                    except:
                        continue
            
            print(f"[+] S3_Galactic NASA Lake built. {records_count} galaxies ingested.")
            print(f"[*] Audit Timestamp: {time.ctime()}")

    except Exception as e:
        print(f"[-] NASA NED Fetch Failed: {e}")
        print("[!] The galactic firewall is thick tonight.")

if __name__ == "__main__":
    build_lake()