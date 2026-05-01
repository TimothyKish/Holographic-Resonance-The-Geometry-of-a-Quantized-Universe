# vol5/N-Series/N1_Lotto/scripts/build_lake.py
import json
import csv
import os
import urllib.request

# Sovereign Data Source: New York State Open Data Portal (Mega Millions)
# This endpoint is designed for programmatic access. No firewalls, no human required.
URL = "https://data.ny.gov/api/views/5xaw-6ayf/rows.csv?accessType=DOWNLOAD"
CSV_FILE = "../lake/us_megamillions_historical.csv"
RAW_LAKE = "../lake/lotto_null_raw.jsonl"

def build_lake():
    print("[*] INITIALIZING N1_LOTTO (Authentic Mechanical Chaos)")
    print("[*] Enforcing Sovereign Chain of Custody (Zero Human Intervention)...")
    
    # 1. Sovereign Download
    print(f"[*] Pulling official US Mega Millions CSV from data.ny.gov...")
    req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    
    try:
        with urllib.request.urlopen(req) as response:
            csv_data = response.read().decode('utf-8')
        
        with open(CSV_FILE, 'w', encoding='utf-8') as f:
            f.write(csv_data)
        print("[+] Sovereign download complete. Zero firewall interference.")
        
    except Exception as e:
        print(f"[-] FATAL ERROR: Sovereign pipeline broken by network error: {e}")
        return

    # 2. Parse the CSV into the Lattice JSONL Schema
    print("[*] Parsing Open Data CSV and building N1_Lotto Raw Lake...")
    draws_processed = 0
    
    with open(CSV_FILE, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        
        with open(RAW_LAKE, 'w', encoding='utf-8') as out_f:
            for row in reader:
                try:
                    # Strip spaces from keys
                    row = {str(k).strip(): str(v).strip() for k, v in row.items() if k is not None}
                    
                    draw_date = row.get('Draw Date', 'Unknown')
                    winning_numbers_str = row.get('Winning Numbers', '')
                    
                    # Mega Millions provides the numbers as a single space-separated string (e.g. "04 26 42 50 60")
                    number_list = [int(n) for n in winning_numbers_str.split()]
                    
                    # The Mega Ball (Bonus) is its own column
                    mega_ball = int(row.get('Mega Ball', 0))
                    
                    # Ensure the data is clean (5 standard balls)
                    if len(number_list) != 5:
                        continue
                        
                    entry = {
                        "draw_id": draws_processed,
                        "draw_date": draw_date,
                        "draw_numbers": sorted(number_list),
                        "bonus_ball": mega_ball
                    }
                    out_f.write(json.dumps(entry) + "\n")
                    draws_processed += 1
                    
                except (ValueError, KeyError, AttributeError):
                    continue

    if draws_processed > 0:
        print(f"[*] N1_Lotto Raw Lake built successfully. {draws_processed} authentic historical draws ingested.")
    else:
        print("[-] Error: Found the CSV, but couldn't parse the row data.")

if __name__ == "__main__":
    os.makedirs("../lake", exist_ok=True)
    build_lake()