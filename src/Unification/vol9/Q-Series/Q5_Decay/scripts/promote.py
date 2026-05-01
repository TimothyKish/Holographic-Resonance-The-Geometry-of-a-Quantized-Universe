"""promote.py -- Q5_Decay"""
import json, os, sys

RAW_PATH      = os.path.join(os.path.dirname(__file__), "..", "lake", "q5_decay_raw.jsonl")
PROMOTED_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "lakes",
                              "inputs_promoted", "q5_decay_promoted.jsonl")
os.makedirs(os.path.dirname(PROMOTED_PATH), exist_ok=True)

def promote():
    records = []; seen = set(); errors = []
    with open(RAW_PATH, encoding="utf-8") as f:
        for i, line in enumerate(f):
            r = json.loads(line.strip())
            if r.get("half_life_seconds", 0) <= 0:
                errors.append(f"row {i+1}: half_life_seconds invalid")
            if r["id"] in seen:
                errors.append(f"row {i+1}: duplicate")
            seen.add(r["id"])
            r["promoted"] = True; r["lake_version"] = "vol9"
            records.append(r)
    if errors:
        print("[Q5_Decay] PROMOTE FAILED:"); [print(f"  {e}") for e in errors[:5]]; sys.exit(1)
    with open(PROMOTED_PATH, "w", encoding="utf-8") as f:
        for r in records: f.write(json.dumps(r) + "\n")
    print(f"[Q5_Decay] promote complete — {len(records)} records — 0 errors")
    print(f"  Output: {PROMOTED_PATH}")

if __name__ == "__main__":
    promote()