#!/usr/bin/env python3
"""
KISH LATTICE — CHEMISTRY PIPELINE (ChEMBL API + ZINC 3D)
--------------------------------------------------------

v1_sanity_pull.py

Purpose:
    Pull the first page of the ChEMBL molecule API as raw JSON.
    This verifies:
        - API connectivity
        - folder structure
        - JSON validity
        - checksum generation

    This script uses NO API keys and performs NO preprocessing.
    The downloaded JSON is stored exactly as received.

Output:
    lakes/chembl_api_json/page_00001.json
    lakes/chembl_api_json/checksums.sha256
"""

import os
import json
import hashlib
import requests

# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------
BASE = os.path.dirname(os.path.dirname(__file__))  # Lattice_Audit_Chemistry/
CHEMBL_DIR = os.path.join(BASE, "lakes", "chembl_api_json")

os.makedirs(CHEMBL_DIR, exist_ok=True)

# ------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------
FIRST_PAGE_URL = "https://www.ebi.ac.uk/chembl/api/data/molecule.json"
OUTFILE = os.path.join(CHEMBL_DIR, "page_00001.json")
CHECKSUM_FILE = os.path.join(CHEMBL_DIR, "checksums.sha256")

# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------
def sha256_of_file(path):
    """Compute SHA-256 checksum of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def download_json(url, outpath):
    """Download JSON from the ChEMBL API and save it exactly as received."""
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    data = r.json()

    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
def main():
    print("Running v1 sanity pull...")
    print(f"Downloading first ChEMBL API page:\n{FIRST_PAGE_URL}")

    download_json(FIRST_PAGE_URL, OUTFILE)

    print(f"Saved: {OUTFILE}")
    checksum = sha256_of_file(OUTFILE)
    print(f"SHA256: {checksum}")

    # Write checksum file
    with open(CHECKSUM_FILE, "w") as f:
        f.write(f"{checksum}  page_00001.json\n")

    print("v1 sanity pull complete.")


if __name__ == "__main__":
    main()
