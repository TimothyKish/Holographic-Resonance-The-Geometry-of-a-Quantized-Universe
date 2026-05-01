"""
build_lake.py -- T2d_Pacific FIXED
NOAA CO-OPS station 1612340, Honolulu HI
FIX: chunk by MONTH (31-day limit), use hourly_height product
"""
import json, os, urllib.request, urllib.parse, datetime, math, time, calendar

PI = math.pi
K_GEO = 16.0 / PI

RAW_PATH = os.path.join(os.path.dirname(__file__), "..", "lake", "t2d_pacific_raw.jsonl")
os.makedirs(os.path.dirname(RAW_PATH), exist_ok=True)

STATION_ID = "1612340"
STATION_NAME = "Honolulu HI"
OCEAN_BASIN = "Pacific"
DOMAIN = "planetary_pacific"
LAKE_ID = "t2d_pacific"
BASE_URL = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
START_YEAR, END_YEAR = 2014, 2023


def fetch_month(year, month):
    last_day = calendar.monthrange(year, month)[1]
    params = {
        "begin_date": f"{year}{month:02d}01",
        "end_date":   f"{year}{month:02d}{last_day:02d}",
        "station":    STATION_ID,
        "product":    "hourly_height",
        "datum":      "MLLW",
        "time_zone":  "GMT",
        "units":      "metric",
        "format":     "json"
    }
    url = BASE_URL + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=30) as resp:
        data = json.loads(resp.read())
    if "error" in data:
        raise ValueError(str(data["error"]))
    return data.get("data", [])


def compute_intervals(wl):
    vals = []
    for e in wl:
        if e.get("t") and e.get("v"):
            try:
                vals.append((e["t"], float(e["v"])))
            except ValueError:
                continue
    minima = []
    for i in range(1, len(vals) - 1):
        if vals[i][1] < vals[i-1][1] and vals[i][1] < vals[i+1][1]:
            minima.append(vals[i][0])
    intervals = []
    for i in range(1, len(minima)):
        try:
            t1 = datetime.datetime.strptime(minima[i-1], "%Y-%m-%d %H:%M")
            t2 = datetime.datetime.strptime(minima[i],   "%Y-%m-%d %H:%M")
            dt = (t2 - t1).total_seconds() / 3600.0
            if 6.0 <= dt <= 30.0:
                intervals.append((minima[i], dt))
        except ValueError:
            continue
    return intervals


def build():
    print(f"[T2d_Pacific] Fetching NOAA {STATION_ID} ({STATION_NAME})")
    print(f"  monthly chunks | hourly_height | {START_YEAR}-{END_YEAR}")
    print(f"  NOTE: Honolulu is mixed semi-diurnal (open ocean, small tidal range)")
    all_wl = []
    failed = 0
    for year in range(START_YEAR, END_YEAR + 1):
        year_readings = 0
        for month in range(1, 13):
            try:
                chunk = fetch_month(year, month)
                all_wl.extend(chunk)
                year_readings += len(chunk)
                time.sleep(0.2)
            except Exception as e:
                failed += 1
                if failed <= 5:
                    print(f"  WARN {year}-{month:02d}: {e}")
        print(f"  {year}: {year_readings} readings")

    print(f"  Total readings: {len(all_wl)} | Failed months: {failed}")
    intervals = compute_intervals(all_wl)
    print(f"  Tidal intervals extracted: {len(intervals)}")

    records = []
    for i, (t, iv) in enumerate(intervals):
        records.append({
            "id": f"{LAKE_ID}_{i:06d}",
            "timestamp": t,
            "interval_hours": round(iv, 4),
            "station_id": STATION_ID,
            "station_name": STATION_NAME,
            "ocean_basin": OCEAN_BASIN,
            "source": "NOAA_CO-OPS_hourly_height",
            "domain": DOMAIN,
            "lake_id": LAKE_ID,
            "preregistration_doi": "10.5281/zenodo.19702022",
            "prediction": "P18"
        })

    with open(RAW_PATH, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

    print(f"\n[T2d_Pacific] complete — {len(records)} records")
    print(f"  Output: {RAW_PATH}")
    if records:
        ivs = [r["interval_hours"] for r in records]
        print(f"  Interval range: {min(ivs):.2f} - {max(ivs):.2f} hours")


if __name__ == "__main__":
    build()