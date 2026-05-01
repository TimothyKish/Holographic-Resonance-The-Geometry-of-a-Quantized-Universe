# ==============================================================================
# SCRIPT: pinch_lake_level.py
# PURPOSE: Lake-level geometric pinch matrix (mean scalar_kls, scalar_klc)
# AUTHOR:  Timothy John Kish & Copilot
# ==============================================================================

import json
import math
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "configs"
LAKES_ROOT = ROOT / "lakes"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_mean_scalars(lake_path: Path):
    kls_vals = []
    klc_vals = []

    with lake_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            kls_vals.append(float(entry.get("scalar_kls", 0.0)))
            klc_vals.append(float(entry.get("scalar_klc", 0.0)))

    if not kls_vals:
        return 0.0, 0.0

    return mean(kls_vals), mean(klc_vals)


def pinch(a, b):
    dkls = a[0] - b[0]
    dklc = a[1] - b[1]
    return math.sqrt(dkls * dkls + dklc * dklc)


def main():
    volumes_cfg = load_json(CONFIG_DIR / "volumes.json")["volumes"]

    # Collect enabled lakes and their mean scalars
    lakes = []
    scalars = {}

    for name, cfg in volumes_cfg.items():
        if not cfg.get("enabled", False):
            continue

        lake_path = ROOT / cfg["path"]
        if not lake_path.exists():
            print(f"[WARN] Lake file missing, skipping: {name} → {lake_path}")
            continue

        print(f"[INFO] Loading mean scalars for lake: {name}")
        kls_mean, klc_mean = load_mean_scalars(lake_path)
        lakes.append(name)
        scalars[name] = (kls_mean, klc_mean)

    # Compute pinch matrix
    print("\n# Lake-level geometric pinch matrix (mean scalar_kls, scalar_klc)\n")
    header = ["lake"] + lakes
    print("| " + " | ".join(header) + " |")
    print("|" + " --- |" * len(header))

    for a in lakes:
        row = [a]
        for b in lakes:
            p = pinch(scalars[a], scalars[b])
            row.append(f"{p:.6e}")
        print("| " + " | ".join(row) + " |")


if __name__ == "__main__":
    main()
