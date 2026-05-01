"""
build_lake.py -- T2g_Indian FIXED
UHSLC ERDDAP station 174, Cochin India (West Coast / Arabian Sea)
FIX: Swapped invalid station 99 for valid Cochin station 174. 
Proper ERDDAP URL encoding for date comparisons.
"""
import json, os, urllib.request, urllib.parse, datetime, math, time

PI = math.pi
K_GEO = 16.0 / PI

RAW_PATH = os.path.join(os.path.dirname(__file__), "..", "lake", "t2g_indian_raw.jsonl")
os.makedirs(os.path.dirname(RAW_PATH), exist_ok=True)

# Updated to Cochin, India (UHSLC ID: 174)
STATION_NUM = 174
STATION_NAME = "Cochin India"
OCEAN_BASIN = "Indian Ocean"
DOMAIN = "planetary_indian"
LAKE_ID = "t2g_indian"
BASE_URL = "https://uhslc.soest.hawaii.edu/erddap/tabledap/global_hourly_fast.csv"
START_YEAR, END_YEAR = 2014, 2023

def fetch_year(year):
    # ERDDAP requires URL encoded >, < operators (%3E, %3C)
    start_time = f"{year}-01-01T00:00:00Z"
    end_time = f"{year}-12-31T23:59:59Z"
    
    query = f"time,sea_level&uhslc_id={STATION_NUM}&time%3E={start_time}&time%3C={end_time}"
    url = f"{BASE_URL}?{query}"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        data = response.read().decode('utf-8')
        
    lines = data.strip().split('\n')
    readings = []
    
    # Skip line 0 (headers) and line 1 (units)
    for line in lines[2:]:
        if not line.strip(): continue
        parts = line.split(',')
        if len(parts) >= 2 and parts[1].strip() != 'NaN':
            try:
                ts = parts[0].strip('Z')
                val = float(parts[1])
                dt = datetime.datetime.fromisoformat(ts)
                readings.append({"t": dt, "v": val})
            except ValueError:
                pass
    return readings

def compute_intervals(readings):
    readings.sort(key=lambda x: x["t"])
    intervals = []
    highs = []
    
    # Identify local maxima (high tides)
    for i in range(1, len(readings) - 1):
        if readings[i]["v"] > readings[i-1]["v"] and readings[i]["v"] > readings[i+1]["v"]:
            highs.append(readings[i])
            
    for i in range(1, len(highs)):
        dt = highs[i]["t"] - highs[i-1]["t"]
        hours = dt.total_seconds() / 3600.0
        # Roughly 10-28 hour filter for tides
        if 10.0 <= hours <= 28.0:
            ts_str = highs[i]["t"].strftime("%Y-%m-%d %H:%M")
            intervals.append((ts_str, hours))
            
    return intervals

if __name__ == "__main__":
    print(f"Building {LAKE_ID} from UHSLC ERDDAP (Cochin 174)...")
    
    all_wl = []
    failed = 0
    
    for year in range(START_YEAR, END_YEAR + 1):
        try:
            chunk = fetch_year(year)
            all_wl.extend(chunk)
            print(f"  {year}: {len(chunk)} readings")
            time.sleep(0.5) # Polite API pacing
        except Exception as e:
            failed += 1
            print(f"  WARN {year}: {e}")
            
    print(f"  Total readings fetched: {len(all_wl)} | Failed years: {failed}")
    
    intervals = compute_intervals(all_wl)
    print(f"  Tidal intervals extracted: {len(intervals)}")
    
    records = []
    for i, (t, iv) in enumerate(intervals):
        records.append({
            "id": f"{LAKE_ID}_{i:06d}",
            "timestamp": t,
            "interval_hours": round(iv, 4),
            "station_number": 174,
            "station_name": "Cochin India",
            "ocean_basin": "Indian",
            "source": "UHSLC_global_hourly_fast",
            "domain": "planetary_indian",
            "lake_id": "t2g_india",
            "preregistration_doi": "10.5281/zenodo.19702022",
            "prediction": "P18"
        })
        
    with open(RAW_PATH, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
            
    print(f"Wrote {len(records)} records to {RAW_PATH}")