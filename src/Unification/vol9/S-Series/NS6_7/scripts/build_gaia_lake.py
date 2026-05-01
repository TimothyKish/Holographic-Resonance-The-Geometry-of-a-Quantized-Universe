import requests
import time
import os
import io
import csv

# 🛡️ NS6_26: THE GAIA 3D HARVESTER
# -----------------------------------------------------------
# Target: Gaia DR3 (I/355/gaiadr3)
# Goal: Pull Parallax-verified stars to calculate true physical km/s.

def build_gaia_lake():
    url = "http://tapvizier.u-strasbg.fr/TAPVizieR/tap/sync"
    
    # THE GAIA QUERY: Pure Local Distance and Motion
    query = """
    SELECT TOP 250000
    Source as objID, RA_ICRS as ra, DE_ICRS as dec, 
    Plx as parallax, e_Plx,
    pmRA, e_pmRA, pmDE, e_pmDE,
    Gmag, BPmag, RPmag,
    RUWE
    FROM "I/355/gaiadr3"
    WHERE Plx > 1.0 
      AND (Plx / e_Plx) > 10.0
      AND RUWE < 1.4
    """
    
    params = {"request": "doQuery", "lang": "ADQL", "format": "csv", "query": query}
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    output_path = os.path.join(project_root, 'lake', 'Master_Gaia.csv')

    print(f"🛰️ INITIATING GAIA 3D HARVEST")
    print(f"Targeting 250,000 Parallax-Verified Anchors...")
    
    attempt = 1
    while attempt <= 50:
        try:
            print(f"[{time.strftime('%H:%M:%S')}] Attempt {attempt}: Knocking on the ESA/VizieR Backbone...", end="\r")
            response = requests.post(url, data=params, timeout=120) # Gaia tables are huge, give it 2 minutes to think
            
            if response.status_code == 200:
                print(f"\n✅ HANDSHAKE SUCCESSFUL! Downloading Gaia Lake...")
                
                # Write the CSV straight to the lake
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                # Quick count to verify
                with open(output_path, 'r', encoding='utf-8') as f:
                    row_count = sum(1 for row in f) - 1 # minus header
                    
                if row_count > 0:
                    print(f"🏆 GAIA LAKE BUILT: {row_count:,} 3D anchors saved to {os.path.basename(output_path)}")
                    break
                else:
                    print("\n❌ Server returned empty table. Retrying...")
            else:
                print(f"\n⚠️ Server Busy (Status {response.status_code}). Retrying in 30s...")
                
        except Exception as e:
            print(f"\n⚠️ Connection spike. Holding line... ({e})")
            
        attempt += 1
        time.sleep(30)

if __name__ == "__main__":
    try:
        build_gaia_lake()
    except Exception as e:
        print(f"\n❌ SCRIPT CRASHED: {e}")
    finally:
        input("\nPress ENTER to close this window...")