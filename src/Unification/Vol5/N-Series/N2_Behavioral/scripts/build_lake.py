# vol5/N-Series/N2_Finance/scripts/build_lake.py
import json
import csv
import os
import urllib.request
import urllib.error
import time
import socket

# Set a generous global timeout to prevent WinError 10060 drops
socket.setdefaulttimeout(45)

# Sovereign Data Source: FRED (Federal Reserve Economic Data)
URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=SP500"
CSV_FILE = "../lake/sp500_fred_historical.csv"
RAW_LAKE = "../lake/finance_null_raw.jsonl"

def build_lake():
    print("[*] INITIALIZING N2_FINANCE (Authentic Behavioral Chaos)")
    print("[*] Enforcing Sovereign Chain of Custody (Zero Human Intervention)...")
    
    # 1. Sovereign Download with Resilient Retry Logic
    print(f"[*] Pulling official S&P 500 CSV from FRED (stlouisfed.org)...")
    
    # Expanded headers to look like a standard data science pull
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/csv,application/csv',
        'Connection': 'keep-alive'
    }
    
    req = urllib.request.Request(URL, headers=headers)
    
    max_retries = 3
    csv_data = None
    
    for attempt in range(max_retries):
        try:
            print(f"[*] Connection attempt {attempt + 1} of {max_retries}...")
            # Enforce the 45-second timeout on the specific request
            with urllib.request.urlopen(req, timeout=45) as response:
                csv_data = response.read().decode('utf-8')
            break # If successful, break out of the loop!
            
        except Exception as e:
            print(f"[-] Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print("[*] Server lagging. Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print(f"[-] FATAL ERROR: Sovereign pipeline broken after {max_retries} attempts.")
                print("    The FRED server might be temporarily down for maintenance.")
                return

    # Write the securely downloaded data
    with open(CSV_FILE, 'w', encoding='utf-8') as f:
        f.write(csv_data)
    print("[+] Sovereign download complete. Resilient connection established.")

    # 2. Parse the CSV into the Lattice JSONL Schema
    print("[*] Parsing Open Data CSV and building N2_Finance Raw Lake...")
    ticks_processed = 0
    
    with open(CSV_FILE, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        
        with open(RAW_LAKE, 'w', encoding='utf-8') as out_f:
            for row in reader:
                try:
                    date = row.get('DATE', '')
                    price_str = row.get('SP500', '')
                    
                    # FRED inserts a '.' for market holidays. We skip those.
                    if price_str == '.' or not price_str:
                        continue
                        
                    price = float(price_str)
                    
                    entry = {
                        "tick_id": ticks_processed,
                        "trade_date": date,
                        "close_price": round(price, 2)
                    }
                    out_f.write(json.dumps(entry) + "\n")
                    ticks_processed += 1
                except (ValueError, KeyError):
                    continue

    if ticks_processed > 0:
        print(f"[*] N2_Finance Raw Lake built successfully. {ticks_processed} authentic trading days ingested.")
    else:
        print("[-] Error: Found the CSV, but couldn't parse the row data.")

if __name__ == "__main__":
    os.makedirs("../lake", exist_ok=True)
    build_lake()