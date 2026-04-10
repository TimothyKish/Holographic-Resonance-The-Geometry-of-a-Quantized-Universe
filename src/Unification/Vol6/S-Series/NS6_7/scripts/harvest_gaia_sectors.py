import requests
import pandas as pd
import io
import os
import time

def harvest_gaia_sectors():
    # Gaia Archive TAP Endpoint
    url = "https://gea.esac.esa.int/tap-server/tap/sync"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    lake_dir = os.path.join(project_root, 'lake')
    
    if not os.path.exists(lake_dir): os.makedirs(lake_dir)

    # Consistent Quadrant Logic
    sectors = {
        'NW': "ra <= 180 AND dec > 15",
        'NE': "ra > 180 AND dec > 15",
        'SW': "ra <= 180 AND dec <= 15",
        'SE': "ra > 180 AND dec <= 15"
    }

    for name, bounds in sectors.items():
        output_file = os.path.join(lake_dir, f'Gaia_Sector_{name}.csv')
        if os.path.exists(output_file): continue

        print(f"🛰️  HARVESTING GAIA SECTOR: {name}...")
        
        # Querying high-precision stars (Parallax SNR > 10)
        query = f"""
        SELECT TOP 500000
        source_id, ra, dec, parallax, parallax_error
        FROM gaiadr3.gaia_source
        WHERE parallax > 0 
          AND parallax_over_error > 10
          AND {bounds}
        """
        
        params = {"request": "doQuery", "lang": "ADQL", "format": "csv", "query": query}
        
        try:
            # Gaia server is generally faster but strict on large pulls
            response = requests.post(url, data=params, timeout=1200)
            if response.status_code == 200:
                df = pd.read_csv(io.StringIO(response.text))
                df.to_csv(output_file, index=False)
                print(f"   ✅ SAVED: {len(df):,} stars to {output_file}")
            else:
                print(f"   ❌ FAILED {name}: {response.status_code}")
            time.sleep(5) 

        except Exception as e:
            print(f"   ❌ CONNECTION ERROR in {name}: {e}")

if __name__ == "__main__":
    harvest_gaia_sectors()