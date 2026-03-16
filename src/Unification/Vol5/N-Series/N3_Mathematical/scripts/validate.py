# vol5/N-Series/N3_Noise/scripts/validate.py
import json

def validate_schema():
    print("[*] Running Mondy's Schema Validation on N3_Noise...")
    
    valid = True
    with open("../lake/noise_null_scalarized.jsonl", "r") as f:
        for line in f:
            entry = json.loads(line)
            
            if entry["geometry_payload"] != {}:
                print(f"[!] ERROR: Geometry payload not empty in {entry['id']}")
                valid = False
            if entry["scalar_invariant"] != 0.0:
                print(f"[!] ERROR: Scalar invariant not zeroed in {entry['id']}")
                valid = False
            if entry["domain"] != "N3_Noise":
                print(f"[!] ERROR: Invalid domain tag in {entry['id']}")
                valid = False
                
    if valid:
        print("[+] Validation Passed: N3_Noise is a perfect mathematical flatline.")
    else:
        print("[-] Validation Failed. Do not proceed to pinch.")

if __name__ == "__main__":
    validate_schema()