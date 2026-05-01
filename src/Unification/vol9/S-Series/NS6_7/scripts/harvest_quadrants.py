import requests
import pandas as pd
import io
import os
import time

def harvest_vol6_sectors():
    url = "http://tapvizier.u-strasbg.fr/TAPVizieR/tap/sync"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    lake_dir = os.path.join(project_root, 'lake')
    
    if not os.path.exists(lake_dir): os.makedirs(lake_dir)

    sectors = {
        'NW': "RA_ICRS <= 180 AND DE_ICRS > 15",
        'NE': "RA_ICRS > 180 AND DE_ICRS > 15",
        'SW': "RA_ICRS <= 180 AND DE_ICRS <= 15",
        'SE': "RA_ICRS > 180 AND DE_ICRS <= 15"
    }

    for name, bounds in sectors.items():
        output_file = os.path.join(lake_dir, f'Sector_{name}_Vol6.csv')
        
        # Skip if already downloaded to save time
        if os.path.exists(output_file):
            print(f"⏩  Sector {name} already exists. Skipping...")
            continue

        print(f"🛰️  HARVESTING SECTOR: {name} (Limit 500k)...")
        
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
        
        try:
            # Increased timeout to 20 mins for the stubborn SW/SE sectors
            response = requests.post(url, data=params, timeout=1200) 
            
            if response.status_code == 200:
                # Check for empty or header-only returns
                if len(response.text) < 2000:
                    print(f"⚠️  Sector {name} returned negligible data (Survey Limit).")
                    continue
                
                df = pd.read_csv(io.StringIO(response.text))
                df.to_csv(output_file, index=False)
                print(f"✅  SAVED: {len(df):,} galaxies to {output_file}")
            else:
                print(f"❌  SECTOR {name} FAILED: Server Error {response.status_code}")
            
            time.sleep(5) # Respect the endpoint

        except Exception as e:
            print(f"❌  CONNECTION ERROR in {name}: {e}")

    print("\n🏁  Sector Pull Complete. Check the 'lake' folder for individual CSVs.")

if __name__ == "__main__":
    harvest_vol6_sectors()