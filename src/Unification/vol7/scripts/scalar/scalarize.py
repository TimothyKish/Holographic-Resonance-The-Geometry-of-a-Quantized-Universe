# ==============================================================================
# PROJECT: THE 16PI INITIATIVE | VOLUME 5: UNIFICATION
# SCRIPT: scripts/scalar/scalarize.py
# DESCRIPTION: Ingests validated domain data, applies cross-domain scale 
# multipliers, and outputs the unified geometric baselines to the unified lake.
# ==============================================================================

import json
import math
import os

# --- LATTICE CONSTANTS ---
PI = math.pi
KISH_CONSTANT = 16.0 / PI  # The core vacuum stiffness modulus (~5.0929)

# --- PATH RESOLUTION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INPUT_PATH = os.path.join(BASE_DIR, 'lakes', 'inputs', 'volumes.json')
OUTPUT_PATH = os.path.join(BASE_DIR, 'lakes', 'unified', 'unified_matrix.json')

def load_data(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def save_data(data, filepath):
    # Ensure output directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

def run_scalarization():
    print("[*] INITIALIZING VOLUME 5 UNIFIER: Cross-Domain Scalarization")
    
    try:
        volumes_data = load_data(INPUT_PATH)
    except FileNotFoundError:
        print(f"[!] ERROR: Could not find {INPUT_PATH}. Did you run validate_lake.py first?")
        return

    unified_records = []

    for record in volumes_data:
        domain = record["domain_id"]
        old_val = record["old_world_value"]
        multiplier = record["scalar_multiplier"]
        coords = record["lattice_coordinate"]
        
        print(f"\n[*] Processing Domain: {domain}...")
        
        # 1. SCALARIZE THE OLD WORLD VALUE
        # Bringing the raw measurement into a standardized unified scale
        scaled_value = old_val * multiplier
        
        # 2. CALCULATE THE LATTICE TENSION
        # Using the coordinate: k (modulus) * m (harmonic mode) + offset
        k = coords["modulus_k"]
        m = coords["harmonic_mode_m"]
        offset = coords["agency_offset_delta"]
        
        # This represents the geometric signature of the phenomenon
        geometric_signature = (k * m) + offset
        
        # Append to our unified output
        unified_record = {
            "domain_id": domain,
            "phenomenon": record["phenomenon"],
            "scaled_world_value": scaled_value,
            "geometric_signature": geometric_signature,
            "resolved_status": "UNIFIED" if record["resolved_paradox"] else "PENDING"
        }
        unified_records.append(unified_record)
        
        print(f"  -> Scaled Value: {scaled_value:.4e}")
        print(f"  -> Geometric Signature: {geometric_signature:.4f}")

    # Save to the unified lake
    save_data(unified_records, OUTPUT_PATH)
    print("-" * 50)
    print(f"[*] SUCCESS: Scalarization complete. Output saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    run_scalarization()