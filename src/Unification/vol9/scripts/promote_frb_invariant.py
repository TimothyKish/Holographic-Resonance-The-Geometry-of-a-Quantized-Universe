# ==============================================================================
# SCRIPT: promote_frb_invariant.py
# TARGET: Extract FRB signature coefficients and compute scalar invariant
# AUTHORS: Timothy John Kish & Phoenix Aurora
# LICENSE: Sovereign Protected / KishLattice 16pi Initiative Copyright 2026
# ==============================================================================
#!/usr/bin/env python
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "lakes" / "inputs_promoted" / "frb_master_promoted.jsonl"
OUTPUT_PATH = ROOT / "lakes" / "inputs_promoted" / "frb_master_promoted_with_invariant.jsonl"

FLOAT_RE = re.compile(r"\(([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)")

def extract_signature_coeffs(known_signatures):
    coeffs = []
    for sig in known_signatures or []:
        m = FLOAT_RE.search(sig)
        if m:
            try:
                coeffs.append(float(m.group(1)))
            except ValueError:
                pass
    return coeffs

def main():
    if not INPUT_PATH.exists():
        raise SystemExit(f"Input FRB file not found: {INPUT_PATH}")

    print(f"Reading FRBs from: {INPUT_PATH}")
    print(f"Writing updated FRBs to: {OUTPUT_PATH}")

    with INPUT_PATH.open("r", encoding="utf-8") as fin, \
         OUTPUT_PATH.open("w", encoding="utf-8") as fout:

        for line in fin:
            line = line.strip()
            if not line:
                continue

            rec = json.loads(line)
            raw = rec.get("_raw_payload", rec)  # tolerate raw-only form

            known_signatures = raw.get("known_signatures") or rec.get("known_signatures")
            coeffs = extract_signature_coeffs(known_signatures)

            if coeffs:
                scalar_inv = sum(coeffs) / len(coeffs)
                raw["scalar_invariant"] = scalar_inv

            rec["_raw_payload"] = raw
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print("Done. Now point the pipeline at the new FRB file.")

if __name__ == "__main__":
    main()
