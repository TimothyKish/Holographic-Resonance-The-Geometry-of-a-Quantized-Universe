# vol5/S-Series/S6_2_Normalized/scripts/build_lake.py
import json
import os
from pathlib import Path

# THE SOVEREIGN SOURCE: Mirroring the S6 Master List
SOURCE_LAKE = Path("../../S6_Galactic/lake/s6_galactic_sovereign_raw.jsonl")
TARGET_LAKE = Path("../lake/s6_2_normalized_raw.jsonl")

def build_lake():
    print("===============================================================")
    print(" 🪐 INITIALIZING S6_2 (Normalized Galactic Mirror)")
    print("===============================================================")
    
    if not SOURCE_LAKE.exists():
        print(f"[!] SOURCE ERROR: S6 Master Lake not found at {SOURCE_LAKE}")
        print("[*] Please ensure S6_Galactic/lake/s6_galactic_sovereign_raw.jsonl exists.")
        return

    os.makedirs(TARGET_LAKE.parent, exist_ok=True)
    
    records_mirrored = 0
    with open(SOURCE_LAKE, 'r', encoding='utf-8') as src, open(TARGET_LAKE, 'w', encoding='utf-8') as dst:
        for line in src:
            # We pass the data through 1:1 to maintain audit integrity
            dst.write(line)
            records_mirrored += 1
            
    print(f"[+] S6_2 Mirror complete. {records_mirrored} benchmark galaxies reflected.")
    print("[*] Status: Ready for Normalization Flip.")

if __name__ == "__main__":
    build_lake()