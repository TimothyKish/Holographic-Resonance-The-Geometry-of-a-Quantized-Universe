import requests
import os

def harvest_hyperleda_kinematics():
    # Source VII/237/meandata contains the ACTUAL physics (vdis, bt)
    # We pull RA, Dec, PGC, velocity dispersion, and B-magnitude
    url = "https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=VII/237/meandata&-out.max=20000&vdis=%3E50"
    
    output_path = r"C:\Users\timot\Downloads\Science\src\Unification\vol5\S-Series\G1_HyperLeda_Galaxy\lake\hyperleda_raw.tsv"

    print("🛰️  HARVESTING HYPERLEDA KINEMATICS (Table: meandata)...")
    
    try:
        with requests.get(url, stream=True, timeout=120) as r:
            r.raise_for_status()
            with open(output_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        print(f"✅ KINEMATIC DATA SECURED: {output_path}")
        size_mb = os.path.getsize(output_path) / (1024*1024)
        print(f"📂 File Size: {size_mb:.2f} MB")

    except Exception as e:
        print(f"❌ HARVEST FAILED: {e}")

if __name__ == "__main__":
    harvest_hyperleda_kinematics()