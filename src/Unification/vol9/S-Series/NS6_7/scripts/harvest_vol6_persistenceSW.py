import requests
import pandas as pd
import io
import os
import time

def harvest_persistence():
    url = "http://tapvizier.u-strasbg.fr/TAPVizieR/tap/sync"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    lake_dir = os.path.join(project_root, 'lake')
    
    # Target only what we are missing
    sectors = {
        'SW': "RA_ICRS <= 180 AND DE_ICRS <= 15"
    }

    print(f"🛡️  RESUMING HARVEST: TARGETING SW AND SE SECTORS...")

    for name, bounds in sectors.items():
        output_file = os.path.join(lake_dir, f'Sector_{name}_Vol6.csv')
        
        if os.path.exists(output_file):
            print(f"⏩  Sector {name} already exists. Skipping.")
            continue

        query = f"""
        SELECT TOP 500000
        objID, RA_ICRS, DE_ICRS, zsp, Vdisp, spCl
        FROM "V/154/sdss16"
        WHERE spCl = 'GALAXY' 
          AND mode = 1
          AND zsp BETWEEN 0.00 AND 1.00
          AND Vdisp > 70
          AND {bounds}
        """
        
        params = {"request": "doQuery", "lang": "ADQL", "format": "csv", "query": query}
        
        attempts = 0
        while attempts < 3:
            try:
                print(f"🛰️  Attempting {name} (Attempt {attempts+1}/3)...")
                response = requests.post(url, data=params, timeout=1800) # 30 min timeout
                
                if response.status_code == 200:
                    if len(response.text) < 2000:
                        print(f"⚠️  {name} contains no more data (Survey Limit).")
                        break
                    
                    df = pd.read_csv(io.StringIO(response.text))
                    df.to_csv(output_file, index=False)
                    print(f"✅  SAVED {len(df):,} rows to {output_file}")
                    break 
                else:
                    print(f"❌  Server Error {response.status_code}. Throttled?")
                    time.sleep(300) # Wait 5 mins if throttled
            
            except Exception as e:
                print(f"⚠️  Connection dropped. Sleeping 60s...")
                time.sleep(60)
            
            attempts += 1

    print("\n🏁  Persistence Check Complete.")

if __name__ == "__main__":
    harvest_persistence()