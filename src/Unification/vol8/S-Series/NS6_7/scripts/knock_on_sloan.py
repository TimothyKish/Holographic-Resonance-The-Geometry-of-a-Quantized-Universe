import pandas as pd
import requests
import time
import io
import os

# 🛡️ NS6_12: THE SLOAN SIEGE (100K PROBE PULL)
# -----------------------------------------------------------
# Target: VizieR TAP Backbone (SDSS DR16)
# Constraints: z (0.01 - 0.70), velDisp > 100, Class=Galaxy
# Goal: 100,000 probes to lock the "Universal Staircase."

def knock_on_sloan():
    # TAP URL (The Direct Backbone)
    url = "http://tapvizier.u-strasbg.fr/TAPVizieR/tap/sync"
    
    # ADQL Query (Professional SQL for Galaxies)
    # We pull the Cardinal Points (RA, Dec) + Physics (z, Vdisp, rpmag)
    query = """
    SELECT TOP 100000 
    objID, RA_ICRS, DE_ICRS, zsp, Vdisp, rpmag, class
    FROM "V/154/sdss16"
    WHERE (zsp > 0.01 AND zsp < 0.70) 
      AND Vdisp > 100 
      AND class = 3
      AND zwarning = 0
    """
    
    params = {
        "request": "doQuery",
        "lang": "ADQL",
        "format": "csv",
        "query": query
    }

    print("🛰️ SIEGE INITIATED: Waiting for Sloan Backbone to respond...")
    attempt = 1
    
    while True:
        try:
            print(f"[{time.strftime('%H:%M:%S')}] Attempt {attempt}: Knocking on the door...", end="\r")
            response = requests.post(url, data=params, timeout=30)
            
            if response.status_code == 200:
                print(f"\n✅ DOOR OPENED! Ingesting 100k Probes...")
                data = pd.read_csv(io.StringIO(response.text))
                
                # Save to our Lake folder
                output_path = os.path.join('..', 'lake', 'sloan_100k_full_lake.csv')
                data.to_csv(output_path, index=False)
                
                print(f"🏆 MISSION ACCOMPLISHED: {len(data)} galaxies added to the lake.")
                print(f"File saved to: {output_path}")
                break
            else:
                print(f"\n❌ Server Busy (Status {response.status_code}). Retrying in 60s...")
        
        except Exception as e:
            # This catches the DNS/Connection errors you saw earlier
            pass
            
        attempt += 1
        time.sleep(60) # Wait 1 minute between knocks to avoid getting blocked

if __name__ == "__main__":
    knock_on_sloan()