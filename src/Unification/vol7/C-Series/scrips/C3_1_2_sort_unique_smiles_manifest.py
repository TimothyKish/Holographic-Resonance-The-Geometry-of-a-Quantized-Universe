#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
C3.1.2 — SMILES-Sorted Manifest Builder
---------------------------------------
Reads the SMILES-deduplicated manifest and produces a new manifest
sorted lexicographically by SMILES. This ensures deterministic,
structure-first ordering for geometry extraction and audit trails.

Inputs:
  ../lakes/zinc_3d_manifest/zinc20_manifest_unique_smiles.jsonl

Outputs:
  ../lakes/zinc_3d_manifest/zinc20_manifest_unique_smiles_sorted.jsonl
"""

import json
import os

DEDUP_MANIFEST = "../lakes/zinc_3d_manifest/zinc20_manifest_unique_smiles.jsonl"
SORTED_MANIFEST = "../lakes/zinc_3d_manifest/zinc20_manifest_unique_smiles_sorted.jsonl"

os.makedirs(os.path.dirname(SORTED_MANIFEST), exist_ok=True)

def run_sort():
    print("=== C3.1.2 SMILES Sorting ===")

    # Load all entries
    entries = []
    with open(DEDUP_MANIFEST, "r", encoding="utf-8") as f:
        for line in f:
            entries.append(json.loads(line))

    # Sort lexicographically by SMILES
    entries.sort(key=lambda e: e["smiles"])

    # Write sorted manifest
    with open(SORTED_MANIFEST, "w", encoding="utf-8") as out:
        for entry in entries:
            out.write(json.dumps(entry) + "\n")

    print(f"Entries sorted: {len(entries)}")
    print(f"Output written to: {SORTED_MANIFEST}")
    print("=== COMPLETE ===")

if __name__ == "__main__":
    run_sort()
