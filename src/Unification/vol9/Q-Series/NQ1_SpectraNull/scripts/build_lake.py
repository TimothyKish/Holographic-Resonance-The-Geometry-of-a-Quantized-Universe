# vol5/Q-Series/NQ1_SpectraNull/scripts/build_lake.py
import json
import random
import os
from pathlib import Path

# Target the pristine empirical lake we just built
REAL_Q1_LAKE_PATH = Path("../../Q1_Spectra/lake/q1_spectra_raw.jsonl") 
RAW_NULL_LAKE = Path("../lake/nq1_spectra_raw.jsonl")

def build_quantum_null():
    print("===============================================================")
    print(" 🪞 INITIALIZING NQ1_SPECTRA (Scrambled Quantum Null)")
    print("===============================================================")
    
    if not REAL_Q1_LAKE_PATH.exists():
        print(f"[-] ERROR: Cannot find the authentic Q1 Lake at {REAL_Q1_LAKE_PATH}")
        print("    Please ensure Q1_Spectra has been successfully built first.")
        return

    print(f"[*] Ingesting authentic quantum data from: {REAL_Q1_LAKE_PATH.name}...")
    
    authentic_wavelengths = []
    base_records = []
    
    # 1. Read the real data and decouple the Wavelengths from the Energy States
    with open(REAL_Q1_LAKE_PATH, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
                
                # Store the wavelength in our list to be scrambled
                authentic_wavelengths.append(entry["wavelength_nm"])
                
                # Store the rest of the record
                base_records.append({
                    "element": entry["element"],
                    "lower_energy_cm1": entry["lower_energy_cm1"],
                    "upper_energy_cm1": entry["upper_energy_cm1"],
                    "raw_nist_dump": entry.get("raw_nist_dump", {})
                })
            except (KeyError, json.JSONDecodeError):
                continue
                
    print(f"[*] Extracted {len(authentic_wavelengths)} physical quantum states.")
    print("[*] Scrambling emitted wavelengths to destroy quantum resonance...")
    
    # 2. Shuffle ONLY the wavelengths (Destroying the physical relationship)
    random.shuffle(authentic_wavelengths)
    
    os.makedirs(RAW_NULL_LAKE.parent, exist_ok=True)
    
    # 3. Write the scrambled pairs to the Null Lake
    with open(RAW_NULL_LAKE, "w", encoding="utf-8") as out_f:
        for i in range(len(base_records)):
            scrambled_entry = {
                "entity_id": f"NULL_NIST_{base_records[i]['element'].replace(' ', '')}_{i:05d}",
                "domain": "null_quantum",
                "element": base_records[i]["element"],
                "wavelength_nm_scrambled": authentic_wavelengths[i],
                "lower_energy_cm1": base_records[i]["lower_energy_cm1"],
                "upper_energy_cm1": base_records[i]["upper_energy_cm1"],
                "raw_nist_dump": base_records[i]["raw_nist_dump"]
            }
            out_f.write(json.dumps(scrambled_entry) + "\n")
            
    print(f"[*] NQ1_Spectra Raw Lake built successfully. Physics destroyed. Distributions preserved.")

if __name__ == "__main__":
    build_quantum_null()