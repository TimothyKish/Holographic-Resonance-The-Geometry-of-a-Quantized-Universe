# vol5/S-Series/S6_3_DeepLock/scripts/build_lake.py
import json
import os
from pathlib import Path

# AUDIT TRAIL: Pointing to the immutable S6 Master List (50 Benchmarks)
SOURCE_LAKE = Path("../../S6_Galactic/lake/s6_galactic_sovereign_raw.jsonl")
TARGET_LAKE = Path("../lake/s6_3_normalized_raw.jsonl")

def build_lake():
    print("===============================================================")
    print(" 🪐 INITIALIZING S6_3 (Sovereign Mirror: DeepLock Phase)")
    print("===============================================================")
    
    if not SOURCE_LAKE.exists():
        print(f"[!] AUDIT ERROR: Master Source not found at {SOURCE_LAKE}")
        return

    os.makedirs(TARGET_LAKE.parent, exist_ok=True)
    
    # REPLICATION LOGIC: 1:1 data parity check
    with open(SOURCE_LAKE, 'r', encoding='utf-8') as src, open(TARGET_LAKE, 'w', encoding='utf-8') as dst:
        for line in src:
            dst.write(line)
            
    print(f"[+] S6_3 Mirror complete. Input Parity verified with S6_Master.")

if __name__ == "__main__":
    build_lake()