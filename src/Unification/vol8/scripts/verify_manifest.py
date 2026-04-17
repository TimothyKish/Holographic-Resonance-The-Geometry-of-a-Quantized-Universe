import json
import os
from pathlib import Path

VOL_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = VOL_ROOT / "large_file_manifest.json"

SIZE_TOLERANCE_MB = 5  # allow small differences due to filesystem rounding

def main():
    if not MANIFEST_PATH.exists():
        print(f"Manifest not found: {MANIFEST_PATH}")
        return

    with open(MANIFEST_PATH, "r") as f:
        entries = json.load(f)

    print("Verifying large sovereign lakes...\n")

    all_ok = True

    for entry in entries:
        rel_path = entry["path"]
        expected_size = entry["size_mb"]

        full_path = VOL_ROOT / rel_path

        if not full_path.exists():
            print(f"[MISSING] {rel_path}")
            all_ok = False
            continue

        actual_size = full_path.stat().st_size / (1024 * 1024)

        if abs(actual_size - expected_size) > SIZE_TOLERANCE_MB:
            print(f"[SIZE MISMATCH] {rel_path}")
            print(f"  Expected: {expected_size} MB")
            print(f"  Actual:   {actual_size:.2f} MB")
            all_ok = False
        else:
            print(f"[OK] {rel_path} ({actual_size:.2f} MB)")

    if all_ok:
        print("\nAll large files verified successfully.")
    else:
        print("\nSome files are missing or mismatched. See above.")

if __name__ == "__main__":
    main()
