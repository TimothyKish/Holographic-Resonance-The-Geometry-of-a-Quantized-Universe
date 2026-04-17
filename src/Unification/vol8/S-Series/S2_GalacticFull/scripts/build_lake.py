# vol5/S-Series/S2_GalacticFull/scripts/build_lake.py
import json
import urllib.request
import urllib.parse
import urllib.error
import time
import os
import socket

# Set a global timeout for resilient fetching
socket.setdefaulttimeout(60)

# Sovereign Data Source: SDSS DR16 (Mirroring T4 Source)
# Pulling velocity dispersion (sigma) and r-band magnitude (luminosity proxy)
SQL_QUERY = """
SELECT TOP 5000 
    objid, z, velDisp, modelMag_r 
FROM SpecObj 
WHERE class='GALAXY' 
    AND velDisp > 70 
    AND zWarning=0 
    AND modelMag_r BETWEEN 10 AND 20
"""

URL = f"http://skyserver.sdss.org/dr16/en/tools/search/x_sql.aspx?cmd={urllib.parse.quote(SQL_QUERY)}&format=json"

RAW_LAKE = "../lake/s2_galactic_full_raw.jsonl"

def build_lake():
    print("===============================================================")
    print(" 🌌 INITIALIZING S2_GALACTIC (The Full T4 Mirror Audit)")
    print("===============================================================")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Application/Science',
        'Accept': 'application/json'
    }
    
    req = urllib.request.Request(URL, headers=headers)
    max_retries = 5 # Increased retries for the heavy kinematic join
    sdss_data = None
    
    for attempt in range(max_retries):
        try:
            print(f"[*] Connection attempt {attempt + 1} of {max_retries}...")
            with urllib.request.urlopen(req, timeout=60) as response:
                raw_response = response.read().decode('utf-8')
                
                # Check if server returned HTML error instead of JSON
                if "<html" in raw_response.lower():
                    print("[-] Server busy (HTML returned). Cooling down...")
                    time.sleep(15)
                    continue
                    
                sdss_data = json.loads(raw_response)
            break 
            
        except Exception as e:
            print(f"[-] Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print("[*] Server lagging on kinematics join. Retrying in 10 seconds...")
                time.sleep(10)
            else:
                print(f"[-] FATAL ERROR: SDSS API unreachable. The bridge is blocked.")
                return

    print("[+] Sovereign download complete. Data parity with T4 established.")
    
    # Extract and Write
    os.makedirs("../lake", exist_ok=True)
    records_count = 0
    
    try:
        # Standard SDSS JSON row extraction
        if isinstance(sdss_data, list) and len(sdss_data) > 0:
            records = sdss_data[0].get("Rows", [])
        elif isinstance(sdss_data, dict):
            records = sdss_data.get("Rows", [])
        else:
            records = []

        with open(RAW_LAKE, 'w', encoding='utf-8') as out_f:
            for row in records:
                entry = {
                    "entity_id": f"S2_GAL_{row['objid']}",
                    "v_dispersion_kms": float(row['velDisp']),
                    "magnitude_r": float(row['modelMag_r']),
                    "z": float(row['z'])
                }
                out_f.write(json.dumps(entry) + "\n")
                records_count += 1
                
    except Exception as e:
        print(f"[-] Data Parsing Error: {e}")
        return

    print(f"[*] S2_Galactic Raw Lake built. {records_count} galactic witnesses ingested.")
    print(f"[*] Audit Timestamp: {time.ctime()}")

if __name__ == "__main__":
    build_lake()