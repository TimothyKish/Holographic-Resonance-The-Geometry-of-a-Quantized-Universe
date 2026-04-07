#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
C3.1.1 — SMILES-Deduplicated Manifest Builder
---------------------------------------------
Reads the raw ZINC20 manifest (possibly containing multiple entries
per ZINC ID or multiple entries with identical SMILES) and produces
a sovereign, geometry-first manifest with exactly one entry per
unique SMILES string.

Outputs:
  ../lakes/zinc_3d_manifest/zinc20_manifest_unique_smiles.jsonl
  ../lakes/zinc_3d_manifest/duplicates_removed.log
"""

import json
import os

RAW_MANIFEST = "../lakes/zinc_3d_manifest/zinc20_manifest.jsonl"
DEDUP_MANIFEST = "../lakes/zinc_3d_manifest/zinc20_manifest_unique_smiles.jsonl"
DUP_LOG = "../lakes/zinc_3d_manifest/duplicates_removed.log"

os.makedirs(os.path.dirname(DEDUP_MANIFEST), exist_ok=True)

def run_dedup():
    print("=== C3.1.1 SMILES Deduplication ===")

    seen = set()
    kept = 0
    removed = 0

    out_f = open(DEDUP_MANIFEST, "w", encoding="utf-8")
    dup_f = open(DUP_LOG, "w", encoding="utf-8")

    with open(RAW_MANIFEST, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            smiles = entry["smiles"]

            if smiles not in seen:
                seen.add(smiles)
                out_f.write(json.dumps(entry) + "\n")
                kept += 1
            else:
                dup_f.write(f"{entry['zinc_id']}\t{smiles}\t{entry.get('tranche_name','UNKNOWN')}\n")
                removed += 1

    out_f.close()
    dup_f.close()

    print(f"Unique SMILES kept: {kept}")
    print(f"Duplicates removed: {removed}")
    print(f"Output written to: {DEDUP_MANIFEST}")
    print("=== COMPLETE ===")

if __name__ == "__main__":
    run_dedup()
