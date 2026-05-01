# vol5/T-Series/T2_Planetary/scripts/build_lake.py
import json
import urllib.request
import urllib.error
import time
import os
import socket
from datetime import datetime

socket.setdefaulttimeout(45)

BASE_URL = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
STATION_ID = "9414290"  # San Francisco, CA
RAW_LAKE = "../lake/planetary_real_raw.jsonl"

YEAR_START = 2015
YEAR_END = 2024  # inclusive, 10 full years

def fetch_year(year):
    params = (
        f"begin_date={year}0101"
        f"&end_date={year}1231"
        f"&station={STATION_ID}"
        f"&product=predictions"
        f"&datum=MLLW"
        f"&time_zone=gmt"
        f"&interval=hilo"
        f"&units=metric"
        f"&application=T2_Planetary"
        f"&format=json"
    )
    url = f"{BASE_URL}?{params}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Application/Science",
        "Accept": "application/json",
    }

    req = urllib.request.Request(url, headers=headers)
    max_retries = 3

    for attempt in range(max_retries):
        try:
            print(f"[*] Fetching {year} high/low tides...")
            with urllib.request.urlopen(req, timeout=45) as response:
                raw_response = response.read().decode("utf-8")
                data = json.loads(raw_response)
            return data
        except Exception as e:
            print(f"[-] Attempt {attempt + 1} for {year} failed: {e}")
            if attempt < max_retries - 1:
                print("[*] Sleeping 3 seconds before retry...")
                time.sleep(3)
            else:
                print(f"[-] FATAL: Unable to fetch year {year}.")
                return None

def build_lake():
    print("[*] INITIALIZING T2_PLANETARY (High/Low Tides, GMT)")
    print("[*] Enforcing Sovereign Chain of Custody (NOAA CO-OPS)...")

    events = []

    for year in range(YEAR_START, YEAR_END + 1):
        data = fetch_year(year)
        if not data or "predictions" not in data:
            continue

        for p in data["predictions"]:
            t_str = p.get("t")
            v_str = p.get("v")
            tide_type = p.get("type")  # 'H' or 'L'

            if not t_str:
                continue

            try:
                t_dt = datetime.strptime(t_str, "%Y-%m-%d %H:%M")
            except Exception:
                continue

            events.append({
                "time_str": t_str,
                "time_dt": t_dt,
                "height_m": float(v_str) if v_str is not None else None,
                "type": tide_type,
            })

        print(f"[+] Year {year} ingested ({len(data.get('predictions', []))} events).")
        time.sleep(1)  # polite spacing for API throttling

    print(f"[*] Total raw tide events collected: {len(events)}")

    # Sort globally by time and compute intervals
    events.sort(key=lambda e: e["time_dt"])

    intervals = []
    for i in range(len(events) - 1):
        e0 = events[i]
        e1 = events[i + 1]
        delta_hours = (e1["time_dt"] - e0["time_dt"]).total_seconds() / 3600.0

        intervals.append({
            "station": STATION_ID,
            "from_time": e0["time_str"],
            "to_time": e1["time_str"],
            "from_type": e0["type"],
            "to_type": e1["type"],
            "interval_hours": round(delta_hours, 6),
        })

    print(f"[*] Computed {len(intervals)} planetary temporal intervals (high/low tide steps).")

    os.makedirs("../lake", exist_ok=True)
    with open(RAW_LAKE, "w", encoding="utf-8") as out_f:
        for entry in intervals:
            out_f.write(json.dumps(entry) + "\n")

    print("[*] T2_Planetary Raw Lake built successfully. High/low tide cycles preserved.")

if __name__ == "__main__":
    build_lake()
