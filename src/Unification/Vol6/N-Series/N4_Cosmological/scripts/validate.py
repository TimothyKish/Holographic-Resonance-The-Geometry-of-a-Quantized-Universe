# vol5/N-Series/N4_Temporal/scripts/validate.py
import json

def validate_schema():
    print("[*] Running Mondy's Schema Validation...")
    
    valid = True
    with open("../lake/temporal_null_scalarized.jsonl", "r") as f:
        for line in f:
            entry = json.loads(line)
            
            if entry["geometry_payload"] != {}:
                print(f"[!] ERROR: Geometry payload not empty in {entry['id']}")
                valid = False
            if entry["scalar_invariant"] != 0.0:
                print(f"[!] ERROR: Scalar invariant not zeroed in {entry['id']}")
                valid = False
            if entry["domain"] != "N4_Temporal":
                print(f"[!] ERROR: Invalid domain tag in {entry['id']}")
                valid = False
                
    if valid:
        print("[+] Validation Passed: N4_Temporal is a perfect structural null.")
    else:
        print("[-] Validation Failed. Do not proceed to pinch.")

if __name__ == "__main__":
    validate_schema()