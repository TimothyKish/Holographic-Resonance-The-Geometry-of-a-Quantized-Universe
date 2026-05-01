# vol5/Q-Series/Q1_Spectra/scripts/build_lake.py
import urllib.request
import urllib.parse
import csv
import json
import os
import socket
import time
from io import StringIO

# Resilient connection settings
socket.setdefaulttimeout(45)

# Sovereign Data Source: NIST Atomic Spectra Database (API/CSV endpoint)
BASE_URL = "https://physics.nist.gov/cgi-bin/ASD/lines1.pl"

RAW_LAKE = "../lake/q1_spectra_raw.jsonl"

def fetch_nist_spectra(element_query):
    print(f"[*] Querying NIST ASD for Sovereign Quantum Data: {element_query}...")
    
    params = {
        'spectra': element_query,
        'limits_type': '0',
        'low_w': '',
        'upp_w': '',
        'unit': '1',
        'de': '0',
        'format': '2',
        'line_out': '0',
        'en_unit': '0',
        'output': '0',
        'bibrefs': '1',
        'show_obs_wl': '1',
        'show_calc_wl': '1',
        'unc_out': '1',
        'order_out': '0',
        'max_low_enrg': '',
        'show_av': '2',
        'max_upp_enrg': '',
        'tsb_value': '0',
        'min_str': '',
        'A_out': '0',
        'intens_out': 'on',
        'max_str': '',
        'allowed_out': '1',
        'forbid_out': '1',
        'min_accur': '',
        'min_intens': '',
        'conf_out': 'on',
        'term_out': 'on',
        'enrg_out': 'on',
        'J_out': 'on'
    }
    
    query_string = urllib.parse.urlencode(params)
    url = f"{BASE_URL}?{query_string}"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Application/Science'})
    
    for attempt in range(3):
        try:
            print(f"    -> Connection attempt {attempt + 1} of 3...")
            with urllib.request.urlopen(req) as response:
                data = response.read().decode('ISO-8859-1') 
                if "<!DOCTYPE html" in data[:50].lower() or "<html" in data[:50].lower():
                    print(f"    [-] Server returned an HTML error instead of CSV.")
                    return None
                print(f"    [+] Sovereign download complete for {element_query}.")
                return data
        except Exception as e:
            print(f"    [-] Attempt {attempt + 1} failed: {e}")
            time.sleep(5)
            
    return None

def build_lake():
    print("===============================================================")
    print(" ⚛️ INITIALIZING Q1_SPECTRA (Empirical Quantum Geometry)")
    print("===============================================================")
    
    targets = ["H I", "He I", "He II"]
    os.makedirs("../lake", exist_ok=True)
    records_processed = 0
    
    with open(RAW_LAKE, 'w', encoding='utf-8') as out_f:
        for target in targets:
            csv_data = fetch_nist_spectra(target)
            if not csv_data:
                continue
            
            f_stream = StringIO(csv_data)
            reader = csv.DictReader(f_stream)
            
            for row in reader:
                try:
                    clean_row = {}
                    for k, v in row.items():
                        if not k: 
                            continue
                        clean_k = k.strip()
                        # Aggressively strip NIST's Excel traps (="...") and theoretical brackets [] ()
                        clean_v = v.replace('=', '').replace('"', '').replace('[', '').replace(']', '').replace('(', '').replace(')', '').strip()
                        clean_row[clean_k] = clean_v
                    
                    # Extract the wavelength (Fallback to Ritz calculated wavelength if observed is missing)
                    obs_wl = clean_row.get('obs_wl_vac(nm)', '')
                    ritz_wl = clean_row.get('ritz_wl_vac(nm)', '')
                    wl = obs_wl if obs_wl else ritz_wl
                    
                    # Extract energy levels
                    lower_energy = clean_row.get('Ei(cm-1)', '')
                    upper_energy = clean_row.get('Ek(cm-1)', '')
                    
                    # Skip if we don't have a wavelength and both energy levels
                    if not wl or not lower_energy or not upper_energy or wl.startswith('---'):
                        continue
                        
                    entry = {
                        "entity_id": f"NIST_{target.replace(' ', '')}_{records_processed:05d}",
                        "domain": "quantum",
                        "element": target,
                        "wavelength_nm": float(wl),
                        "lower_energy_cm1": float(lower_energy),
                        "upper_energy_cm1": float(upper_energy),
                        "raw_nist_dump": clean_row
                    }
                    
                    out_f.write(json.dumps(entry) + "\n")
                    records_processed += 1
                    
                except Exception as e:
                    # Ignore rows that have non-float text like "AAA" in the wavelength/energy columns
                    continue

    print(f"\n[*] Q1_Spectra Raw Lake built successfully. {records_processed} quantum energy states ingested.")

if __name__ == "__main__":
    build_lake()