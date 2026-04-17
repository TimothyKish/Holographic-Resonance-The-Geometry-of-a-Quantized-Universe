# ==============================================================================
# PROJECT: THE 16PI INITIATIVE | VOLUME 5: UNIFICATION
# SCRIPT: scripts/schema/validate_lake.py
# DESCRIPTION: Validates the domain entries in volumes.json against schema.json
# to ensure perfect geometric coordinate formatting before scalarization.
# ==============================================================================

import json
import jsonschema
from jsonschema import validate
import os

# --- PATH RESOLUTION ---
# Assumes script is run from anywhere, resolving relative to the script's location
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCHEMA_PATH = os.path.join(BASE_DIR, 'lakes', 'inputs', 'schema.json')
VOLUMES_PATH = os.path.join(BASE_DIR, 'lakes', 'inputs', 'volumes.json')

def load_json(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def run_validation():
    print("[*] INITIALIZING VOLUME 5 GATEKEEPER: Schema Validation")
    
    try:
        schema = load_json(SCHEMA_PATH)
        volumes_data = load_json(VOLUMES_PATH)
        print(f"[*] Loaded schema and found {len(volumes_data)} domain records.")
    except Exception as e:
        print(f"[!] ERROR LOADING FILES: {e}")
        return

    # Validate each record in the array
    valid_count = 0
    for idx, record in enumerate(volumes_data):
        try:
            validate(instance=record, schema=schema)
            print(f"  [+] Validated: {record.get('domain_id')} | {record.get('phenomenon')}")
            valid_count += 1
        except jsonschema.exceptions.ValidationError as err:
            print(f"  [!] VALIDATION FAILED on record {idx} ({record.get('domain_id')}):")
            print(f"      Reason: {err.message}")

    print("-" * 50)
    if valid_count == len(volumes_data):
        print("[*] SUCCESS: All records passed the Kish Lattice Schema.")
        print("[*] The Lake is clean. Ready for Scalarization.")
    else:
        print(f"[!] WARNING: Only {valid_count} out of {len(volumes_data)} records passed.")

if __name__ == "__main__":
    run_validation()