"""promote.py -- K3_SolarCycle"""
import json, os, sys

RAW_PATH      = os.path.join(os.path.dirname(__file__), "..", "lake", "k3_solar_cycle_raw.jsonl")
PROMOTED_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "lakes",
                              "inputs_promoted", "k3_solar_cycle_promoted.jsonl")
os.makedirs(os.path.dirname(PROMOTED_PATH), exist_ok=True)

def promote():
    records = []; seen = set()
    with open(RAW_PATH, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line.strip())
            if r["id"] in seen:
                print(f"[K3_SolarCycle] WARNING: duplicate id {r['id']}")
            seen.add(r["id"])
            if r.get("domain") != "stellar_cycle":
                print(f"[K3_SolarCycle] WARNING: domain mismatch on {r['id']}")
            r["promoted"] = True; r["lake_version"] = "vol9"
            records.append(r)
    with open(PROMOTED_PATH, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
    print(f"[K3_SolarCycle] promote complete — {len(records)} records")
    print(f"  Output: {PROMOTED_PATH}")

if __name__ == "__main__":
    promote()