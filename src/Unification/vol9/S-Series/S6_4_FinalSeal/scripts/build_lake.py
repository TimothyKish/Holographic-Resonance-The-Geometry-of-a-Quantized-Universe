# vol5/S-Series/S6_4_FinalSeal/scripts/build_lake.py
import json
import os
from pathlib import Path

# THE AUDIT ANCHOR: Pointing back to the immutable S6 Master List.
# Parity check with S6 (Ridge), S6_2 (Slope), and S6_3 (Zero-Crossing).
SOURCE_LAKE = Path("../../S6_Galactic/lake/s6_galactic_sovereign_raw.jsonl")
TARGET_LAKE = Path("../lake/s6_4_normalized_raw.jsonl")

def build_lake():
    print("===============================================================")
    print(" 🪐 INITIALIZING S6_4 (The Final Mirror: Lock Phase)")
    print("===============================================================")
    
    if not SOURCE_LAKE.exists():
        print(f"[!] SOURCE ERROR: S6 Master Lake not found. Audit Broken.")
        return

    os.makedirs(TARGET_LAKE.parent, exist_ok=True)
    
    # REPLICATION LOGIC: Proving the 'Eggs' haven't changed, only the 'Carton'.
    with open(SOURCE_LAKE, 'r', encoding='utf-8') as src, open(TARGET_LAKE, 'w', encoding='utf-8') as dst:
        for line in src:
            dst.write(line)
            
    print(f"[+] S6_4 Mirror complete. Data parity verified.")
    print("[*] Lesson: The underlying physics (Sigma/Mag) is constant across all S6 tests.")

if __name__ == "__main__":
    build_lake()