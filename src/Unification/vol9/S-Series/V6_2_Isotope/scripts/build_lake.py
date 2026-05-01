# vol6/S-Series/V6_2_Isotope/scripts/build_lake.py
import json
import os
from pathlib import Path

TARGET_LAKE = Path("../lake/v6_2_isotopes_raw.jsonl")

def build_lake():
    print("===============================================================")
    print(" 🧪 INITIALIZING V6_2: THE ISOTOPIC PHASE AUDIT")
    print("===============================================================")
    
    # Comparing "Open" vs "Sealed" atmosphere/regolith markers
    isotope_data = [
        {"name": "Earth Atmosphere", "ar_40_36": 298.56, "status": "OPEN"},
        {"name": "Mars Atmosphere", "ar_40_36": 1900.0, "status": "SEALED"},
        {"name": "Chondrite Meteorite", "ar_40_36": 0.0001, "status": "PRIMORDIAL"},
        {"name": "Titan Atmosphere", "ar_40_36": 1.4, "status": "OPEN_COLD"}
    ]
    
    os.makedirs(TARGET_LAKE.parent, exist_ok=True)
    with open(TARGET_LAKE, 'w', encoding='utf-8') as f:
        for entry in isotope_data:
            f.write(json.dumps(entry) + "\n")
            
    print(f"[+] V6_2 Isotope Lake built. Testing the Rotational Brake.")

if __name__ == "__main__":
    build_lake()