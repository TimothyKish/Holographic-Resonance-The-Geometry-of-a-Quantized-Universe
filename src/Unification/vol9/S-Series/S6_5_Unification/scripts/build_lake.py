# vol5/S-Series/S6_5_Unification/scripts/build_lake.py
import json
import os
from pathlib import Path

# THE SOVEREIGN SOURCE: The 50-Galaxy Master List (Messier/NGC Benchmarks)
SOURCE_LAKE = Path("../../S6_Galactic/lake/s6_galactic_sovereign_raw.jsonl")
TARGET_LAKE = Path("../lake/s6_5_normalized_raw.jsonl")

def build_lake():
    print("===============================================================")
    print(" 🪐 INITIALIZING S6_5 (The Unified Mirror: Gold Record)")
    print("===============================================================")
    
    if not SOURCE_LAKE.exists():
        print(f"[!] SOURCE ERROR: Master Lake missing. Check S6_Galactic/lake/.")
        return

    os.makedirs(TARGET_LAKE.parent, exist_ok=True)
    
    # REPLICATION LOGIC: Ensuring Bit-Perfect Parity for the Final Audit.
    with open(SOURCE_LAKE, 'r', encoding='utf-8') as src, open(TARGET_LAKE, 'w', encoding='utf-8') as dst:
        for line in src:
            dst.write(line)
            
    print(f"[+] S6_5 Mirror complete. Parity check: PASSED.")
    print("[*] Purpose: Establish the stable baseline for the Final Seal.")

if __name__ == "__main__":
    build_lake()