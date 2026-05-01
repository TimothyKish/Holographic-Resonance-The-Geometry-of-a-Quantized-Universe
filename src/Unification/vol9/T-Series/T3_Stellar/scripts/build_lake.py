# vol5/T-Series/T3_Stellar/scripts/build_lake.py
import json
import urllib.request
import urllib.error
import time
import os
import socket

socket.setdefaulttimeout(45)

CHIME_URL = "https://storage.googleapis.com/chimefrb-dev.appspot.com/catalog2/chimefrbcat2.json"
RAW_LAKE = "../lake/stellar_real_raw.jsonl"

def build_lake():
    print("[*] INITIALIZING T3_STELLAR (Authentic FRB Temporal Cycles)")
    print("[*] Enforcing Sovereign Chain of Custody (CHIME/FRB Catalog)...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Application/Science',
        'Accept': 'application/json'
    }

    req = urllib.request.Request(CHIME_URL, headers=headers)
    max_retries = 3
    frb_data = None

    print("[*] Fetching CHIME FRB catalog...")

    for attempt in range(max_retries):
        try:
            print(f"[*] Connection attempt {attempt + 1} of {max_retries}...")
            with urllib.request.urlopen(req, timeout=45) as response:
                raw_response = response.read().decode('utf-8')
                frb_data = json.loads(raw_response)
            break
        except Exception as e:
            print(f"[-] Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print("[*] Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print("[-] FATAL ERROR: CHIME FRB catalog unreachable.")
                return

    print("[+] Sovereign download complete.")

    # Extract FRB events using mjd_400 or mjd_inf
    temporal_points = []

    for event in frb_data:
        name = event.get("tns_name") or event.get("previous_name")

        # Prefer mjd_400, fallback to mjd_inf
        mjd = event.get("mjd_400") or event.get("mjd_inf")

        if name and mjd:
            temporal_points.append({
                "name": name,
                "mjd": float(mjd)
            })

    print(f"[*] Extracted {len(temporal_points)} FRB temporal points.")

    # Compute intervals per FRB name
    intervals = []
    grouped = {}

    for entry in temporal_points:
        grouped.setdefault(entry["name"], []).append(entry["mjd"])

    for name, times in grouped.items():
        if len(times) < 2:
            continue

        times.sort()
        for i in range(len(times) - 1):
            interval = round(times[i+1] - times[i], 6)
            intervals.append({
                "name": name,
                "period_days": interval
            })

    print(f"[*] Computed {len(intervals)} authentic FRB temporal intervals.")

    os.makedirs("../lake", exist_ok=True)
    with open(RAW_LAKE, "w", encoding="utf-8") as out_f:
        for entry in intervals:
            out_f.write(json.dumps(entry) + "\n")

    print("[*] T3_Stellar Raw Lake built successfully. Authentic FRB cycles preserved.")

if __name__ == "__main__":
    build_lake()
