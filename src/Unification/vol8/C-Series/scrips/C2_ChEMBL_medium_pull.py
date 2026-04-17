#!/usr/bin/env python3
import os
import json
import hashlib
import requests

BASE = os.path.dirname(os.path.dirname(__file__))
CHEMBL_DIR = os.path.join(BASE, "lakes", "chembl_api_json")
os.makedirs(CHEMBL_DIR, exist_ok=True)

CHECKSUM_FILE = os.path.join(CHEMBL_DIR, "checksums.sha256")

BASE_URL = "https://www.ebi.ac.uk"

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

def normalize_next_url(next_url):
    if not next_url:
        return None
    if next_url.startswith("http"):
        return next_url
    if next_url.startswith("/"):
        return BASE_URL + next_url
    return None

def main():
    print("Running v2 medium pull...")

    url = "https://www.ebi.ac.uk/chembl/api/data/molecule.json"

    with open(CHECKSUM_FILE, "a") as checksum_log:
        for i in range(1, 11):
            outfile = os.path.join(CHEMBL_DIR, f"page_{i:05d}.json")
            print(f"Downloading page {i}...")

            data = download_json(url, outfile)
            checksum = sha256_of_file(outfile)
            checksum_log.write(f"{checksum}  page_{i:05d}.json\n")

            print(f"Saved: {outfile}")
            print(f"SHA256: {checksum}")

            next_url = normalize_next_url(data.get("page_meta", {}).get("next"))
            if not next_url:
                print("Reached end of available pages early.")
                break

            url = next_url

    print("v2 medium pull complete.")

if __name__ == "__main__":
    main()
