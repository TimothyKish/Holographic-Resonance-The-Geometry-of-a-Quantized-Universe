"""
promote.py -- L1_GWTC
"""
import json, os, sys

RAW_PATH      = os.path.join(os.path.dirname(__file__), "..", "lake", "l1_gwtc_raw.jsonl")
PROMOTED_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "lakes",
                              "inputs_promoted", "l1_gwtc_promoted.jsonl")
os.makedirs(os.path.dirname(PROMOTED_PATH), exist_ok=True)

def promote():
    records = []
    seen = set()
    errors = []
    with open(RAW_PATH, encoding="utf-8") as f:
        for i, line in enumerate(f):
            r = json.loads(line.strip())
            if r.get("f_ring_hz", 0) <= 0:
                errors.append(f"row {i+1}: f_ring_hz invalid")
            if r.get("id") in seen:
                errors.append(f"row {i+1}: duplicate id")
            seen.add(r.get("id"))
            if r.get("domain") != "gravitational_wave":
                errors.append(f"row {i+1}: domain mismatch")
            records.append(r)
    if errors:
        print("[L1_GWTC] PROMOTE FAILED:")
        for e in errors: print(f"  {e}")
        sys.exit(1)
    with open(PROMOTED_PATH, "w", encoding="utf-8") as f:
        for r in records:
            r["promoted"] = True
            r["lake_version"] = "vol9"
            f.write(json.dumps(r) + "\n")
    print(f"[L1_GWTC] promote complete — {len(records)} records — 0 errors")
    print(f"  Output: {PROMOTED_PATH}")

if __name__ == "__main__":
    promote()