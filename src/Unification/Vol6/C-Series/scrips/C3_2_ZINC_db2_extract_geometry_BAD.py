#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
C3.2 — ZINC20 DB2 → JSON Geometry Extractor
Single-threaded, skip-bad mode, sovereign extraction.

Reads the C3.1 manifest (NDJSON), downloads each .db2.gz file,
extracts atoms + bonds, and emits JSON objects matching the
chemistry pipeline schema.

Raw DB2 files are preserved unchanged for chain-of-custody.
JSON geometry is written to lakes/zinc_3d_geometry/.

Author: Timothy
Volume 3 — Lattice Audit Chemistry
"""

import os
import json
import gzip
import hashlib
import requests

MANIFEST_PATH = "../../lakes/zinc_3d_manifest/zinc20_manifest.jsonl"
RAW_DB2_DIR = "../../lakes/zinc_3d_db2_raw/"
GEOM_OUT_PATH = "../../lakes/zinc_3d_geometry/zinc20_geometry.jsonl"
CHECKSUM_PATH = "../../lakes/zinc_3d_geometry/checksums.sha256"

# Ensure output directories exist
os.makedirs(RAW_DB2_DIR, exist_ok=True)
os.makedirs(os.path.dirname(GEOM_OUT_PATH), exist_ok=True)


def sha256_file(path):
    """Compute SHA-256 checksum of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def download_db2(db2_url, local_path):
    """Download a DB2 file if not already present."""
    if os.path.exists(local_path):
        print(f"[SKIP] Already downloaded: {local_path}")
        return True

    try:
        print(f"[GET] {db2_url}")
        r = requests.get(db2_url, timeout=20)
        if r.status_code != 200:
            print(f"[ERR] HTTP {r.status_code} for {db2_url}")
            return False

        with open(local_path, "wb") as f:
            f.write(r.content)

        print(f"[OK] Saved: {local_path}")
        return True

    except Exception as e:
        print(f"[ERR] Download failed: {db2_url} — {e}")
        return False


def parse_db2(db2_path):
    """
    Minimal DB2 parser.
    Extracts atoms and bonds from a .db2.gz file.
    DB2 format is line-based; atoms start with 'ATOM', bonds with 'BOND'.
    """

    atoms = []
    bonds = []

    try:
        with gzip.open(db2_path, "rt", encoding="utf-8", errors="ignore") as f:
            for line in f:
                parts = line.strip().split()

                # Atom line example:
                # ATOM  C  0.123  -1.234  2.345
                if parts[0] == "ATOM" and len(parts) >= 5:
                    element = parts[1]
                    x = float(parts[2])
                    y = float(parts[3])
                    z = float(parts[4])
                    atoms.append({"element": element, "x": x, "y": y, "z": z})

                # Bond line example:
                # BOND  0  1  1
                if parts[0] == "BOND" and len(parts) >= 4:
                    i = int(parts[1])
                    j = int(parts[2])
                    order = int(parts[3])
                    bonds.append({"i": i, "j": j, "order": order})

        return atoms, bonds

    except Exception as e:
        print(f"[ERR] Failed to parse DB2: {db2_path} — {e}")
        return None, None


def main():
    print("=== C3.2 ZINC DB2 → JSON Geometry Extractor ===")

    if not os.path.exists(MANIFEST_PATH):
        print(f"[FATAL] Manifest not found: {MANIFEST_PATH}")
        return

    out_f = open(GEOM_OUT_PATH, "w", encoding="utf-8")
    checksum_f = open(CHECKSUM_PATH, "w", encoding="utf-8")

    with open(MANIFEST_PATH, "r", encoding="utf-8") as manifest:
        for line in manifest:
            try:
                entry = json.loads(line)
            except:
                print("[ERR] Bad JSON in manifest, skipping.")
                continue

            zinc_id = entry.get("zinc_id")
            db2_rel = entry.get("files_db2")

            if not db2_rel:
                print(f"[SKIP] No DB2 path for ZINC {zinc_id}")
                continue

            db2_url = f"https://files.docking.org{db2_rel}"
            local_db2 = os.path.join(RAW_DB2_DIR, os.path.basename(db2_rel))

            # Download DB2
            if not download_db2(db2_url, local_db2):
                print(f"[SKIP] Could not fetch DB2 for {zinc_id}")
                continue

            # Parse DB2
            atoms, bonds = parse_db2(local_db2)
            if atoms is None:
                print(f"[SKIP] Parse failed for {zinc_id}")
                continue

            # Build JSON geometry object
            geom_obj = {
                "zinc_id": zinc_id,
                "smiles": entry.get("smiles"),
                "inchikey": entry.get("inchikey"),
                "net_charge": entry.get("net_charge"),
                "substance_mwt": entry.get("substance_mwt"),
                "substance_logp": entry.get("substance_logp"),
                "purchasable": entry.get("purchasable"),
                "reactive": entry.get("reactive"),
                "features": entry.get("features"),
                "tranche_name": entry.get("tranche_name"),
                "atoms": atoms,
                "bonds": bonds
            }

            # Write JSON geometry
            out_f.write(json.dumps(geom_obj) + "\n")

            # Write checksums
            db2_hash = sha256_file(local_db2)
            checksum_f.write(f"{db2_hash}  {os.path.basename(local_db2)}\n")

            print(f"[OK] Extracted geometry for ZINC {zinc_id}")

    out_f.close()
    checksum_f.close()
    print("=== C3.2 COMPLETE ===")


if __name__ == "__main__":
    main()
