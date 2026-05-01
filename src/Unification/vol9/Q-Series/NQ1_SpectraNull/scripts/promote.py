# vol5/Q-Series/NQ1_SpectraNull/scripts/promote.py
import json
import os
from pathlib import Path

RAW_LAKE = Path("../lake/nq1_spectra_raw.jsonl")
PROMOTED_LAKE = Path("../lake/nq1_spectra_promoted.jsonl")

def promote():
    print("===============================================================")
    print(" 🪞 PROMOTING NQ1_SPECTRA_NULL (Scrambled Quantum Physics)")
    print("===============================================================")
    
    if not RAW_LAKE.exists():
        print(f"[-] ERROR: Raw lake not found at {RAW_LAKE}")
        return

    records = []
    with open(RAW_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                
                # The Quantum Geometric Payload (Energy Difference)
                energy_diff = abs(data["upper_energy_cm1"] - data["lower_energy_cm1"])
                
                promoted = {
                    "entity_id": data["entity_id"],
                    "domain": "NQ1_SpectraNull",
                    # CRITICAL: We map the SCRAMBLED wavelength here
                    "primary_value": data["wavelength_nm_scrambled"],
                    "secondary_value": energy_diff,
                    "meta": {
                        "element": data["element"],
                        "source": "NIST ASD (Scrambled Null Mirror)"
                    }
                }
                records.append(promoted)
            except Exception as e:
                continue

    os.makedirs(PROMOTED_LAKE.parent, exist_ok=True)
    with open(PROMOTED_LAKE, 'w', encoding='utf-8') as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")
            
    print(f"[+] Promotion complete. {len(records)} scrambled quantum states wrapped in Vol5 Schema.")

if __name__ == "__main__":
    promote()