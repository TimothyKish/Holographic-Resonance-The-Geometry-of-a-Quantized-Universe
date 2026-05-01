# vol5/T-Series/T1_Biological/scripts/validate.py
import json
import os

SCALAR_LAKE = "../lake/biological_scalar.jsonl"

def validate():
    print("===============================================================")
    print(" 🧬 VALIDATING T1 BIOLOGICAL (Spellman α + cdc15)")
    print("===============================================================")

    if not os.path.exists(SCALAR_LAKE):
        raise FileNotFoundError(f"Scalar lake not found: {SCALAR_LAKE}")

    counts = {"alpha": 0, "cdc15": 0}
    last_t = {"alpha": None, "cdc15": None}
    bad_monotonic = []
    bad_dt = []

    with open(SCALAR_LAKE, encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            series = row["series"]
            t_mid = row["t_mid_min"]
            dt = row["dt_min"]

            counts[series] = counts.get(series, 0) + 1

            # monotonic mid-time
            prev = last_t.get(series)
            if prev is not None and t_mid <= prev:
                bad_monotonic.append((series, prev, t_mid))
            last_t[series] = t_mid

            # basic dt sanity
            if dt <= 0:
                bad_dt.append((series, dt))

    print(f"[*] Interval counts: {counts}")
    if bad_monotonic:
        print("[!] Non-monotonic mid-times detected:")
        for s, p, t in bad_monotonic[:10]:
            print(f"    {s}: {p} → {t}")
    else:
        print("[+] Monotonic mid-times per series OK.")

    if bad_dt:
        print("[!] Non-positive durations detected:")
        for s, d in bad_dt[:10]:
            print(f"    {s}: dt = {d}")
    else:
        print("[+] All durations positive.")

    print("[*] T1 Biological validation complete.")


if __name__ == "__main__":
    validate()
