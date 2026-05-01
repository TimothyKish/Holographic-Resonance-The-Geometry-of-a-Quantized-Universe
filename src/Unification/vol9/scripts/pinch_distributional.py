# ==============================================================================
# SCRIPT: pinch_distributional.py
# PURPOSE: Distributional geometric pinch (entry-level) between lakes
# AUTHOR:  Timothy John Kish & Copilot
# ==============================================================================

import json
import math
from pathlib import Path
from statistics import mean, median, pstdev


ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "configs"
LAKES_ROOT = ROOT / "lakes"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_scalars(lake_path: Path):
    vals = []
    with lake_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            kls = float(entry.get("scalar_kls", 0.0))
            klc = float(entry.get("scalar_klc", 0.0))
            vals.append((kls, klc))
    return vals


def pinch(a, b):
    dkls = a[0] - b[0]
    dklc = a[1] - b[1]
    return math.sqrt(dkls * dkls + dklc * dklc)


def summarize(values):
    if not values:
        return {
            "mean": 0.0,
            "median": 0.0,
            "min": 0.0,
            "max": 0.0,
            "std": 0.0,
            "count": 0,
        }
    return {
        "mean": mean(values),
        "median": median(values),
        "min": min(values),
        "max": max(values),
        "std": pstdev(values) if len(values) > 1 else 0.0,
        "count": len(values),
    }


def main():
    volumes_cfg = load_json(CONFIG_DIR / "volumes.json")["volumes"]

    # Load all enabled lakes
    lakes = []
    entries = {}

    for name, cfg in volumes_cfg.items():
        if not cfg.get("enabled", False):
            continue

        lake_path = ROOT / cfg["path"]
        if not lake_path.exists():
            print(f"[WARN] Lake file missing, skipping: {name} → {lake_path}")
            continue

        print(f"[INFO] Loading scalars for lake: {name}")
        lakes.append(name)
        entries[name] = load_scalars(lake_path)

    # Compute distributional pinch between lakes
    print("\n# Distributional geometric pinch between lakes (entry-level)\n")
    print("| lake_a | lake_b | count | mean_pinch | median_pinch | min_pinch | max_pinch | std_pinch |")
    print("| --- | --- | ---:| ---:| ---:| ---:| ---:| ---:|")

    for i, a in enumerate(lakes):
        for j, b in enumerate(lakes):
            # We still compute self-pinch to show internal spread (should be small)
            vals_a = entries[a]
            vals_b = entries[b]

            pinches = []
            # Simple pairing strategy: min(len(a), len(b)) pairs
            n = min(len(vals_a), len(vals_b))
            for k in range(n):
                pinches.append(pinch(vals_a[k], vals_b[k]))

            stats = summarize(pinches)
            print(
                f"| {a} | {b} | {stats['count']} | "
                f"{stats['mean']:.6e} | {stats['median']:.6e} | "
                f"{stats['min']:.6e} | {stats['max']:.6e} | {stats['std']:.6e} |"
            )


if __name__ == "__main__":
    main()
