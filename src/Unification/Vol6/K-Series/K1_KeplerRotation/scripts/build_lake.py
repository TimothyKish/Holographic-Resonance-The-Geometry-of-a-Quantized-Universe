# ==============================================================================
# SCRIPT: build_k1_kepler_rotation_lake.py
# SERIES: K-Series / K1_KeplerRotation
# DOMAIN: stellar_rotation
#
# SOURCE: McQuillan, Mazeh & Aigrain (2014), ApJS 211, 24
#         Kepler stellar rotation periods for ~34,000 main-sequence stars
#         VizieR catalog J/ApJS/211/24
#
# DOWNLOAD:
#   1. Go to: https://vizier.cds.unistra.fr/viz-bin/VizieR-4?-source=J/ApJS/211/24
#   2. Set output format to CSV and max rows to unlimited
#   3. Download and save as:
#      K-Series/K1_KeplerRotation/lake/kepler_rotation_raw.csv
#
#   The CSV should have columns including: KIC, Prot (rotation period days)
#   Alternative direct download:
#   https://cdsarc.cds.unistra.fr/viz-bin/nph-Cat/fits?J/ApJS/211/24
#
# KINEMATIC TYPE: SPIN (stellar rotation on axis)
#   This is physically distinct from orbital revolution (P1).
#   A star's rotation period measures how fast it spins — a direct
#   kinematic quantity encoding the angular momentum history of the
#   stellar formation process.
#
# SCALAR:
#   scalar = log(Prot + 1) / log(k_geo)
#   Prot in days. Range: 1-100 days -> scalar 0.43 to 2.57
#   Fills Gap 1 (1.05-1.67) corresponding to periods 4.5-14.2 days
#   Overlaps chemistry (0.10-1.05) at short periods
#   Overlaps biology (1.79-2.30) at 20-50 day periods
#
# WHY THIS MATTERS:
#   Orbital (revolution) showed z=9.89. Stellar rotation (spin) tests
#   whether the lattice sees spin and revolution the same way, or
#   whether they are physically distinct kinematic modes.
#   If both show signal: lattice responds to all periodic motion.
#   If only one: the lattice distinguishes spin from revolution.
#
# AUTHORS: Timothy John Kish & Mondy
# AUDIT STATUS: mondy_verified_2026-04
# ==============================================================================

import csv
import json
import math
import uuid
from datetime import datetime, timezone
from pathlib import Path

PI    = math.pi
K_GEO = 16.0 / PI
LOG_K = math.log(K_GEO)

SCRIPTS_DIR = Path(__file__).resolve().parent
K1_DIR      = SCRIPTS_DIR.parent
K_SERIES    = K1_DIR.parent
VOL5_ROOT   = K_SERIES.parent
PROMOTED    = VOL5_ROOT / "lakes" / "inputs_promoted"

RAW_INPUT   = K1_DIR / "lake" / "kepler_rotation_raw.csv"
OUT_REAL    = PROMOTED / "k1_kepler_rotation_promoted.jsonl"

PROT_MAX    = 200.0  # days — exclude spurious long periods


def compute_scalar(prot_days):
    try:
        p = float(prot_days)
        if p <= 0 or p > PROT_MAX:
            return None
        return math.log(p + 1.0) / LOG_K
    except (TypeError, ValueError):
        return None


def find_period_column(header_row):
    """Find the rotation period column — handles different VizieR export formats."""
    for i, col in enumerate(header_row):
        col_clean = col.strip().strip('"').lower()
        if col_clean in ("prot", "p_rot", "period", "rot_period", "rotperiod"):
            return i
    # Fallback: look for anything containing "prot" or "period"
    for i, col in enumerate(header_row):
        if "prot" in col.lower() or ("period" in col.lower() and "orb" not in col.lower()):
            return i
    return None


def find_kic_column(header_row):
    """Find the KIC ID column."""
    for i, col in enumerate(header_row):
        col_clean = col.strip().strip('"').lower()
        if col_clean in ("kic", "kic_id", "kid", "kepid"):
            return i
    return None


