import json
import os
from pathlib import Path

RAW_LAKE = Path("../lake/q1_spectra_raw.jsonl")
PROMOTED_LAKE = Path("../lake/q1_spectra_promoted.jsonl")

def promote():
    print("[*] Promoting Q1_Spectra to Vol5 Schema...")
    if not RAW_LAKE.exists():
        print("[-] Raw lake not found.")
        return

    records = []
    with open(RAW_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            # The signature of the quantum state: Wavelength * Energy difference
            # (In physics, E = hc/lambda, so lambda * E is a constant. We test the lattice against this geometry)
            energy_diff = data["upper_energy_cm1"] - data["lower_energy_cm1"]
            
            promoted = {
                "entity_id": data["entity_id"],
                "domain": "Q1_Spectra",
                "primary_value": data["wavelength_nm"],
                "secondary_value": energy_diff,
                "meta": {
                    "element": data["element"],
                    "source": "NIST ASD (Empirical)"
                }
            }
            records.append(promoted)

    with open(PROMOTED_LAKE, 'w', encoding='utf-8') as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")
            
    print(f"[+] Promotion complete. {len(records)} quantum states ready for the Lattice.")

if __name__ == "__main__":
    promote()