import requests
import time
import os
import pandas as pd
import io

# 🛡️ NS6_35: THE GAIA CHUNKED HARVESTER (Unstoppable Mode)
# -----------------------------------------------------------
def build_gaia_lake_chunked():
    url = "http://tapvizier.u-strasbg.fr/TAPVizieR/tap/sync"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    output_path = os.path.join(project_root, 'lake', 'Master_Gaia.csv')
    
    chunk_size = 50000
    total_requested = 250000
    
    print(f"🛰️ INITIATING CHUNKED GAIA HARVEST: {total_requested} stars")
    
    all_chunks = []
    
    for i in range(0, total_requested, chunk_size):
        offset = i
        print(f"\n🚀 Pulling Chunk: Stars {offset} to {offset + chunk_size}...")
        
        query = f"""
        SELECT TOP {chunk_size}
        Source as objID, RA_ICRS as ra, DE_ICRS as dec, 
        Plx as parallax, e_Plx, pmRA, pmDE, Gmag, RUWE
        FROM "I/355/gaiadr3"
        WHERE Gmag < 15 AND Plx > 1.0 AND (Plx / e_Plx) > 10.0 AND RUWE < 1.4
        OFFSET {offset}
        """
        
        params = {"request": "doQuery", "lang": "ADQL", "format": "csv", "query": query}
        
        success = False
        attempts = 0
        while not success and attempts < 5:
            try:
                response = requests.post(url, data=params, timeout=180)
                if response.status_code == 200:
                    df = pd.read_csv(io.StringIO(response.text))
                    all_chunks.append(df)
                    print(f"  ✅ Received {len(df)} stars.")
                    success = True
                else:
                    print(f"  ⚠️ Server Busy ({response.status_code}). Retrying in 10s...")
                    time.sleep(10)
            except Exception as e:
                print(f"  ⚠️ Timeout. Retrying... {attempts+1}/5")
                time.sleep(5)
            attempts += 1

    if all_chunks:
        final_df = pd.concat(all_chunks, ignore_index=True)
        final_df.to_csv(output_path, index=False)
        print(f"\n🏆 GAIA LAKE BUILT: {len(final_df):,} stars in {output_path}")
    else:
        print("\n❌ Failed to pull any data chunks.")

if __name__ == "__main__":
    build_gaia_lake_chunked()