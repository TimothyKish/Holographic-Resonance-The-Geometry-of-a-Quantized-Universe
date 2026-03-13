# ==============================================================================
# SCRIPT: unify.py
# TARGET: Merge scalarized lakes, run modulus sweep, build pinch table
# AUTHORS: Timothy John Kish & Phoenix Aurora
# LICENSE: Sovereign Protected / KishLattice 16pi Initiative Copyright 2026
# ==============================================================================
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "configs"
UNIFIED_DIR = ROOT / "lakes" / "unified"

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def ensure_dir(path):
    path.mkdir(parents=True, exist_ok=True)

def load_scalarized_lake(name):
    path = UNIFIED_DIR / f"{name}_scalarized.jsonl"
    if not path.exists():
        print(f"Scalarized lake missing: {path}")
        return []
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entries.append(json.loads(line))
    return entries

def modulus_lock_rate(entries, modulus):
    if not entries:
        return 0.0
    locked = 0
    for e in entries:
        k = e.get("scalar_klc", None)
        if k is None:
            continue
        phase = (k % modulus) / modulus
        # simple shelf criterion; refine later if needed
        if phase < 0.05 or phase > 0.95:
            locked += 1
    return locked / max(1, len(entries))

def main():
    ensure_dir(UNIFIED_DIR)

    unify_cfg = load_json(CONFIG_DIR / "unify.json")["unify"]
    volumes_cfg = load_json(CONFIG_DIR / "volumes.json")["volumes"]

    unified_path = UNIFIED_DIR / "unified_master.jsonl"
    pinch_table_path = UNIFIED_DIR / "pinch_table.json"
    sweep_results_path = UNIFIED_DIR / "sweep_results.json"

    unified_entries = []
    domain_map = {}

    # Load scalarized lakes (unsorted)
    for name, cfg in volumes_cfg.items():
        if not cfg.get("enabled", False):
            continue

        domain = cfg.get("domain", "unknown")
        entries = load_scalarized_lake(name)

        for e in entries:
            e["_volume_name"] = name
            e["_domain"] = domain
            unified_entries.append(e)
            domain_map.setdefault(domain, []).append(e)

    # Write unified master (unsorted)
    with open(unified_path, "w", encoding="utf-8") as f:
        for e in unified_entries:
            f.write(json.dumps(e) + "\n")
    print(f"Unified master written: {unified_path}")

    # Modulus sweep
    sweep_cfg = unify_cfg["modulus_sweep"]
    sweep_values = sweep_cfg["values"]
    sweep_labels = sweep_cfg["labels"]

    sweep_results = []

    for domain, entries in domain_map.items():
        for value, label in zip(sweep_values, sweep_labels):
            rate = modulus_lock_rate(entries, value)
            sweep_results.append({
                "domain": domain,
                "modulus": value,
                "label": label,
                "lock_rate": rate
            })

    with open(sweep_results_path, "w", encoding="utf-8") as f:
        json.dump(sweep_results, f, indent=2)
    print(f"Sweep results written: {sweep_results_path}")

    # Scale‑ordered pinch table
    pinch_cfg = unify_cfg["cross_domain_pinch"]
    pinch_domains = pinch_cfg["domains"]

    # Sort by scale_rank from volumes.json
    ordered_domains = sorted(
        volumes_cfg.items(),
        key=lambda x: x[1].get("scale_rank", 999)
    )

    pinch_table = []
    for name, cfg in ordered_domains:
        if not cfg.get("enabled", False):
            continue

        domain = cfg["domain"]
        entries = domain_map.get(domain, [])
        if not entries:
            continue

        row = {
            "domain": domain,
            "volume_name": name,
            "scale_rank": cfg.get("scale_rank", None)
        }

        for value, label in zip(sweep_values, sweep_labels):
            rate = modulus_lock_rate(entries, value)
            row[f"lock_{label}"] = rate

        pinch_table.append(row)

    with open(pinch_table_path, "w", encoding="utf-8") as f:
        json.dump(pinch_table, f, indent=2)
    print(f"Pinch table written: {pinch_table_path}")

if __name__ == "__main__":
    main()
