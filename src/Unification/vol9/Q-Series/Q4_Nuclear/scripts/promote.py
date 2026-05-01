"""promote.py -- Q4_Nuclear"""
import json, os, sys

RAW_PATH      = os.path.join(os.path.dirname(__file__), "..", "lake", "q4_nuclear_raw.jsonl")
PROMOTED_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "lakes",
                              "inputs_promoted", "q4_nuclear_promoted.jsonl")
os.makedirs(os.path.dirname(PROMOTED_PATH), exist_ok=True)

def promote():
    records = []; seen = set(); errors = []
    with open(RAW_PATH, encoding="utf-8") as f:
        for i, line in enumerate(f):
            r = json.loads(line.strip())
            if r.get("binding_energy_mev_per_A", 0) <= 0:
                errors.append(f"row {i+1}: BE/A invalid")
            if r["id"] in seen: errors.append(f"row {i+1}: duplicate")
            seen.add(r["id"])
            r["promoted"] = True; r["lake_version"] = "vol9"
            records.append(r)
    if errors:
        print("[Q4_Nuclear] PROMOTE FAILED:"); [print(f"  {e}") for e in errors[:5]]; sys.exit(1)
    with open(PROMOTED_PATH, "w", encoding="utf-8") as f:
        for r in records: f.write(json.dumps(r) + "\n")
    print(f"[Q4_Nuclear] promote complete — {len(records)} records")
    print(f"  Output: {PROMOTED_PATH}")

if __name__ == "__main__":
    promote()