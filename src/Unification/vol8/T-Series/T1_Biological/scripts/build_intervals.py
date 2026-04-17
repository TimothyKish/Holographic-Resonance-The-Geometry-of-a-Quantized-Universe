# vol5/T-Series/T1_Biological/scripts/build_intervals.py
import os
import json
import re

RAW_MATRIX_DIR = "../lake/raw_matrices"
OUT_LAKE = "../lake/biological_real_raw.jsonl"

ALPHA_FILE = "GSE22_alpha_matrix.txt"
CDC15_FILE = "GSE23_cdc15_matrix.txt"


def parse_matrix(path, series_name):
    print(f"[*] Parsing matrix: {path} ({series_name})")

    with open(path, encoding="utf-8") as f:
        lines = [l.rstrip("\n") for l in f]

    # 1. Find the first non-comment line → header
    header = None
    for line in lines:
        if line.startswith("!"):
            continue
        parts = line.split("\t")
        if len(parts) > 1:
            header = parts
            break

    if header is None:
        print(f"[!] No usable header found in {path}")
        return []

    # Column 0 is ID_REF, columns 1..N are GSM IDs
    sample_ids = [s.strip().strip('"') for s in header[1:]]

    # Series-specific cadence (documented assumption)
    if series_name == "alpha":
        dt = 7.0
    elif series_name == "cdc15":
        dt = 10.0
    else:
        dt = 1.0

    samples = []
    for idx, gsm in enumerate(sample_ids):
        t = idx * dt
        samples.append({
            "series": series_name,
            "title": gsm,
            "time_min": t,
        })

    print(f"[+] Parsed {len(samples)} samples for {series_name} (dt = {dt} min)")
    return samples





def build_intervals(samples):
    print("[*] Building intervals...")
    by_series = {}
    for s in samples:
        by_series.setdefault(s["series"], []).append(s)

    intervals = []
    for series, group in by_series.items():
        group_sorted = sorted(group, key=lambda x: x["time_min"])

        for i in range(len(group_sorted) - 1):
            s0 = group_sorted[i]
            s1 = group_sorted[i + 1]
            delta = s1["time_min"] - s0["time_min"]

            intervals.append({
                "series": series,
                "from_title": s0["title"],
                "to_title": s1["title"],
                "from_time_min": s0["time_min"],
                "to_time_min": s1["time_min"],
                "interval_min": round(delta, 6),
            })

        print(f"[+] {series}: {len(group_sorted) - 1} intervals")

    return intervals


def main():
    print("===============================================================")
    print(" 🧬 BUILDING T1 BIOLOGICAL TEMPORAL LAKE (Spellman α + cdc15)")
    print("===============================================================")

    alpha_path = os.path.join(RAW_MATRIX_DIR, ALPHA_FILE)
    cdc15_path = os.path.join(RAW_MATRIX_DIR, CDC15_FILE)

    all_samples = []
    all_samples.extend(parse_matrix(alpha_path, "alpha"))
    all_samples.extend(parse_matrix(cdc15_path, "cdc15"))

    intervals = build_intervals(all_samples)

    os.makedirs(os.path.dirname(OUT_LAKE), exist_ok=True)
    with open(OUT_LAKE, "w", encoding="utf-8") as f:
        for row in intervals:
            f.write(json.dumps(row) + "\n")

    print("[*] T1 Biological Temporal Lake built.")
    print(f"[*] Total intervals: {len(intervals)}")


if __name__ == "__main__":
    main()
