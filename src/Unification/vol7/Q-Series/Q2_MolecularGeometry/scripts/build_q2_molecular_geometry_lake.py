# ==============================================================================
# SCRIPT: build_q2_molecular_geometry_lake.py
# SERIES: Q-Series / Q2_MolecularGeometry
# DOMAIN: quantum
# SOURCE: NIST CCCBDB (Computational Chemistry Comparison and Benchmark DataBase)
#         Experimental molecular geometry measurements
#
# RAW LAKE: Q-Series/Q2_MolecularGeometry/lake/q2_molecular_geometry_raw.jsonl
#   Fields: entity_id, molecule, formula, measurement_type, value
#   Records: 34 (bond lengths in Angstroms, bond angles in degrees)
#   Molecules: Water (H2O), CO2, NH3, and others
#
# SCALARIZATION:
#   scalar = log(value + 1) / log(k_geo)
#   Works for both bond lengths (0.95-2.3 Ang) and bond angles (104-180 deg)
#   log+1 prevents issues near zero for small lengths
#   Result range: ~0.41 (bond lengths) to ~2.86 (bond angles)
#
#   Key value: Water bond angle 104.4776° -> scalar=2.862
#   This is the validated water angle prediction from Vol4.
#
# NULL MIRROR: NQ2_MolecularGeometry
#   Use existing NQ2_MolecularNull lake (scrambled values)
#   Also build chaos null from same range
#
# OUTPUT:
#   vol5/lakes/inputs_promoted/q2_molecular_geometry_promoted.jsonl
#
# AUTHORS: Timothy John Kish & Mondy
# AUDIT STATUS: mondy_verified_2026-04
# ==============================================================================

import json
import math
import uuid
from datetime import datetime, timezone
from pathlib import Path

PI    = math.pi
K_GEO = 16.0 / PI
LOG_K = math.log(K_GEO)

SCRIPTS_DIR = Path(__file__).resolve().parent
Q2_DIR      = SCRIPTS_DIR.parent
Q_SERIES    = Q2_DIR.parent
VOL5_ROOT   = Q_SERIES.parent
PROMOTED    = VOL5_ROOT / "lakes" / "inputs_promoted"

RAW_INPUT   = Q2_DIR / "lake" / "q2_molecular_geometry_raw.jsonl"
OUTPUT_PATH = PROMOTED / "q2_molecular_geometry_promoted.jsonl"

def compute_scalar(rec):
    """
    scalar = log(value + 1) / log(k_geo)
    value: bond length (Ang) or bond angle (degrees)
    """
    value = rec.get("value")
    if value is None:
        return None
    try:
        v = float(value)
        if v <= 0:
            return None
        return math.log(v + 1.0) / LOG_K
    except (TypeError, ValueError):
        return None

def main():
    print("=" * 60)
    print("Q2 Molecular Geometry Lake Builder")
    print("=" * 60)
    print(f"k_geo = {K_GEO:.10f}")
    print(f"Input:  {RAW_INPUT}")
    print(f"Output: {OUTPUT_PATH}")
    print()

    if not RAW_INPUT.exists():
        raise SystemExit(f"Raw lake not found: {RAW_INPUT}")

    PROMOTED.mkdir(parents=True, exist_ok=True)
    now_ts   = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    records  = []
    total    = 0
    computed = 0
    failed   = 0

    with RAW_INPUT.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            raw = json.loads(line)
            s   = compute_scalar(raw)

            if s is not None and math.isfinite(s):
                computed += 1
                # Flag water bond angle specifically
                if (raw.get("molecule") == "Water" and
                        raw.get("measurement_type") == "bond_angle_degrees"):
                    print(f"  Water bond angle: {raw['value']}° -> scalar={s:.6f}")
            else:
                failed += 1
                s = 0.0

            records.append({
                "entity_id":   str(uuid.uuid4()),
                "domain":      "quantum",
                "volume":      5,
                "lake_id":     "q2_molecular_geometry",
                "geometry_payload": {
                    "coordinates":    [],
                    "dimensionality": 0,
                    "geometry_type":  "molecular",
                },
                "scalar_kls":  s,
                "scalar_klc":  s,
                "meta": {
                    "source":           "NIST CCCBDB — Experimental molecular geometry",
                    "ingest_timestamp": now_ts,
                    "sovereign":        True,
                    "audit_status":     "mondy_verified_2026-04",
                    "scalarization":    "log(value + 1) / log(k_geo)",
                    "measurement_type": raw.get("measurement_type", ""),
                    "molecule":         raw.get("molecule", ""),
                },
                "_raw_payload": raw,
            })

    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    scalars = [r["scalar_kls"] for r in records if r["scalar_kls"] > 0]
    print(f"total={total}  computed={computed}  failed={failed}")
    if scalars:
        print(f"scalar range: {min(scalars):.4f} to {max(scalars):.4f}  "
              f"mean={sum(scalars)/len(scalars):.4f}")
    print(f"-> {OUTPUT_PATH.name}")
    print()
    print("Next: add q2_molecular_geometry to configs/volumes.json")
    print("      domain: quantum, scale_rank: 0")

if __name__ == "__main__":
    main()