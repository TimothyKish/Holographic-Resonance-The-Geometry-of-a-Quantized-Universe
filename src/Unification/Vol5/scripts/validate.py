# ==============================================================================
# SCRIPT: validate.py
# TARGET: Validate unified lakes against the V5 schema
# AUTHORS: Timothy John Kish & Phoenix Aurora
# LICENSE: Sovereign Protected / KishLattice 16pi Initiative Copyright 2026
# ==============================================================================
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "configs"
LAKES_INPUT_DIR = ROOT / "lakes" / "inputs"

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_entry(entry, schema):
    required = schema["required_fields"]
    errors = []

    # top-level required keys
    for key in ["entity_id", "domain", "volume", "lake_id", "geometry_payload", "scalar_kls", "scalar_klc", "meta"]:
        if key not in entry:
            errors.append(f"Missing required field: {key}")

    # domain
    if "domain" in entry and entry["domain"] not in schema["allowed_domains"]:
        errors.append(f"Invalid domain: {entry['domain']}")

    # geometry_payload
    gp = entry.get("geometry_payload", {})
    for gkey in required["geometry_payload"]["required"]:
        if gkey not in gp:
            errors.append(f"geometry_payload missing: {gkey}")

    # meta
    meta = entry.get("meta", {})
    for mkey in schema["meta"]["required"]:
        if mkey not in meta:
            errors.append(f"meta missing: {mkey}")

    return errors

def validate_lake(path, schema):
    print(f"Validating lake: {path.name}")
    errors_total = 0
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"  Line {i}: JSON decode error: {e}")
                errors_total += 1
                continue

            errs = validate_entry(entry, schema)
            if errs:
                errors_total += len(errs)
                print(f"  Line {i}:")
                for e in errs:
                    print(f"    - {e}")

    if errors_total == 0:
        print("  ✅ OK\n")
    else:
        print(f"  ❌ {errors_total} issues found\n")

def main():
    schema = load_json(CONFIG_DIR / "schema.json")
    volumes_cfg = load_json(CONFIG_DIR / "volumes.json")["volumes"]

    for name, cfg in volumes_cfg.items():
        if not cfg.get("enabled", False):
            continue
        lake_path = ROOT / cfg["path"]
        if not lake_path.exists():
            print(f"Missing lake file for {name}: {lake_path}")
            continue
        validate_lake(lake_path, schema)

if __name__ == "__main__":
    main()
