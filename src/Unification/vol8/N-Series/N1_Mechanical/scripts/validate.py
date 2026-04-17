# vol5/N-Series/N1_Lotto/scripts/validate.py
import json

def validate_schema():
    print("[*] Running Mondy's Schema Validation on N1_Lotto...")
    
    valid = True
    with open("../lake/lotto_null_scalarized.jsonl", "r") as f:
        for line in f:
            entry = json.loads(line)
            
            if entry["geometry_payload"] != {}:
                print(f"[!] ERROR: Geometry payload not empty in {entry['id']}")
                valid = False
            if entry["scalar_invariant"] != 0.0:
                print(f"[!] ERROR: Scalar invariant not zeroed in {entry['id']}")
                valid = False
            if entry["domain"] != "N1_Lotto":
                print(f"[!] ERROR: Invalid domain tag in {entry['id']}")
                valid = False
                
    if valid:
        print("[+] Validation Passed: N1_Lotto is a perfect structural null.")
    else:
        print("[-] Validation Failed. Do not proceed to pinch.")

if __name__ == "__main__":
    validate_schema()