# vol5/T-Series/NT4_Cosmological/scripts/build_lake.py
import json
import urllib.request
import urllib.parse
import urllib.error
import time
import random
import os
import socket

# Set a global timeout for resilient fetching
socket.setdefaulttimeout(45)

# Sovereign Data Source: SDSS DR16 (Sloan Digital Sky Survey)
SQL_QUERY = "SELECT TOP 5000 z, ra, dec FROM SpecObj WHERE z > 0.01 AND z < 1 AND class='GALAXY'"
URL = f"http://skyserver.sdss.org/dr16/en/tools/search/x_sql.aspx?cmd={urllib.parse.quote(SQL_QUERY)}&format=json"

RAW_LAKE = "../lake/temporal_null_raw.jsonl"

def calculate_distance_proxy(z):
    """
    Computes a standard Hubble distance proxy (in Mpc).
    c = speed of light (km/s), H0 = Hubble constant (km/s/Mpc)
    """
    c = 299792.458
    H0 = 70.0
    return (c * z) / H0

def build_lake():
    print("[*] INITIALIZING N4_TEMPORAL (Empirical Scrambled Physics)")
    print("[*] Enforcing Sovereign Chain of Custody (SDSS DR16 API)...")
    
    # 1. Sovereign Download with Resilient Retry Logic
    print(f"[*] Executing SQL Query on Sloan Digital Sky Survey...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Application/Science',
        'Accept': 'application/json'
    }
    
    req = urllib.request.Request(URL, headers=headers)
    max_retries = 3
    sdss_data = None
    
    for attempt in range(max_retries):
        try:
            print(f"[*] Connection attempt {attempt + 1} of {max_retries}...")
            with urllib.request.urlopen(req, timeout=45) as response:
                raw_response = response.read().decode('utf-8')
                sdss_data = json.loads(raw_response)
            break 
            
        except Exception as e:
            print(f"[-] Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print("[*] Server lagging. Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print(f"[-] FATAL ERROR: SDSS API unreachable. Sovereign pipeline broken.")
                return

    print("[+] Sovereign download complete. Zero firewall interference.")
    
    # 2. Extract and Compute Authentic Values
    authentic_z = []
    authentic_d = []
    
    try:
        # NEW PARSING LOGIC: Handle the specific SDSS nested structure
        if isinstance(sdss_data, list) and len(sdss_data) > 0 and isinstance(sdss_data[0], dict) and "Rows" in sdss_data[0]:
            records = sdss_data[0]["Rows"]
        elif isinstance(sdss_data, dict) and "Rows" in sdss_data:
            records = sdss_data["Rows"]
        else:
            records = sdss_data 
            
        for row in records:
            z_val = float(row["z"])
            d_val = calculate_distance_proxy(z_val)
            authentic_z.append(z_val)
            authentic_d.append(d_val)
            
    except Exception as e:
        print(f"[-] Data Parsing Error. SDSS returned an unexpected JSON structure: {e}")
        print(str(sdss_data)[:200])
        return

    print(f"[*] Extracted {len(authentic_z)} authentic Cosmological z-d pairings.")
    
    # 3. SCRAMBLE THE PHYSICS (The Structural Null)
    print("[*] Scrambling distance metrics to destroy geometric resonance...")
    random.shuffle(authentic_d)
    
    # 4. Write to JSONL
    os.makedirs("../lake", exist_ok=True)
    with open(RAW_LAKE, 'w', encoding='utf-8') as out_f:
        for i in range(len(authentic_z)):
            entry = {
                "pair_id": i,
                "z_authentic": authentic_z[i],
                "d_proxy_scrambled": round(authentic_d[i], 4)
            }
            out_f.write(json.dumps(entry) + "\n")

    print(f"[*] N4_Temporal Raw Lake built successfully. Physics destroyed. Distributions perfectly preserved.")

if __name__ == "__main__":
    build_lake()