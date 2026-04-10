# vol5/T-Series/T2_Planetary/scripts/validate.py
import json

def validate_schema():
    print("[*] Running Mondy's Schema Validation on T2_Planetary...")

    valid = True

    with open("../lake/planetary_real_scalarized.jsonl", "r") as f:
        for line in f:
            entry = json.loads(line)

            if entry.get("domain") != "T2_Planetary":
                print(f"[!] ERROR: Invalid domain tag in {entry.get('id')}")
                valid = False

            if "raw_payload" not in entry:
                print(f"[!] ERROR: Missing raw_payload in {entry.get('id')}")
                valid = False

            if "geometry_payload" not in entry:
                print(f"[!] ERROR: Missing geometry_payload in {entry.get('id')}")
                valid = False

    if valid:
        print("[+] Validation Passed: T2_Planetary is schema-clean.")
    else:
        print("[-] Validation Failed. Do not proceed to pinch.")

if __name__ == "__main__":
    validate_schema()