def main():
    print("=" * 60)
    print("K1 Kepler Stellar Rotation Lake Builder")
    print("=" * 60)
    print(f"k_geo = {K_GEO:.10f}")
    print(f"Scalar: log(Prot_days + 1) / log(k_geo)")
    print(f"Input:  {RAW_INPUT}")
    print(f"Output: {OUT_REAL}")
    print()

    if not RAW_INPUT.exists():
        print("RAW FILE NOT FOUND.")
        print()
        print("Download instructions:")
        print("  1. Visit: https://vizier.cds.unistra.fr/viz-bin/VizieR-4?-source=J/ApJS/211/24")
        print("  2. Set maximum rows to unlimited (999999)")
        print("  3. Output format: Comma Separated Values (CSV)")
        print("  4. Submit and download")
        print(f"  5. Save as: {RAW_INPUT}")
        print()
        print("The CSV must contain a column named 'Prot' (rotation period in days)")
        raise SystemExit("Awaiting raw data download.")

    PROMOTED.mkdir(parents=True, exist_ok=True)
    now_ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    scalars = []
    total = computed = failed = gap1_count = 0

    with RAW_INPUT.open("r", encoding="utf-8-sig") as fin, \
         OUT_REAL.open("w", encoding="utf-8") as fout:

        # Try CSV parsing
        reader = csv.reader(fin)
        header = next(reader, None)
        if header is None:
            raise SystemExit("Empty file.")

        prot_col = find_period_column(header)
        kic_col  = find_kic_column(header)

        if prot_col is None:
            print(f"Header columns found: {header}")
            raise SystemExit("Cannot find Prot column. Check CSV format.")

        print(f"Using column {prot_col} ('{header[prot_col].strip()}') for rotation period")
        if kic_col is not None:
            print(f"Using column {kic_col} ('{header[kic_col].strip()}') for KIC ID")
        print()

        for row in reader:
            if not row or len(row) <= prot_col:
                continue
            total += 1

            prot_raw = row[prot_col].strip()
            kic_id   = row[kic_col].strip() if kic_col is not None else f"KIC_{total}"

            s = compute_scalar(prot_raw)
            if s is None:
                failed += 1
                continue

            computed += 1
            scalars.append(s)
            if 1.05 <= s <= 1.67:
                gap1_count += 1

            rec = {
                "entity_id": str(uuid.uuid4()),
                "domain":    "stellar_rotation",
                "volume":    5,
                "lake_id":   "k1_kepler_rotation",
                "geometry_payload": {
                    "coordinates":    [],
                    "dimensionality": 0,
                    "geometry_type":  "stellar_rotation",
                },
                "scalar_kls": s,
                "scalar_klc": s,
                "meta": {
                    "source":           "McQuillan+ 2014 ApJS 211 24 (VizieR J/ApJS/211/24)",
                    "ingest_timestamp": now_ts,
                    "sovereign":        True,
                    "audit_status":     "mondy_verified_2026-04",
                    "scalarization":    "log(Prot_days + 1) / log(k_geo)",
                    "kinematic_type":   "spin_period",
                    "kic_id":           kic_id,
                    "prot_days":        float(prot_raw) if prot_raw else None,
                },
                "_raw_payload": {"kic_id": kic_id, "prot_days": prot_raw},
            }
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")

            if total % 10000 == 0:
                print(f"  {total:,} read, {computed:,} computed...")

    print(f"total={total:,}  computed={computed:,}  failed={failed:,}")
    if scalars:
        print(f"scalar range: {min(scalars):.4f} to {max(scalars):.4f}  mean={sum(scalars)/len(scalars):.4f}")
        print(f"Gap 1 records (1.05-1.67): {gap1_count:,} of {computed:,} ({100*gap1_count/computed:.1f}%)")
    print(f"-> {OUT_REAL.name}")
    print()
    print("Add k1_kepler_rotation to configs/volumes.json (entry in batch_volumes_update.json)")


if __name__ == "__main__":
    main()