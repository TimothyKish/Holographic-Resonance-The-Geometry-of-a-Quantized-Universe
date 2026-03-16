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


def promote_lake(lake_name, cfg):
    input_path = INPUT_DIR / f"{lake_name}.jsonl"
    output_path = PROMOTED_DIR / f"{lake_name}_promoted.jsonl"
    domain = cfg.get("domain", "unknown")

    ensure_dir(PROMOTED_DIR)

    # If a promoted file already exists, check if it's truly V5.
    if output_path.exists():
        with output_path.open("r", encoding="utf-8") as f:
            first = None
            for line in f:
                line = line.strip()
                if line:
                    first = json.loads(line)
                    break

        if first is not None and is_v5_entry(first):
            print(f"[OK] {lake_name} already in V5 format → {output_path}")
            return

        # Not V5: treat existing promoted file as raw and rewrap it.
        print(f"[REWRAP] {lake_name}: existing promoted file is not V5, re‑promoting → {output_path}")
        raw_lines_path = output_path
    else:
        # No promoted file yet: use raw input from INPUT_DIR.
        if not input_path.exists():
            print(f"[WARN] No raw or promoted lake found for {lake_name}")
            return
        print(f"[PROMOTE] {lake_name}: {input_path} -> {output_path}")
        raw_lines_path = input_path

    # Read raw lines from whichever path we decided
    with raw_lines_path.open("r", encoding="utf-8") as fin:
        lines = [line.strip() for line in fin if line.strip()]

    if not lines:
        print(f"[WARN] Lake {lake_name} is empty.")
        return

    # Peek first entry just for sanity
    try:
        json.loads(lines[0])
    except json.JSONDecodeError as e:
        print(f"[ERROR] Lake {lake_name} has invalid JSON on first line: {e}")
        return

    # Write proper V5‑wrapped entries
    with output_path.open("w", encoding="utf-8") as fout:
        for idx, line in enumerate(lines, start=1):
            try:
                raw_entry = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"[WARN] Skipping line {idx} in {lake_name}: JSON decode error: {e}")
                continue

            promoted = promote_entry(raw_entry, lake_name, domain, volume=5, idx=idx)
            fout.write(json.dumps(promoted) + "\n")

    print(f"[DONE] Lake {lake_name} promoted to V5 format at: {output_path}")



def main():
    volumes_cfg = load_json(CONFIG_DIR / "volumes.json")["volumes"]

    for lake_name, cfg in volumes_cfg.items():
        if not cfg.get("enabled", False):
            continue
        promote_lake(lake_name, cfg)


if __name__ == "__main__":
    main()
