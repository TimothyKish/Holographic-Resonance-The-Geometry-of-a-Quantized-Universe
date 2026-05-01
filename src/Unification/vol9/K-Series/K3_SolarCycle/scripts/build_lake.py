"""
build_lake.py -- K3_SolarCycle: SIDC Solar Cycle Intervals
Lake ID: k3_solar_cycle
Domain: stellar_cycle
Source: SIDC Royal Observatory Belgium, International Sunspot Number
        https://www.sidc.be/SILSO/datafiles

Records: ~300 (annual mean sunspot numbers since 1700)
Scalar: log(interval_years * 365.25 + 1) / log(k_geo)
        Using days as unit, consistent with K-series period lakes

Pre-registration: DOI 10.5281/zenodo.19702022 (Prediction P26)
Prediction P26: Solar cycle intervals cluster at N/pi harmonic register.
Tests whether the 11-year solar cycle encodes the lattice rupture timer.

Build: Timothy John Kish / KishLattice 16pi Initiative LLC / April 2026
"""

import json, os, urllib.request, math, csv, io

PI    = math.pi
K_GEO = 16.0 / PI

RAW_PATH = os.path.join(os.path.dirname(__file__), "..", "lake", "k3_solar_cycle_raw.jsonl")
os.makedirs(os.path.dirname(RAW_PATH), exist_ok=True)

# SIDC annual mean sunspot number (Version 2.0)
SIDC_URL = "https://www.sidc.be/SILSO/DATA/SN_y_tot_V2.0.csv"


def fetch_sidc():
    with urllib.request.urlopen(SIDC_URL, timeout=30) as resp:
        content = resp.read().decode("utf-8")
    rows = []
    for line in content.strip().split("\n"):
        parts = line.strip().split(";")
        if len(parts) >= 2:
            try:
                year = int(float(parts[0].strip()))
                sn   = float(parts[1].strip())
                rows.append((year, sn))
            except ValueError:
                continue
    return rows


def find_cycle_minima(data):
    """
    Find solar cycle minima (years of minimum sunspot number between cycles).
    A minimum is a local minimum that is below a threshold.
    """
    years  = [d[0] for d in data]
    values = [d[1] for d in data]
    minima = []
    window = 3
    for i in range(window, len(values) - window):
        local_min = min(values[i-window:i+window+1])
        if values[i] == local_min and values[i] < 20:
            # Avoid duplicate minima in same cycle
            if not minima or (years[i] - minima[-1][0]) > 3:
                minima.append((years[i], values[i]))
    return minima


def build():
    print("[K3_SolarCycle] Fetching SIDC annual sunspot data...")
    try:
        data = fetch_sidc()
        print(f"  Fetched {len(data)} annual records ({data[0][0]}-{data[-1][0]})")
    except Exception as e:
        print(f"  SIDC fetch failed ({e}). Using embedded fallback data.")
        # Fallback: well-known cycle minima years
        data = None

    records = []

    if data:
        # Primary: use annual sunspot numbers to derive cycle properties
        for year, sn in data:
            records.append({
                "id": f"k3_sunspot_{year}",
                "year": year,
                "sunspot_number_annual_mean": round(sn, 2),
                "measurement_type": "annual_mean",
                "source": "SIDC_SILSO_V2",
                "domain": "stellar_cycle",
                "lake_id": "k3_solar_cycle",
                "preregistration_doi": "10.5281/zenodo.19702022",
                "prediction": "P26"
            })

        # Also compute cycle intervals from minima
        minima = find_cycle_minima(data)
        for i in range(1, len(minima)):
            interval_years = minima[i][0] - minima[i-1][0]
            records.append({
                "id": f"k3_cycle_interval_{minima[i][0]}",
                "year": minima[i][0],
                "cycle_minimum_year": minima[i][0],
                "previous_minimum_year": minima[i-1][0],
                "interval_years": interval_years,
                "interval_days": round(interval_years * 365.25, 1),
                "minimum_sunspot_number": round(minima[i][1], 2),
                "measurement_type": "cycle_interval",
                "source": "SIDC_SILSO_V2_derived",
                "domain": "stellar_cycle",
                "lake_id": "k3_solar_cycle",
                "preregistration_doi": "10.5281/zenodo.19702022",
                "prediction": "P26"
            })
    else:
        # Fallback: known cycle minima years from literature
        known_minima = [
            1700, 1712, 1723, 1734, 1745, 1755, 1766, 1775, 1784, 1798,
            1810, 1823, 1833, 1843, 1856, 1867, 1878, 1889, 1901, 1913,
            1923, 1933, 1944, 1954, 1964, 1976, 1986, 1996, 2008, 2019
        ]
        for i in range(1, len(known_minima)):
            iv = known_minima[i] - known_minima[i-1]
            records.append({
                "id": f"k3_cycle_interval_{known_minima[i]}",
                "year": known_minima[i],
                "interval_years": iv,
                "interval_days": round(iv * 365.25, 1),
                "measurement_type": "cycle_interval",
                "source": "SIDC_fallback_literature",
                "domain": "stellar_cycle",
                "lake_id": "k3_solar_cycle",
                "preregistration_doi": "10.5281/zenodo.19702022",
                "prediction": "P26"
            })

    with open(RAW_PATH, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

    print(f"[K3_SolarCycle] build_lake complete")
    print(f"  Records: {len(records)}")
    print(f"  Output:  {RAW_PATH}")
    print(f"  Note: Two record types — annual means (for distribution) and")
    print(f"        cycle intervals (for P26 harmonic test)")


if __name__ == "__main__":
    build()