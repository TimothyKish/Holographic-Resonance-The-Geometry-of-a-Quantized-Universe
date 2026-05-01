import pandas as pd
import requests
import time
import io
import os
import json

# 🛡️ NS6_13: THE MASTER FLEET HARVESTER
# -----------------------------------------------------------
# Goal: Build a Sovereign JSONL Lake with full Physics Stack.
# Standard: Lake_[Source]_[N]_[Zmin]_[Zmax]_[Constraint]

def build_master_fleet():
    url = "http://tapvizier.u-strasbg.fr/TAPVizieR/tap/sync"
    
    # THE DEEP WELL QUERY: Every physics field available
    query = """
    SELECT TOP 100000
    objID, ra, dec, zsp, Vdisp, e_Vdisp, 
    upmag, gpmag, rpmag, ipmag, zpmag,
    uPmag, gPmag, rPmag, iPmag, zPmag,
    uPrad, gPrad, rPrad, iPrad, zPrad,
    spCl, subCl, "spS/N"
    FROM "V/154/sdss16"
    WHERE (zsp > 0.01 AND zsp < 0.70) 
      AND Vdisp > 70 
      AND class = 3 
      AND zwarning = 0
    """
    
    params = {"request": "doQuery", "lang": "ADQL", "format": "csv", "query": query}
    lake_name = "Lake_SDSS_DR16_100K_z01_z70_V70_G.jsonl"
    output_path = os.path.join('..', 'lake', lake_name)

    print(f"🛰️ INITIATING MASTER HARVEST: {lake_name}")
    attempt = 1
    
    while True:
        try:
            print(f"[{time.strftime('%H:%M:%S')}] Attempt {attempt}: Knocking...", end="\r")
            response = requests.post(url, data=params, timeout=60)
            
            if response.status_code == 200:
                print(f"\n✅ HANDSHAKE SUCCESSFUL. Converting to JSONL...")
                df = pd.read_csv(io.StringIO(response.text))
                
                # Convert to JSONL line by line
                with open(output_path, 'w') as f:
                    for record in df.to_dict(orient='records'):
                        f.write(json.dumps(record) + '\n')
                
                print(f"🏆 FLEET LAKE BUILT: {len(df)} records in {output_path}")
                break
        except Exception:
            pass
            
        attempt += 1
        time.sleep(60)

if __name__ == "__main__":
    build_master_fleet()