# vol5/T-Series/T3_Stellar/scripts/validate.py
import json

def validate_schema():
    print("[*] Running Mondy's Schema Validation on T3_Stellar...")

    valid = True

    with open("../lake/stellar_real_scalarized.jsonl", "r") as f:
        for line in f:
            entry = json.loads(line)

            if entry.get("domain") != "T3_Stellar":
                print(f"[!] ERROR: Invalid domain tag in {entry.get('id')}")
                valid = False

            if "raw_payload" not in entry:
                print(f"[!] ERROR: Missing raw_payload in {entry.get('id')}")
                valid = False

            if "geometry_payload" not in entry:
                print(f"[!] ERROR: Missing geometry_payload in {entry.get('id')}")
                valid = False

    if valid:
        print("[+] Validation Passed: T3_Stellar is schema‑clean.")
    else:
        print("[-] Validation Failed. Do not proceed to pinch.")

if __name__ == "__main__":
    validate_schema()
