import requests
import pandas as pd
import io
import os
import time

def harvest_gaia_physical():
    url = "https://gea.esac.esa.int/tap-server/tap/sync"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    lake_dir = os.path.join(project_root, 'lake')
    
    if not os.path.exists(lake_dir): os.makedirs(lake_dir)

    sectors = {
        'NW': "ra <= 180 AND dec > 15",
        'NE': "ra > 180 AND dec > 15",
        'SW': "ra <= 180 AND dec <= 15",
        'SE': "ra > 180 AND dec <= 15"
    }

    for name, bounds in sectors.items():
        output_file = os.path.join(lake_dir, f'Gaia_Physical_{name}.csv')
        
        # We target the 'Lite' table for speed, but ensure the core physics are there
        print(f"🛰️  REFRESHING SECTOR {name} (Physical Payload)...")
        
        query = f"""
        SELECT TOP 500000
        source_id, ra, dec, parallax, pmra, pmdec, phot_g_mean_mag
        FROM gaiadr3.gaia_source
        WHERE parallax_over_error > 20
          AND pmra IS NOT NULL
          AND pmdec IS NOT NULL
          AND {bounds}
        """
        
        params = {"request": "doQuery", "lang": "ADQL", "format": "csv", "query": query}
        
        try:
            response = requests.post(url, data=params, timeout=1200)
            if response.status_code == 200:
                df = pd.read_csv(io.StringIO(response.text))
                df.to_csv(output_file, index=False)
                print(f"   ✅ SAVED: {len(df):,} Physical Stars to {name}")
            else:
                print(f"   ❌ FAILED: {response.status_code}")
            time.sleep(5) 
        except Exception as e:
            print(f"   ❌ ERROR: {e}")

if __name__ == "__main__":
    harvest_gaia_physical()