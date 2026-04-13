# vol5/T-Series/T1_Biological/scripts/promote.py
import json
import os
from datetime import datetime

RAW_LAKE = "../lake/biological_real_raw.jsonl"
PROMOTED_LAKE = "../lake/biological_promoted.jsonl"

def promote():
    print("===============================================================")
    print(" 🧬 PROMOTING T1 BIOLOGICAL (Spellman α + cdc15)")
    print("===============================================================")

    if not os.path.exists(RAW_LAKE):
        raise FileNotFoundError(f"Raw lake not found: {RAW_LAKE}")

    ts = datetime.utcnow().isoformat() + "Z"

    with open(RAW_LAKE, encoding="utf-8") as f_in, \
         open(PROMOTED_LAKE, "w", encoding="utf-8") as f_out:

        for line in f_in:
            row = json.loads(line)

            promoted = {
                "lake_id": "T1_Biological_Spellman1998",
                "series": row["series"],
                "from_time_min": row["from_time_min"],
                "to_time_min": row["to_time_min"],
                "interval_min": row["interval_min"],
                "from_title": row["from_title"],
                "to_title": row["to_title"],
                "meta": {
                    "domain": "biology",
                    "subdomain": "yeast_cell_cycle",
                    "provenance": {
                        "series_accessions": {
                            "alpha": "GSE22",
                            "cdc15": "GSE23",
                        },
                        "platforms": ["GPL59", "GPL60"],
                        "source": "NCBI GEO series matrix files",
                        "spellman_reference": "Spellman et al., Mol Biol Cell 9:3273-97 (1998)",
                        "promotion_timestamp_utc": ts,
                    },
                    "assumptions": {
                        "alpha_cadence_min": 7.0,
                        "cdc15_cadence_min": 10.0,
                        "note": (
                            "Original GEO matrices contain GSM IDs only; "
                            "timepoints reconstructed as equal-spaced samples "
                            "per series based on study description."
                        ),
                    },
                    "quality": {
                        "temporal_precision": "low",
                        "role": "historical_oscillator_not_chronometer",
                    },
                },
            }

            f_out.write(json.dumps(promoted) + "\n")

    print(f"[*] T1 Biological promoted → {PROMOTED_LAKE}")


if __name__ == "__main__":
    promote()
