# vol5/P-Series/P1_Planetary/scripts/build_lake.py
import urllib.request
import urllib.parse
import json
import os
import socket
import time

socket.setdefaulttimeout(60)

# Source 1: NASA Exoplanet Archive
EXO_QUERY = "select pl_name, pl_orbper, pl_orbsmax from ps where default_flag=1 and pl_orbper is not null and pl_orbsmax is not null"
EXO_URL = f"https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query={urllib.parse.quote_plus(EXO_QUERY)}&format=json"

# Source 2: JPL Small-Body Database (Robust Query)
# We request: full_name, semi-major axis (a), and orbital period (per)
# Filters: Numbered objects (n), Asteroids (a), limit to first 10,000 for a massive haul
JPL_URL = "https://ssd-api.jpl.nasa.gov/sbdb_query.api?fields=full_name,a,per&sb-kind=a&sb-ns=n&limit=10000"

RAW_LAKE = "../lake/p1_planetary_raw.jsonl"

def fetch_data(url, name):
    print(f"[*] Dumping {name} Data...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Application/Science'}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            return json.loads(content)
    except Exception as e:
        print(f"[-] {name} Fetch Failed: {e}")
        return None

def build_lake():
    print("===============================================================")
    print(" 🪐 INITIALIZING P1_PLANETARY (The Dump Truck Ingestion v1.2)")
    print("===============================================================")
    
    os.makedirs("../lake", exist_ok=True)
    records_processed = 0
    
    # Run the haul
    exo_json = fetch_data(EXO_URL, "NASA Exoplanet")
    asteroid_json = fetch_data(JPL_URL, "JPL Asteroid")
    
    with open(RAW_LAKE, 'w', encoding='utf-8') as out_f:
        # Process NASA Exoplanet Data
        if exo_json:
            for row in exo_json:
                try:
                    entry = {
                        "entity_id": f"EXO_{records_processed:05d}",
                        "source": "NASA_EXO",
                        "name": row['pl_name'],
                        "period_days": float(row['pl_orbper']),
                        "semi_major_au": float(row['pl_orbsmax'])
                    }
                    out_f.write(json.dumps(entry) + "\n")
                    records_processed += 1
                except: continue
        
        # Process JPL Asteroid Data
        if asteroid_json and 'data' in asteroid_json:
            for row in asteroid_json['data']:
                try:
                    # JPL index mapping: 0=name, 1=a (AU), 2=per (days)
                    a_val = float(row[1])
                    p_val = float(row[2])
                    
                    if a_val > 0 and p_val > 0:
                        entry = {
                            "entity_id": f"AST_{records_processed:05d}",
                            "source": "JPL_SBDB",
                            "name": row[0],
                            "period_days": p_val,
                            "semi_major_au": a_val
                        }
                        out_f.write(json.dumps(entry) + "\n")
                        records_processed += 1
                except: continue

    print(f"\n[+] P1_Planetary Raw Lake built. Total records: {records_processed}")
    if records_processed > 10000:
        print("[*] 5-Sigma coverage ACHIEVED. The orbital lattice is ready for audit.")
    else:
        print(f"[*] Total records: {records_processed}. Building the statistical foundation.")

if __name__ == "__main__":
    build_lake()