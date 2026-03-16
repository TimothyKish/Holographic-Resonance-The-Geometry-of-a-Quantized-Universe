# vol5/T-Series/T2_Planetary/scripts/promote.py
import json

def promote_to_v5_schema():
    print("[*] Promoting T2_Planetary to strict Vol5 Schema...")

    promoted = []

    with open("../lake/planetary_real_raw.jsonl", "r") as f:
        for idx, line in enumerate(f):
            raw_data = json.loads(line)

            v5_entry = {
                "id": f"T2_{str(idx).zfill(6)}",
                "domain": "T2_Planetary",
                "raw_payload": raw_data,
                "geometry_payload": {},
                "scalar_invariant": None,
                "meta": {
                    "source": "NOAA CO-OPS — High/Low Tide Predictions (GMT)",
                    "notes": "Planetary temporal domain — high/low tide intervals at station 9414290 (San Francisco, CA)"
                }
            }

            promoted.append(v5_entry)

    with open("../lake/planetary_real.jsonl", "w") as f:
        for entry in promoted:
            f.write(json.dumps(entry) + "\n")

    print("[*] Promotion complete. Vol5 Schema applied.")

if __name__ == "__main__":
    promote_to_v5_schema()
