# vol5/T-Series/T4_Cosmological/scripts/validate.py
import json

def validate_schema():
    print("[*] Running Mondy's Schema Validation on T4_Cosmological...")

    valid = True

    with open("../lake/temporal_real_scalarized.jsonl", "r") as f:
        for line in f:
            entry = json.loads(line)

            if entry["domain"] != "T4_Cosmological":
                print(f"[!] ERROR: Invalid domain tag in {entry['id']}")
                valid = False

            if "raw_payload" not in entry:
                print(f"[!] ERROR: Missing raw_payload in {entry['id']}")
                valid = False

            if "geometry_payload" not in entry:
                print(f"[!] ERROR: Missing geometry_payload in {entry['id']}")
                valid = False

    if valid:
        print("[+] Validation Passed: T4_Cosmological is schema‑clean.")
    else:
        print("[-] Validation Failed. Do not proceed to pinch.")

if __name__ == "__main__":
    validate_schema()
