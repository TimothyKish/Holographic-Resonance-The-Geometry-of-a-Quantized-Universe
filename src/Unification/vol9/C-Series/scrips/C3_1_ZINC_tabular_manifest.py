#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
C3.1 — ZINC20 3D Tranche Crawler + Manifest Builder
Correct traversal using real ZINC20 structure:
- Level 1: AA/, AB/, AC/, ...
- Level 2: AAHL/, AALN/, AAMP/, ...
- Level 3: .txt tranche files

Alphabetical sorting for reproducibility.
Downloads .txt files from the directory they appear in.
Stops after 20 successful downloads.
"""

import os
import re
import json
import hashlib
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# -----------------------------
# CONFIGURABLE USER-AGENT FIX
# -----------------------------
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    )
}

# -----------------------------
# FILTERS
# -----------------------------
def is_level1_dir(name):
    return bool(re.match(r"^[A-Z]{2}/$", name))

def is_level2_dir(name):
    return bool(re.match(r"^[A-Z]{4}/$", name))

def is_txt_file(name):
    return name.endswith(".txt") and re.match(r"^[A-Z0-9]", name)


ROOT_URL = "https://files.docking.org/3D/"

# CORRECTED RELATIVE PATHS (relative to scripts/)
RAW_DIR = "../lakes/zinc_3d_raw/"
MANIFEST_PATH = "../lakes/zinc_3d_manifest/zinc20_manifest.jsonl"
CHECKSUM_PATH = "../lakes/zinc_3d_manifest/checksums.sha256"

LIMIT = 150  # hard-coded tranche limit


# Ensure directories exist
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(os.path.dirname(MANIFEST_PATH), exist_ok=True)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_html(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code != 200:
            print(f"[ERR] HTTP {r.status_code} for {url}")
            return None
        return BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print(f"[ERR] Failed to fetch {url} — {e}")
        return None


def list_directory(url):
    soup = fetch_html(url)
    if soup is None:
        return []

    entries = []
    for a in soup.find_all("a"):
        name = a.text.strip()
        href = a.get("href")
        if not href:
            continue
        entries.append((name, href))

    return entries


def download_txt(url, local_path):
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code != 200:
            print(f"[ERR] HTTP {r.status_code} for {url}")
            return False

        with open(local_path, "wb") as f:
            f.write(r.content)

        return True

    except Exception as e:
        print(f"[ERR] Download failed: {url} — {e}")
        return False


def parse_txt_to_json(txt_path, tranche_name):
    entries = []
    try:
        with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
            header = f.readline().strip().split("\t")
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) != len(header):
                    continue
                row = dict(zip(header, parts))

                entry = {
                    "zinc_id": int(row.get("zinc_id", 0)),
                    "smiles": row.get("smiles"),
                    "inchikey": row.get("inchikey"),
                    "files_db2": row.get("files_db2"),
                    "net_charge": int(row.get("net_charge", 0)),
                    "substance_mwt": float(row.get("substance_mwt", 0)),
                    "substance_logp": float(row.get("substance_logp", 0)),
                    "purchasable": int(row.get("purchasable", 0)),
                    "reactive": int(row.get("reactive", 0)),
                    "features": row.get("features"),
                    "tranche_name": tranche_name
                }
                entries.append(entry)

    except Exception as e:
        print(f"[ERR] Failed to parse {txt_path} — {e}")

    return entries


def crawl():
    print("=== C3.1 ZINC20 Tranche Crawler ===")

    # Overwrite manifest + checksum
    open(MANIFEST_PATH, "w").close()
    open(CHECKSUM_PATH, "w").close()

    manifest_f = open(MANIFEST_PATH, "a", encoding="utf-8")
    checksum_f = open(CHECKSUM_PATH, "a", encoding="utf-8")

    processed = 0

    # -----------------------------
    # LEVEL 1 — two-letter dirs
    # -----------------------------
    level1 = sorted([e for e in list_directory(ROOT_URL) if is_level1_dir(e[0])])

    for name1, href1 in level1:
        url1 = urljoin(ROOT_URL, href1)

        # -----------------------------
        # LEVEL 2 — four-letter dirs
        # -----------------------------
        level2 = sorted([e for e in list_directory(url1) if is_level2_dir(e[0])])

        for name2, href2 in level2:
            url2 = urljoin(url1, href2)

            # -----------------------------
            # LEVEL 3 — .txt files
            # -----------------------------
            files = sorted([e for e in list_directory(url2) if is_txt_file(e[0])])

            for filename, href3 in files:

                print(f"[{processed+1}/{LIMIT}] Processing tranche: {filename}")

                download_url = urljoin(url2, filename)
                local_path = os.path.join(RAW_DIR, filename)

                ok = download_txt(download_url, local_path)
                if not ok:
                    print(f"[SKIP] Could not download {filename}")
                    continue

                file_hash = sha256_file(local_path)
                checksum_f.write(f"{file_hash}  {filename}\n")

                entries = parse_txt_to_json(local_path, filename.replace(".txt", ""))
                for e in entries:
                    manifest_f.write(json.dumps(e) + "\n")

                processed += 1

                if processed >= LIMIT:
                    print(f"=== C3.1 COMPLETE ({LIMIT} tranche files) ===")

                    manifest_f.close()
                    checksum_f.close()
                    return

    print(f"=== C3.1 COMPLETE (fewer than {LIMIT} tranche files found) ===")
    manifest_f.close()
    checksum_f.close()


if __name__ == "__main__":
    crawl()
