# ==============================================================================
# SCRIPT: validate.py
# TARGET: Validate promoted lakes against the V5 schema
# AUTHORS: Timothy John Kish & Phoenix Aurora
# LICENSE: Sovereign Protected / KishLattice 16pi Initiative Copyright 2026
# ==============================================================================

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "configs"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_entry(entry, schema, expected_domain: str):
    required = schema["required_fields"]
    errors = []

    # top-level required keys
    for key in [
        "entity_id",
        "domain",
        "volume",
        "lake_id",
        "geometry_payload",
        "scalar_kls",
        "scalar_klc",
        "meta",
    ]:
        if key not in entry:
            errors.append(f"Missing required field: {key}")

    # domain: must match the lake's declared domain
    if "domain" in entry and entry["domain"] != expected_domain:
        errors.append(
            f"Invalid domain for lake (expected '{expected_domain}', got '{entry['domain']}')"
        )

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


def validate_lake(path: Path, schema, expected_domain: str):
    print("\n==============================================")
    print(">>> START VALIDATION FOR FILE:")
    print("    ", path)
    print("==============================================")

    if not path.exists():
        print("  !! File does not exist, skipping.")
        return

    print("VALIDATING:", path)
    print(f"Validating lake: {path.name}")

    errors_total = 0
    first_line_shown = False

    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            raw_line = line
            line = line.strip()
            if not line:
                continue

            if not first_line_shown:
                print("  >>> First non-empty line of file:")
                print("      ", raw_line.rstrip()[:200])
                first_line_shown = True

            try:
                entry = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"  Line {i}: JSON decode error: {e}")
                errors_total += 1
                continue

            errs = validate_entry(entry, schema, expected_domain=expected_domain)
            if errs:
                errors_total += len(errs)
                print(f"  Line {i}:")
                for e in errs:
                    print(f"    - {e}")

    if errors_total == 0:
        print("  ✅ OK\n")
    else:
        print(f"  ERRORS: {errors_total}\n")


def main():
    schema_path = CONFIG_DIR / "schema.json"
    volumes_path = CONFIG_DIR / "volumes.json"

    print("ROOT:       ", ROOT)
    print("CONFIG_DIR: ", CONFIG_DIR)
    print("SCHEMA:     ", schema_path)
    print("VOLUMES:    ", volumes_path)
    print("")

    schema = load_json(schema_path)
    volumes_cfg = load_json(volumes_path)["volumes"]

    print("==== Lakes to be validated ===")
    for name, cfg in volumes_cfg.items():
        if cfg.get("enabled", False):
            print(" -", name, "→", ROOT / cfg["path"])
    print("================================\n")

    for name, cfg in volumes_cfg.items():
        if not cfg.get("enabled", False):
            continue

        lake_path = ROOT / cfg["path"]
        if not lake_path.exists():
            print(f"Missing lake file for {name}: {lake_path}")
            continue

        expected_domain = cfg.get("domain")
        validate_lake(lake_path, schema, expected_domain=expected_domain)


if __name__ == "__main__":
    main()
