# vol6/S-Series/V6_AntiLife/scripts/build_lake.py
import json
import os
from pathlib import Path

TARGET_LAKE = Path("../lake/v6_lethal_benchmarks.jsonl")

def build_lake():
    print("===============================================================")
    print(" 🧪 INITIALIZING V6: THE LETHAL RIDGE AUDIT")
    print("===============================================================")
    
    # We are pulling environments where the "Pocket" has closed.
    # We use TDS (Total Dissolved Solids) as our Kinetic Stiffness proxy.
    lethal_zones = [
        {"name": "Don Juan Pond", "tds_gl": 440.0, "status": "STERILE"},
        {"name": "Dead Sea (Deep)", "tds_gl": 340.0, "status": "EXTREME_ONLY"},
        {"name": "Gaet'ale Spring", "tds_gl": 430.0, "status": "STERILE"},
        {"name": "Lake Vida Brine", "tds_gl": 200.0, "status": "DORMANT"},
        {"name": "Mars Surface (Avg)", "uv_flux": 600.0, "status": "STERILE"}
    ]
    
    os.makedirs(TARGET_LAKE.parent, exist_ok=True)
    with open(TARGET_LAKE, 'w', encoding='utf-8') as f:
        for entry in lethal_zones:
            f.write(json.dumps(entry) + "\n")
            
    print(f"[+] V6 Lethal Lake built. Preparing to find the Negative Peak.")

if __name__ == "__main__":
    build_lake()