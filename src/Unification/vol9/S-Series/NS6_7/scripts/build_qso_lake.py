import pandas as pd
import requests
import time
import io
import os
import json

# 🛡️ NS6_16: THE QUASAR (QSO) DEEP TIME HARVESTER
# -----------------------------------------------------------
# Target: SDSS DR16 Quasars (spCl = 'QSO')
# Goal: Build the "Deep Time" Lake for high-redshift lattice audits.

def build_qso_lake():
    url = "http://tapvizier.u-strasbg.fr/TAPVizieR/tap/sync"
    
    # THE QSO QUERY: spCl='QSO', no upper limit on Z!
    query = """
    SELECT TOP 100000
    objID, RA_ICRS as ra, DE_ICRS as dec, 
    zsp, e_zsp, 
    upmag, gpmag, rpmag, ipmag, zpmag,
    spCl, subCl, "spS/N"
    FROM "V/154/sdss16"
    WHERE spCl = 'QSO'
      AND zwarning = 0
      AND "spS/N" > 5
    """
    
    params = {"request": "doQuery", "lang": "ADQL", "format": "csv", "query": query}
    lake_name = "Lake_SDSS_DR16_100K_QSO.jsonl"
    
    os.makedirs('../lake', exist_ok=True)
    output_path = os.path.join('../lake', lake_name)

    print(f"🕳️ INITIATING QUASAR HARVEST: {lake_name}")
    attempt = 1
    
    while attempt <= 50:
        try:
            print(f"[{time.strftime('%H:%M:%S')}] Attempt {attempt}: Knocking on the Quasar Door...", end="\r")
            response = requests.post(url, data=params, timeout=60)
            
            if response.status_code == 200:
                print(f"\n✅ HANDSHAKE SUCCESSFUL! Downloading 100k Quasars...")
                df = pd.read_csv(io.StringIO(response.text))
                
                if len(df) == 0:
                    print("❌ Server returned an empty table. Retrying...")
                else:
                    # Convert to JSONL line by line
                    with open(output_path, 'w') as f:
                        for record in df.to_dict(orient='records'):
                            f.write(json.dumps(record) + '\n')
                    
                    print(f"🏆 QUASAR LAKE BUILT: {len(df)} deep-time probes saved to {output_path}")
                    break
            else:
                print(f"\n⚠️ Server Busy (Status {response.status_code}). Retrying in 30s...")
        except Exception as e:
            pass
            
        attempt += 1
        time.sleep(30)

if __name__ == "__main__":
    build_qso_lake()