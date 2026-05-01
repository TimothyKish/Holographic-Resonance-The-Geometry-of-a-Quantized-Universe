"""promote.py -- Q8_Ionisation"""
import json, os, sys

RAW_PATH      = os.path.join(os.path.dirname(__file__), "..", "lake", "q8_ionisation_raw.jsonl")
PROMOTED_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "lakes",
                              "inputs_promoted", "q8_ionisation_promoted.jsonl")
os.makedirs(os.path.dirname(PROMOTED_PATH), exist_ok=True)

def promote():
    records = []; seen = set(); errors = []
    with open(RAW_PATH, encoding="utf-8") as f:
        for i, line in enumerate(f):
            r = json.loads(line.strip())
            if r.get("ionisation_energy_eV", 0) <= 0:
                errors.append(f"row {i+1}: IE invalid")
            if r["id"] in seen: errors.append(f"row {i+1}: duplicate")
            seen.add(r["id"])
            r["promoted"] = True; r["lake_version"] = "vol9"
            records.append(r)
    if errors:
        print("[Q8_Ionisation] PROMOTE FAILED:"); [print(f"  {e}") for e in errors]; sys.exit(1)
    if len(records) != 118:
        print(f"[Q8_Ionisation] WARNING: expected 118 elements, got {len(records)}")
    with open(PROMOTED_PATH, "w", encoding="utf-8") as f:
        for r in records: f.write(json.dumps(r) + "\n")
    print(f"[Q8_Ionisation] promote complete — {len(records)} elements — 0 errors")
    print(f"  Output: {PROMOTED_PATH}")

if __name__ == "__main__":
    promote()