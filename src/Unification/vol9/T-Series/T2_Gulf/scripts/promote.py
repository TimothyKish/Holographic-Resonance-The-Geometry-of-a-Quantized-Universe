"""promote.py -- t2c_gulf"""
import json, os, sys

RAW_PATH      = os.path.join(os.path.dirname(__file__), "..", "lake", "t2c_gulf_raw.jsonl")
PROMOTED_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "lakes",
                              "inputs_promoted", "t2c_gulf_promoted.jsonl")
os.makedirs(os.path.dirname(PROMOTED_PATH), exist_ok=True)

def promote():
    records = []; errors = []; seen = set()
    with open(RAW_PATH, encoding="utf-8") as f:
        for i, line in enumerate(f):
            r = json.loads(line.strip())
            iv = r.get("interval_hours", 0)
            if not (6.0 <= iv <= 30.0):
                errors.append(f"row {i+1}: interval_hours={iv} out of range")
            if r["id"] in seen:
                errors.append(f"row {i+1}: duplicate id")
            seen.add(r["id"])
            records.append(r)
    if errors:
        print("[T2c_Gulf] PROMOTE FAILED:"); [print(f"  {e}") for e in errors[:10]]; sys.exit(1)
    with open(PROMOTED_PATH, "w", encoding="utf-8") as f:
        for r in records:
            r["promoted"] = True; r["lake_version"] = "vol9"
            f.write(json.dumps(r) + "\n")
    print(f"[T2c_Gulf] promote complete — {len(records)} records — 0 errors")
    print(f"  Output: {PROMOTED_PATH}")

if __name__ == "__main__":
    promote()