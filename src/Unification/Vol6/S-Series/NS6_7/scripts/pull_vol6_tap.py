import requests
import pandas as pd
import io
import os

def harvest_vol6():
    # 1. Establish repeatable paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    lake_dir = os.path.join(project_root, 'lake')
    
    # Ensure the correct lake folder exists
    if not os.path.exists(lake_dir):
        os.makedirs(lake_dir)
        
    output_path = os.path.join(lake_dir, 'Master_Galaxy_Vol6.csv')

    # 2. Define the TAP Query (SDSS DR16)
    url = "http://tapvizier.u-strasbg.fr/TAPVizieR/tap/sync"
    
    # We use RA_ICRS/DE_ICRS as confirmed in your Full-Sky PDF 
    query = """
    SELECT TOP 500000
    objID, RA_ICRS, DE_ICRS, zsp, Vdisp, spCl
    FROM "V/154/sdss16"
    WHERE spCl = 'GALAXY' 
      AND mode = 1
      AND zsp BETWEEN 0.00 AND 1.00
      AND Vdisp > 70
      AND RA_ICRS BETWEEN 0 AND 360
      AND DE_ICRS BETWEEN -20 AND 90
    """
    
    print(f"🛰️  INITIATING REPEATABLE HARVEST...")
    print(f"📂  TARGET FOLDER: {lake_dir}")
    
    params = {
        "request": "doQuery",
        "lang": "ADQL",
        "format": "csv",
        "query": query
    }
    
    try:
        # 10-minute timeout for the massive join operation
        response = requests.post(url, data=params, timeout=600)
        
        if response.status_code == 200:
            # Verify we didn't just get headers
            if len(response.text) < 5000:
                print("⚠️  Warning: Small file received. Verify constraints.")
            
            df = pd.read_csv(io.StringIO(response.text))
            df.to_csv(output_path, index=False)
            print(f"✅  SUCCESS: {len(df):,} galaxies saved to {output_path}")
        else:
            print(f"❌  SERVER ERROR {response.status_code}: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌  CONNECTION FAILED: {e}")

if __name__ == "__main__":
    harvest_vol6()