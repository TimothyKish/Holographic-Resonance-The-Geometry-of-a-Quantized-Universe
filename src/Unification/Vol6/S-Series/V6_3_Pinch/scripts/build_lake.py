# vol6/S-Series/V6_3_Pinch/scripts/build_lake.py
import json
import os
from pathlib import Path

TARGET_LAKE = Path("../lake/v6_3_pinch_raw.jsonl")

def build_lake():
    print("===============================================================")
    print(" 🧪 INITIALIZING V6_3: THE CUMULATIVE PINCH AUDIT")
    print("===============================================================")
    
    # Testing the "Multi-Factor" Seal
    pinch_data = [
        {"name": "Mars_Regolith_Composite", "ar_ratio": 1900.0, "perchlorate_gl": 10.0, "uv_stiffness": 50.0},
        {"name": "Earth_Deep_Brine", "ar_ratio": 298.0, "salinity_gl": 300.0, "uv_stiffness": 0.0},
        {"name": "Europa_Subsurface", "ar_ratio": 100.0, "salinity_gl": 50.0, "uv_stiffness": 0.0}
    ]
    
    os.makedirs(TARGET_LAKE.parent, exist_ok=True)
    with open(TARGET_LAKE, 'w', encoding='utf-8') as f:
        for entry in pinch_data:
            f.write(json.dumps(entry) + "\n")
            
    print(f"[+] V6_3 Pinch Lake built. Identifying the 'Geometric Hard-Stop'.")

if __name__ == "__main__":
    build_lake()