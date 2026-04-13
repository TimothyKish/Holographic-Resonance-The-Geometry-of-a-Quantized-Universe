# vol5/T-Series/T1_Biological/scripts/scalarize.py
import json
import os
import math

PROMOTED_LAKE = "../lake/biological_promoted.jsonl"
SCALAR_LAKE = "../lake/biological_scalar.jsonl"

def scalarize():
    print("===============================================================")
    print(" 🧬 SCALARIZING T1 BIOLOGICAL (Spellman α + cdc15)")
    print("===============================================================")

    if not os.path.exists(PROMOTED_LAKE):
        raise FileNotFoundError(f"Promoted lake not found: {PROMOTED_LAKE}")

    with open(PROMOTED_LAKE, encoding="utf-8") as f_in, \
         open(SCALAR_LAKE, "w", encoding="utf-8") as f_out:

        for line in f_in:
            row = json.loads(line)

            mid_time = 0.5 * (row["from_time_min"] + row["to_time_min"])
            duration = row["interval_min"]

            scalar = {
                "lake_id": row["lake_id"],
                "series": row["series"],
                "t_mid_min": mid_time,
                "dt_min": duration,
                "log_dt": math.log(duration) if duration > 0 else None,
                "meta": row["meta"],
            }

            f_out.write(json.dumps(scalar) + "\n")

    print(f"[*] T1 Biological scalar lake → {SCALAR_LAKE}")


if __name__ == "__main__":
    scalarize()
