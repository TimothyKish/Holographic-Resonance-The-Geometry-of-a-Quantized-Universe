# ==============================================================================
# SCRIPT: promote_lakes_to_v5.py
# TARGET: Promote raw lakes into standardized V5 sovereign format
# AUTHORS: Timothy John Kish & Phoenix Aurora
# LICENSE: Sovereign Protected / KishLattice 16pi Initiative Copyright 2026
# ==============================================================================
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "configs"
INPUT_DIR = ROOT / "lakes" / "inputs"
PROMOTED_DIR = ROOT / "lakes" / "inputs_promoted"

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def ensure_dir(path):
    path.mkdir(parents=True, exist_ok=True)

def is_v5_entry(entry):
    return isinstance(entry, dict) and "entity_id" in entry

def promote_entry(raw_entry, lake_name, domain, volume=5, idx=0):
    entity_id = f"{lake_name.upper()}_{idx:06d}"

    return {
        "entity_id": entity_id,
        "domain": domain,
        "volume": volume,
        "lake_id": lake_name,

        "geometry_payload": {
            "coordinates": [],
            "dimensionality": 0,
            "geometry_type": "unknown"
        },

        "scalar_kls": 0.0,
        "scalar_klc": 0.0,

        "meta": {
            "source": "vol5_promotion_raw_lake",
            "ingest_timestamp": "2026-03-13T00:00:00Z",
            "sovereign": False
        },

        "_raw_payload": raw_entry
    }

def promote_lake(name, cfg):
    # ALWAYS read raw lakes from INPUT_DIR
    src = INPUT_DIR / f"{name}.jsonl"
    domain = cfg.get("domain", "unknown")

    if not src.exists():
        print(f"[SKIP] Missing source lake for {name}: {src}")
        return

    ensure_dir(PROMOTED_DIR)
    dst = PROMOTED_DIR / f"{name}_promoted.jsonl"

    print(f"[PROMOTE] {name}: {src} -> {dst}")

    with open(src, "r", encoding="utf-8") as fin:
        lines = [line.strip() for line in fin if line.strip()]

    if not lines:
        print(f"[WARN] Lake {name} is empty.")
        return

    # Peek first line to see if already V5
    try:
        first_entry = json.loads(lines[0])
    except json.JSONDecodeError as e:
        print(f"[ERROR] Lake {name} has invalid JSON on first line: {e}")
        return

    if is_v5_entry(first_entry):
        print(f"[SKIP] Lake {name} already appears to be in V5 format.")
        return

    with open(dst, "w", encoding="utf-8") as fout:
        for idx, line in enumerate(lines):
            try:
                raw_entry = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"[WARN] Skipping line {idx+1} in {name}: JSON decode error: {e}")
                continue

            promoted = promote_entry(raw_entry, name, domain, volume=5, idx=idx+1)
            fout.write(json.dumps(promoted) + "\n")

    print(f"[DONE] Lake {name} promoted to V5 format at: {dst}")

def main():
    volumes_cfg = load_json(CONFIG_DIR / "volumes.json")["volumes"]

    for name, cfg in volumes_cfg.items():
        if not cfg.get("enabled", False):
            continue
        promote_lake(name, cfg)

if __name__ == "__main__":
    main()
