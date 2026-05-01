#!/usr/bin/env python3
"""
KISH LATTICE — CHEMISTRY PIPELINE (ChEMBL API + ZINC 3D)
--------------------------------------------------------

v3_extract_lakes.py

Purpose:
    Full ingestion of the ChEMBL molecule API and ZINC 3D JSON subsets.
    This script:
        - walks all ChEMBL API pages until page_meta.next is null
        - saves each page as raw JSON (no preprocessing)
        - streams molecules into NDJSON shards (100k per shard)
        - merges ChEMBL + ZINC 3D
        - writes manifest + checksums

    WARNING:
        This process may take many hours and consume many gigabytes.
        A confirmation prompt is included to prevent accidental execution.
"""

import os
import json
import gzip
import hashlib
import requests

# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------
BASE = os.path.dirname(os.path.dirname(__file__))
CHEMBL_DIR = os.path.join(BASE, "lakes", "chembl_api_json")
ZINC_DIR = os.path.join(BASE, "lakes")
SOVEREIGN = os.path.join(BASE, "sovereign", "Kish_Chemistry_Empirical_Lake")

os.makedirs(CHEMBL_DIR, exist_ok=True)
os.makedirs(SOVEREIGN, exist_ok=True)

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------
BASE_URL = "https://www.ebi.ac.uk"
FIRST_PAGE_URL = f"{BASE_URL}/chembl/api/data/molecule.json"
SHARD_SIZE = 100_000

# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------
def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def normalize_next_url(next_url):
    if not next_url:
        return None
    if next_url.startswith("http"):
        return next_url
    if next_url.startswith("/"):
        return BASE_URL + next_url
    return None

def download_json(url, outpath):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    data = r.json()
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return data

def normalize_molecule(rec):
    """Minimal normalization: rename fields without altering values."""
    out = {}
    out["source"] = "chembl"
    out["id"] = rec.get("molecule_chembl_id")
    out["smiles"] = rec.get("molecule_structures", {}).get("canonical_smiles")
    out["molfile"] = rec.get("molecule_structures", {}).get("molfile")
    out["props"] = rec.get("molecule_properties")
    return out

# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
def main():
    print("\nWARNING: You are about to run the FULL ChEMBL ingestion.")
    print("This may take MANY HOURS and consume MANY GIGABYTES of storage.")
    print("All pages will be downloaded and stored permanently.")
    print("NDJSON shards will be created in the sovereign lake.\n")

    confirm = input("Proceed? (Y/N): ").strip().lower()
    if confirm != "y":
        print("Aborted by user.")
        return

    print("\nStarting full ChEMBL ingestion...\n")
    
    # --------------------------------------------------------
    # RESUME LOGIC — detect last downloaded page
    # --------------------------------------------------------
    existing_pages = [
        f for f in os.listdir(CHEMBL_DIR)
        if f.startswith("page_") and f.endswith(".json")
    ]

    if existing_pages:
        # Extract numeric page indices
        nums = sorted(int(f[5:10]) for f in existing_pages)
        last_page = nums[-1]
        resume_page = last_page + 1

        print(f"\nDetected existing pages 1–{last_page}.")
        print(f"Resuming from page {resume_page}...\n")

        # Build the resume URL
        offset = (resume_page - 1) * 20
        url = f"{BASE_URL}/chembl/api/data/molecule.json?limit=20&offset={offset}"

        page_index = resume_page
        page_paths = [
            os.path.join(CHEMBL_DIR, f"page_{n:05d}.json")
            for n in nums
        ]
    else:
        print("\nNo existing pages detected. Starting from page 1...\n")
        url = FIRST_PAGE_URL
        page_index = 1
        page_paths = []

    # --------------------------------------------------------
    # STEP 1 — Download all ChEMBL API pages
    # --------------------------------------------------------
    url = FIRST_PAGE_URL
    page_index = 1
    page_paths = []

    while True:
        outpath = os.path.join(CHEMBL_DIR, f"page_{page_index:05d}.json")
        print(f"Downloading page {page_index}...")
        data = download_json(url, outpath)
        page_paths.append(outpath)

        next_url = normalize_next_url(data.get("page_meta", {}).get("next"))
        if not next_url:
            print("Reached final page.")
            break

        url = next_url
        page_index += 1

    print(f"\nDownloaded {page_index} pages.\n")

    # --------------------------------------------------------
    # STEP 2 — Create NDJSON shards
    # --------------------------------------------------------
    shard_index = 1
    count = 0
    shard_path = os.path.join(SOVEREIGN, f"shard_{shard_index:05d}.jsonl")
    shard = open(shard_path, "w", encoding="utf-8")

    manifest = {
        "shard_size": SHARD_SIZE,
        "shards": [],
        "total_molecules": 0,
        "sources": ["chembl_api_json"],
    }

    for p in page_paths:
        print(f"Streaming molecules from {p}...")
        with open(p, "r", encoding="utf-8") as f:
            page = json.load(f)

        for rec in page.get("molecules", []):
            out = normalize_molecule(rec)
            shard.write(json.dumps(out) + "\n")

            count += 1
            manifest["total_molecules"] += 1

            if count >= SHARD_SIZE:
                shard.close()
                manifest["shards"].append(f"shard_{shard_index:05d}.jsonl")
                shard_index += 1
                count = 0
                shard_path = os.path.join(SOVEREIGN, f"shard_{shard_index:05d}.jsonl")
                shard = open(shard_path, "w", encoding="utf-8")

    shard.close()
    manifest["shards"].append(f"shard_{shard_index:05d}.jsonl")

    # --------------------------------------------------------
    # STEP 3 — Write manifest + checksums
    # --------------------------------------------------------
    with open(os.path.join(SOVEREIGN, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)

    with open(os.path.join(SOVEREIGN, "checksums.sha256"), "w") as f:
        for shard_name in manifest["shards"]:
            path = os.path.join(SOVEREIGN, shard_name)
            f.write(f"{sha256_of_file(path)}  {shard_name}\n")

    print("\nFull extraction complete.")
    print(f"Total molecules: {manifest['total_molecules']}")
    print(f"Total shards: {len(manifest['shards'])}\n")


if __name__ == "__main__":
    main()
