# ==============================================================================
# SCRIPT: universal_promote.py
# TARGET: Promote unified scalarized lakes to V5-compliant promoted lakes
# AUTHORS: Timothy John Kish & Phoenix Aurora
# LICENSE: Sovereign Protected / KishLattice 16pi Initiative Copyright 2026
# ==============================================================================

import argparse
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAKES_DIR = ROOT / "lakes"


def promote_universal(input_path: Path, output_path: Path, lake_id: str, volume: int, domain: str) -> None:
    print(f"[PROMOTE] {lake_id}")
    print(f"  Input:  {input_path}")
    print(f"  Output: {output_path}")

    errors = 0
    count = 0

    output_path.parent.mkdir(parents=True, exist_ok=True)

    now_ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    with input_path.open("r", encoding="utf-8") as f_in, \
         output_path.open("w", encoding="utf-8") as f_out:

        for line in f_in:
            line = line.strip()
            if not line:
                continue

            try:
                src = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"  !! JSON decode error in input: {e}")
                errors += 1
                continue

            # Geometry: pass through from scalarized lake
            geometry = src.get("geometry_payload", {})

            # Scalar fields: default to 0.0 if not present
            scalar_kls = src.get("scalar_kls", 0.0)
            scalar_klc = src.get("scalar_klc", 0.0)

            # Build V5-compliant promoted entry
            entry_out = {
                "entity_id": str(uuid.uuid4()),
                "domain": domain,
                "volume": int(volume),
                "lake_id": lake_id,
                "geometry_payload": geometry,
                "scalar_kls": float(scalar_kls),
                "scalar_klc": float(scalar_klc),
                "meta": {
                    "source": "vol5_promotion_raw_lake",
                    "ingest_timestamp": now_ts,
                    "sovereign": True,
                    "source_row": src,
                },
            }

            f_out.write(json.dumps(entry_out, ensure_ascii=False) + "\n")
            count += 1

    if errors == 0:
        print(f"[DONE] Promoted {count} entries → {output_path}\n")
    else:
        print(f"[DONE] Promoted {count} entries with {errors} input errors → {output_path}\n")


def main():
    parser = argparse.ArgumentParser(description="Universal promoter for Vol5 lakes")
    parser.add_argument("--input", required=True, help="Path to unified scalarized input JSONL")
    parser.add_argument("--output", required=True, help="Path to promoted output JSONL")
    parser.add_argument("--lake_id", required=True, help="Lake ID (e.g., b1_chirality)")
    parser.add_argument("--volume", required=True, type=int, help="Volume number (e.g., 5)")
    parser.add_argument("--domain", required=True, help="Domain (e.g., biology, chemistry, cosmology)")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    promote_universal(
        input_path=input_path,
        output_path=output_path,
        lake_id=args.lake_id,
        volume=args.volume,
        domain=args.domain,
    )


if __name__ == "__main__":
    main()
