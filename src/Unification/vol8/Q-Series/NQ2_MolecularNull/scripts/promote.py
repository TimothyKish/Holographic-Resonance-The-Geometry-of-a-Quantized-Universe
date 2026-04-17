# vol5/Q-Series/NQ2_MolecularNull/scripts/promote.py
import json
import os
from pathlib import Path

RAW_LAKE = Path("../lake/nq2_molecular_raw.jsonl")
PROMOTED_LAKE = Path("../lake/nq2_molecular_promoted.jsonl")

def promote():
    print("[*] Promoting NQ2_MolecularNull to Vol5 Schema...")
    records = []
    with open(RAW_LAKE, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            promoted = {
                "entity_id": data["entity_id"],
                "domain": "NQ2_MolecularNull",
                "primary_value": data["value_scrambled"], # Mapping the scrambled value
                "secondary_value": 1.0,
                "meta": { "molecule": data["molecule"], "source": "NIST (Scrambled)" }
            }
            records.append(promoted)

    os.makedirs(PROMOTED_LAKE.parent, exist_ok=True)
    with open(PROMOTED_LAKE, 'w', encoding='utf-8') as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")
    print(f"[+] Promotion complete. {len(records)} scrambled states ready.")

if __name__ == "__main__":
    promote()