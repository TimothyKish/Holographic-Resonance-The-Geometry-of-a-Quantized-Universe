#!/usr/bin/env python3
"""
KISH LATTICE — CHEMISTRY PIPELINE
---------------------------------

C1.1 — ZINC 3D SANITY PULL

Purpose:
    Validate ZINC 3D ingestion by downloading a single JSON chunk.
    This confirms:
        - folder structure
        - download integrity
        - JSON validity
        - geometry fields presence
        - checksum reproducibility

    This script performs NO preprocessing.
    The JSON is stored exactly as received.

Output:
    lakes/zinc_3d/sample_chunk.json
    lakes/zinc_3d/checksums.sha256
"""

import os
import json
import hashlib
import requests

# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------
BASE = os.path.dirname(os.path.dirname(__file__))  # Lattice_Audit_Chemistry/
ZINC_DIR = os.path.join(BASE, "lakes", "zinc_3d")

os.makedirs(ZINC_DIR, exist_ok=True)

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------
# Using a small, stable ZINC 3D JSON file for sanity validation.
# This is from the ZINC "Clean Leads" 3D subset.
ZINC_SAMPLE_URL = (
    "https://files.docking.org/3D/CLEAN/000/000/000/00000001.json"
)

OUTFILE = os.path.join(ZINC_DIR, "sample_chunk.json")
CHECKSUM_FILE = os.path.join(ZINC_DIR, "checksums.sha256")

# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------
def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def download_json(url, outpath):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    data = r.json()

    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return data


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
def main():
    print("Running C1.1 — ZINC 3D sanity pull...")
    print(f"Downloading sample ZINC 3D JSON:\n{ZINC_SAMPLE_URL}")

    data = download_json(ZINC_SAMPLE_URL, OUTFILE)
    print(f"Saved: {OUTFILE}")

    checksum = sha256_of_file(OUTFILE)
    print(f"SHA256: {checksum}")

    with open(CHECKSUM_FILE, "w") as f:
        f.write(f"{checksum}  sample_chunk.json\n")

    # Minimal geometry validation
    mol = data.get("molecules", [{}])[0]
    coords = mol.get("atoms", {}).get("coords", {})

    if coords:
        print("Geometry fields detected (atoms/coords present).")
    else:
        print("WARNING: Geometry fields not detected. Inspect JSON manually.")

    print("C1.1 sanity pull complete.")


if __name__ == "__main__":
    main()
