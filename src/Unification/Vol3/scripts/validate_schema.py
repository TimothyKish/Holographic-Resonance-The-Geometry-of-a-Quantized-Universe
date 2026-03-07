#!/usr/bin/env python3
"""
Vol3 Schema Validator
Validates sovereign Materials, Chemistry, and Clean lakes
against the canonical Vol3 schema.

Outputs:
    reports/umc/schema_validation.md
"""

import json
from pathlib import Path
from datetime import datetime

# === Paths ===
ROOT = Path(__file__).resolve().parents[2]
LAKES = ROOT / "lakes"
REPORT = ROOT / "reports" / "umc" / "schema_validation.md"

SCHEMA = {
    "required_fields": [
        "entity_id",
        "domain",
        "volume",
        "lake_id",
        "geometry_payload",
        "scalar_kls",
        "scalar_klc",
        "meta"
    ],
    "optional_fields": ["kuu_series"],
    "meta_required": [
        "source",
        "ingested_at",
        "schema_version",
        "units"
    ],
    "domains": ["materials", "chemistry"]
}

def validate_entry(obj, errors, file_name, line_num):
    # Check required fields
    for field in SCHEMA["required_fields"]:
        if field not in obj:
            errors.append(f"{file_name}:{line_num} — Missing required field '{field}'")
    
    # Check domain
    if "domain" in obj and obj["domain"] not in SCHEMA["domains"]:
        errors.append(f"{file_name}:{line_num} — Invalid domain '{obj['domain']}'")

    # Check volume
    if "volume" in obj and obj["volume"] != 3:
        errors.append(f"{file_name}:{line_num} — Volume must be 3, got {obj['volume']}")

    # Check scalar types
    if "scalar_kls" in obj and not isinstance(obj["scalar_kls"], (int, float)):
        errors.append(f"{file_name}:{line_num} — scalar_kls must be numeric")

    if "scalar_klc" in obj and not isinstance(obj["scalar_klc"], (int, float)):
        errors.append(f"{file_name}:{line_num} — scalar_klc must be numeric")

    # Check meta block
    if "meta" in obj:
        for m in SCHEMA["meta_required"]:
            if m not in obj["meta"]:
                errors.append(f"{file_name}:{line_num} — meta missing '{m}'")

def validate_file(path, errors):
    with open(path) as f:
        for i, line in enumerate(f, start=1):
            try:
                obj = json.loads(line)
                validate_entry(obj, errors, path.name, i)
            except json.JSONDecodeError:
                errors.append(f"{path.name}:{i} — Invalid JSON")

def main():
    errors = []
    lake_dirs = ["materials", "chemicals", "clean"]

    for d in lake_dirs:
        folder = LAKES / d
        for file in folder.glob("*.jsonl"):
            validate_file(file, errors)

    # Write report
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT, "w") as f:
        f.write("# Vol3 Schema Validation Report\n")
        f.write(f"Generated: {datetime.now()}\n\n")

        if errors:
            f.write("## lakes do not conform to Vol3 schema Errors Found\n")
            for e in errors:
                f.write(f"- {e}\n")
        else:
            f.write("## All lakes conform to the Vol3 schema.\n")

    print("Schema validation complete.")
    print(f"Report written to: {REPORT}")

if __name__ == "__main__":
    main()
