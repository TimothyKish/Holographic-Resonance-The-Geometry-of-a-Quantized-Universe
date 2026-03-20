# vol5/P-Series/P1_2_Normalized/scripts/build_lake.py
import urllib.request
import urllib.parse
import json
import os
import socket
import time

socket.setdefaulttimeout(60)

EXO_QUERY = "select pl_name, pl_orbper, pl_orbsmax from ps where default_flag=1 and pl_orbper is not null and pl_orbsmax is not null"
EXO_URL = f"https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query={urllib.parse.quote_plus(EXO_QUERY)}&format=json"
JPL_URL = "https://ssd-api.jpl.nasa.gov/sbdb_query.api?fields=full_name,a,per&sb-kind=a&sb-ns=n&limit=10000"

RAW_LAKE = "../lake/p1_2_normalized_raw.jsonl"

def fetch_data(url, name):
    print(f"[*] Auditing {name} Source...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Application/Science'}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"[-] {name} Audit Failed: {e}")
        return None

def build_lake():
    print("===============================================================")
    print(" 🪐 INITIALIZING P1_2 (Normalized Audit Chain of Custody)")
    print("===============================================================")
    os.makedirs("../lake", exist_ok=True)
    records_processed = 0
    
    exo_json = fetch_data(EXO_URL, "NASA Exoplanet")
    asteroid_json = fetch_data(JPL_URL, "JPL Asteroid")
    
    with open(RAW_LAKE, 'w', encoding='utf-8') as out_f:
        if exo_json:
            for row in exo_json:
                try:
                    entry = {"entity_id": f"P1_2_EXO_{records_processed:05d}", "source": "NASA_EXO", "name": row['pl_name'], "period_days": float(row['pl_orbper']), "semi_major_au": float(row['pl_orbsmax'])}
                    out_f.write(json.dumps(entry) + "\n")
                    records_processed += 1
                except: continue
        if asteroid_json and 'data' in asteroid_json:
            for row in asteroid_json['data']:
                try:
                    entry = {"entity_id": f"P1_2_AST_{records_processed:05d}", "source": "JPL_SBDB", "name": row[0], "period_days": float(row[2]), "semi_major_au": float(row[1])}
                    out_f.write(json.dumps(entry) + "\n")
                    records_processed += 1
                except: continue
    print(f"\n[+] P1_2 Normalized Raw Lake built. Total records: {records_processed}")
    print(f"[*] Audit Timestamp: {time.ctime()}")

if __name__ == "__main__":
    build_lake()