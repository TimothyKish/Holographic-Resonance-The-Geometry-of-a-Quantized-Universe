#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
C3.2 — ZINC20 Geometry Extractor
Reads the C3.1 manifest, downloads corresponding .db2.gz geometry files,
extracts coordinates, and writes a sovereign geometry JSONL lake.

Directory structure (relative to scripts/):
  ../lakes/zinc_3d_raw/                — tranche .txt files (C3.1)
  ../lakes/zinc_3d_manifest/           — manifest + checksums (C3.1)
  ../lakes/zinc_3d_geom/               — raw .db2.gz geometry files (C3.2)
  ../lakes/zinc_3d_geom_jsonl/         — extracted geometry JSONL (C3.2)
  ../lakes/zinc_3d_geom_manifest/      — audit trail (C3.2)

Author: Timothy
Volume 3 — Lattice Audit Chemistry
"""

import os
import re
import json
import gzip
import hashlib
import requests
from urllib.parse import urljoin

# -----------------------------
# USER-AGENT FIX
# -----------------------------
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    )
}

# -----------------------------
# PATHS (relative to scripts/)
# -----------------------------
MANIFEST_PATH = "../lakes/zinc_3d_manifest/zinc20_manifest.jsonl"

GEOM_RAW_DIR = "../lakes/zinc_3d_geom/"
GEOM_JSONL_DIR = "../lakes/zinc_3d_geom_jsonl/"
GEOM_AUDIT_PATH = "../lakes/zinc_3d_geom_manifest/geometry_audit.jsonl"

ROOT_URL = "https://files.docking.org/3D/"

# Ensure directories exist
os.makedirs(GEOM_RAW_DIR, exist_ok=True)
os.makedirs(GEOM_JSONL_DIR, exist_ok=True)
os.makedirs(os.path.dirname(GEOM_AUDIT_PATH), exist_ok=True)


# -----------------------------
# HELPERS
# -----------------------------
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def download_file(url, local_path):
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


def extract_coordinates_from_db2gz(path):
    """
    Minimal DB2.gz parser.
    Extracts coordinates from lines like:
        ATOM x y z element
    Returns a list of atoms with x,y,z,element.
    """
    atoms = []
    try:
        with gzip.open(path, "rt", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if line.startswith("ATOM"):
                    parts = line.strip().split()
                    if len(parts) >= 5:
                        x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                        element = parts[4]
                        atoms.append({
                            "x": x,
                            "y": y,
                            "z": z,
                            "element": element
                        })
    except Exception as e:
        print(f"[ERR] Failed to parse geometry: {path} — {e}")

    return atoms


# -----------------------------
# MAIN GEOMETRY EXTRACTION
# -----------------------------
def run_geometry_extraction():
    print("=== C3.2 ZINC20 Geometry Extractor ===")

    audit_f = open(GEOM_AUDIT_PATH, "w", encoding="utf-8")

    # Read manifest entries
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest_entries = [json.loads(line) for line in f]

    # Deterministic ordering
    manifest_entries.sort(key=lambda e: e["zinc_id"])

    processed = 0

    for entry in manifest_entries:
        zinc_id = entry["zinc_id"]
        db2_rel = entry["files_db2"]  # e.g. "AA/AAHL/AAAAHL.db2.gz"
        tranche = entry["tranche_name"]

        if not db2_rel or not db2_rel.endswith(".db2.gz"):
            continue

        # Construct full URL
        geom_url = urljoin(ROOT_URL, db2_rel)

        # Local raw geometry path
        filename = os.path.basename(db2_rel)
        local_raw = os.path.join(GEOM_RAW_DIR, filename)

        # Local JSONL geometry output
        local_jsonl = os.path.join(GEOM_JSONL_DIR, f"{zinc_id}.jsonl")

        print(f"[{processed+1}] ZINC ID {zinc_id} — {filename}")

        # Download geometry file
        ok = download_file(geom_url, local_raw)
        if not ok:
            print(f"[SKIP] Missing geometry for ZINC {zinc_id}")
            continue

        # Extract coordinates
        atoms = extract_coordinates_from_db2gz(local_raw)
        if not atoms:
            print(f"[SKIP] No atoms found for ZINC {zinc_id}")
            continue

        # Write sovereign geometry JSONL
        geom_record = {
            "zinc_id": zinc_id,
            "tranche": tranche,
            "geometry": atoms,
            "source_db2": filename
        }

        with open(local_jsonl, "w", encoding="utf-8") as out:
            out.write(json.dumps(geom_record) + "\n")

        # Write audit trail
        audit_f.write(json.dumps({
            "zinc_id": zinc_id,
            "db2_file": filename,
            "sha256": sha256_file(local_raw),
            "jsonl_file": f"{zinc_id}.jsonl"
        }) + "\n")

        processed += 1

    audit_f.close()
    print("=== C3.2 COMPLETE ===")


if __name__ == "__main__":
    run_geometry_extraction()
