#!/usr/bin/env python
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = ROOT / "lakes" / "inputs"
PROMOTED_DIR = ROOT / "lakes" / "inputs_promoted"

BIO_LAKES = ["b1_chirality", "b2_codon", "b3_amino"]

def extract_kish_scalar(raw_entry):
    """
    MODIFY THIS LINE depending on where the Kish scalar lives.
    For example, if your raw Biology entries look like:
        { "kish_scalar": 0.247, ... }
    then return raw_entry["kish_scalar"].
    """
    return raw_entry.get("kish_scalar")  # <-- adjust if needed

def main():
    for lake in BIO_LAKES:
        src = INPUT_DIR / f"{lake}.jsonl"
        dst = PROMOTED_DIR / f"{lake}_promoted.jsonl"

        if not src.exists():
            print(f"[SKIP] Missing raw Biology lake: {src}")
            continue

        print(f"[PROMOTE BIOLOGY] {lake}: {src} -> {dst}")

        with open(src, "r", encoding="utf-8") as fin, \
             open(dst, "w", encoding="utf-8") as fout:

            for idx, line in enumerate(fin):
                line = line.strip()
                if not line:
                    continue

                raw = json.loads(line)

                # Extract Kish scalar
                ks = extract_kish_scalar(raw)
                if ks is None:
                    print(f"[WARN] No Kish scalar found in {lake} line {idx+1}")
                    continue

                # Wrap into V5 promoted entry
                promoted = {
                    "entity_id": f"{lake.upper()}_{idx+1:06d}",
                    "domain": "biology",
                    "volume": 5,
                    "lake_id": lake,
                    "geometry_payload": {
                        "coordinates": [],
                        "dimensionality": 0,
                        "geometry_type": "unknown"
                    },
                    "scalar_kls": 0.0,
                    "scalar_klc": 0.0,
                    "meta": {
                        "source": "vol5_biology_invariant_promotion",
                        "ingest_timestamp": "2026-03-13T00:00:00Z",
                        "sovereign": True
                    },
                    "_raw_payload": {
                        **raw,
                        "scalar_invariant": ks
                    }
                }

                fout.write(json.dumps(promoted) + "\n")

        print(f"[DONE] Biology lake promoted with invariants: {dst}")

if __name__ == "__main__":
    main()
