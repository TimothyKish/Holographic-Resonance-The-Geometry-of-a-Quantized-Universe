# ==============================================================================
# SCRIPT: convert_frb_json_to_jsonl.py
# TARGET: Convert FRB master file from JSON array to JSONL format
# AUTHORS: Timothy John Kish & Phoenix Aurora
# LICENSE: Sovereign Protected / KishLattice 16pi Initiative Copyright 2026
# ==============================================================================
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "lakes" / "inputs" / "frb_master.jsonl"

def main():
    # Load the JSON array (even though the file is named .jsonl)
    with open(INPUT, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Overwrite with JSONL format
    with open(INPUT, "w", encoding="utf-8") as f:
        for entry in data:
            f.write(json.dumps(entry) + "\n")

    print("FRB master lake successfully converted to JSONL format.")

if __name__ == "__main__":
    main()
