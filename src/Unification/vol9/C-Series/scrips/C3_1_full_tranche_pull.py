#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
C3.1 — Full Tranche Pull (Unlimited Ingestion)
----------------------------------------------
Reads ALL ZINC20 tranche .txt files in the tranche directory and produces a
unified sovereign manifest for geometry generation.

Input:
  ../lakes/zinc20_tranches/*.txt

Output:
  ../lakes/zinc20_manifest/zinc20_manifest.jsonl

Each line in the output contains:
  {
    "zinc_id": "...",
    "smiles": "...",
    "tranche": "...",
    "source_file": "..."
  }
"""

import os
import json

TRANCHE_DIR = "../lakes/zinc_3d_raw/"
MANIFEST_DIR = "../lakes/zinc20_manifest/"
MANIFEST_PATH = os.path.join(MANIFEST_DIR, "zinc20_manifest.jsonl")

os.makedirs(MANIFEST_DIR, exist_ok=True)


def parse_tranche_line(line):
    """
    Expected format per ZINC20 tranche line:
      SMILES<TAB>ZINC_ID<TAB>...other fields...
    We only need SMILES and ZINC_ID.
    """
    parts = line.strip().split()
    if len(parts) < 2:
        return None, None
    smiles = parts[0]
    zinc_id = parts[1]
    return smiles, zinc_id


def build_manifest():
    print("=== C3.1 Full Tranche Pull ===")

    tranche_files = sorted(
        f for f in os.listdir(TRANCHE_DIR)
        if f.endswith(".txt")
    )

    total = 0

    with open(MANIFEST_PATH, "w", encoding="utf-8") as out:
        for fname in tranche_files:
            path = os.path.join(TRANCHE_DIR, fname)
            tranche_name = fname.replace(".txt", "")

            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    smiles, zinc_id = parse_tranche_line(line)
                    if not smiles or not zinc_id:
                        continue

                    rec = {
                        "zinc_id": zinc_id,
                        "smiles": smiles,
                        "tranche": tranche_name,
                        "source_file": fname
                    }

                    out.write(json.dumps(rec) + "\n")
                    total += 1

    print(f"=== C3.1 COMPLETE — {total} molecules written to manifest ===")


if __name__ == "__main__":
    build_manifest()
