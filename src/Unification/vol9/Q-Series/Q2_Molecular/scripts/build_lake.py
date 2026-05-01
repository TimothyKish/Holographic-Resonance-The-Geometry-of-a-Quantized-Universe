# vol5/Q-Series/Q2_Molecular/scripts/build_lake.py
import urllib.request
import json
import os
import re
import socket
import time

# Resilient connection settings
socket.setdefaulttimeout(45)

# Sovereign Data Source: NIST CCCBDB
BASE_URL = "https://cccbdb.nist.gov/expgeom2x.asp?casno="
RAW_LAKE = "../lake/q2_molecular_raw.jsonl"

TARGETS = {
    "7732-18-5": {"formula": "H2O", "name": "Water"},
    "124-38-9": {"formula": "CO2", "name": "Carbon Dioxide"},
    "7664-41-7": {"formula": "NH3", "name": "Ammonia"},
    "74-82-8": {"formula": "CH4", "name": "Methane"},
    "7446-09-5": {"formula": "SO2", "name": "Sulfur Dioxide"},
    "10028-15-6": {"formula": "O3", "name": "Ozone"},
    "50-00-0": {"formula": "H2CO", "name": "Formaldehyde"},
    "74-81-7": {"formula": "CH5N", "name": "Methylamine"}
}

def fetch_nist_geometry(cas_number, name):
    print(f"[*] Querying NIST CCCBDB for Experimental Geometry: {name} ({cas_number})...")
    url = f"{BASE_URL}{cas_number}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Application/Science', 'Cookie': 'cccbdb=1'}
    req = urllib.request.Request(url, headers=headers)
    
    for attempt in range(3):
        try:
            print(f"    -> Connection attempt {attempt + 1} of 3...")
            with urllib.request.urlopen(req) as response:
                return response.read().decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"    [-] Attempt {attempt + 1} failed: {e}")
            time.sleep(5)
    return None

def extract_geometry_from_html(html_data):
    """
    Scavenger Parser: Slices rows, strips HTML, and extracts physical values.
    """
    extracted_data = {"bond_lengths_angstroms": [], "bond_angles_degrees": []}
    if not html_data: return extracted_data
    
    # Isolate the data tables
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html_data, re.IGNORECASE | re.DOTALL)
    
    for row in rows:
        cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.IGNORECASE | re.DOTALL)
        if len(cells) >= 2:
            # Strip all HTML tags from the cells to get pure text
            clean_cells = [re.sub(r'<[^>]+>', '', str(c)).strip() for c in cells]
            
            # Look at all cells in this row for valid physical numbers
            for cell in clean_cells:
                # Find the first floating point number in the cell
                num_match = re.search(r'([0-9]{1,3}\.[0-9]{1,5})', cell)
                if num_match:
                    val = float(num_match.group(1))
                    
                    # Logic gates for physical reality
                    if 0.5 < val < 3.5:
                        # It is a bond length (Angstroms)
                        extracted_data["bond_lengths_angstroms"].append(val)
                    elif 50.0 < val <= 180.0:
                        # It is a bond angle (Degrees)
                        extracted_data["bond_angles_degrees"].append(val)

    # Deduplicate the findings (NIST often lists the same value multiple times from different papers)
    extracted_data["bond_lengths_angstroms"] = list(set(extracted_data["bond_lengths_angstroms"]))
    extracted_data["bond_angles_degrees"] = list(set(extracted_data["bond_angles_degrees"]))
    
    return extracted_data

def build_lake():
    print("===============================================================")
    print(" 🔬 INITIALIZING Q2_MOLECULAR (Empirical Atomic Geometry)")
    print("===============================================================")
    
    os.makedirs("../lake", exist_ok=True)
    records_processed = 0
    
    with open(RAW_LAKE, 'w', encoding='utf-8') as out_f:
        for cas, meta in TARGETS.items():
            html_data = fetch_nist_geometry(cas, meta["name"])
            geometry = extract_geometry_from_html(html_data)
            
            print(f"    [*] Extracted Lengths: {geometry['bond_lengths_angstroms']}")
            print(f"    [*] Extracted Angles:  {geometry['bond_angles_degrees']}\n")
            
            feature_id = 0
            
            for length in geometry['bond_lengths_angstroms']:
                entry = {
                    "entity_id": f"CCCBDB_{meta['formula']}_L{feature_id}",
                    "domain": "molecular_geometry",
                    "molecule": meta["name"],
                    "formula": meta["formula"],
                    "cas_number": cas,
                    "measurement_type": "bond_length_angstroms",
                    "value": length
                }
                out_f.write(json.dumps(entry) + "\n")
                records_processed += 1
                feature_id += 1
                
            for angle in geometry['bond_angles_degrees']:
                entry = {
                    "entity_id": f"CCCBDB_{meta['formula']}_A{feature_id}",
                    "domain": "molecular_geometry",
                    "molecule": meta["name"],
                    "formula": meta["formula"],
                    "cas_number": cas,
                    "measurement_type": "bond_angle_degrees",
                    "value": angle
                }
                out_f.write(json.dumps(entry) + "\n")
                records_processed += 1
                feature_id += 1

    print(f"[*] Q2_Molecular Raw Lake built successfully. {records_processed} empirical geometric features ingested.")

if __name__ == "__main__":
    build_lake()