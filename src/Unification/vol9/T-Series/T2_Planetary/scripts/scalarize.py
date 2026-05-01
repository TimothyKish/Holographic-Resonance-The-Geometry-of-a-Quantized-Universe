# vol5/T-Series/T2_Planetary/scripts/scalarize.py
import json

def scalarize_real_lake():
    print("[*] Scalarizing T2_Planetary (Planetary Temporal Geometry)...")

    scalarized = []

    with open("../lake/planetary_real.jsonl", "r") as f:
        for line in f:
            entry = json.loads(line)

            # Placeholder invariants — real geometry comes later
            entry["scalar_invariant"] = None
            entry["scalar_kls"] = None
            entry["scalar_klc"] = None

            scalarized.append(entry)

    with open("../lake/planetary_real_scalarized.jsonl", "w") as f:
        for entry in scalarized:
            f.write(json.dumps(entry) + "\n")

    print("[*] Scalarization complete (placeholder).")

if __name__ == "__main__":
    scalarize_real_lake()
