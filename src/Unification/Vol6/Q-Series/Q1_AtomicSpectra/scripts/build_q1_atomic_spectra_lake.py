# ==============================================================================
# SCRIPT: build_q1_atomic_spectra_lake.py
# SERIES: Q-Series / Q1_AtomicSpectra
# DOMAIN: quantum
# SOURCE: NIST Atomic Spectra Database (ASD) — empirical spectral lines
#         https://physics.nist.gov/asd
#
# RAW LAKE: Q-Series/Q1_AtomicSpectra/lake/q1_atomic_spectra_raw.jsonl
#   Fields: entity_id, element, wavelength_nm, upper_energy_cm1
#   Records: ~2975 (hydrogen Lyman series and other elements)
#
# SCALARIZATION:
#   scalar = log(upper_energy_cm1 + 1) / log(k_geo)
#   upper_energy_cm1 is the upper state energy in wavenumbers (cm⁻¹)
#   This is the natural quantum energy scale for atomic transitions.
#   log-k_geo normalization consistent with all other domains.
#
#   For H I Lyman series: upper_energy_cm1 ~109,600 cm⁻¹
#   scalar = log(109600+1)/log(5.093) = 16.12/1.628 = 9.90
#
#   NOTE: Q_Refereed_Vol1 used a different scalar (klc_resonance ~0.45-0.51)
#   This script uses the raw wavenumber approach for clean provenance.
#   The Q_Refereed_Vol1 scalars should be inspected separately.
#
# NULL MIRROR: NQ1_AtomicSpectra
#   Chaos null: uniform random over same energy range
#   Scramble null: shuffled assignment
#
# OUTPUT:
#   Q-Series/Q1_AtomicSpectra/lake/q1_atomic_spectra_raw.jsonl  (copy/source)
#   vol5/lakes/inputs_promoted/q1_atomic_spectra_promoted.jsonl
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

# Paths — script lives at Q-Series/Q1_AtomicSpectra/scripts/
SCRIPTS_DIR = Path(__file__).resolve().parent
Q1_DIR      = SCRIPTS_DIR.parent
Q_SERIES    = Q1_DIR.parent
VOL5_ROOT   = Q_SERIES.parent
PROMOTED    = VOL5_ROOT / "lakes" / "inputs_promoted"

RAW_INPUT   = Q1_DIR / "lake" / "q1_atomic_spectra_raw.jsonl"
OUTPUT_PATH = PROMOTED / "q1_atomic_spectra_promoted.jsonl"

# --------------------------------------------------------------------
# Scalar function
# --------------------------------------------------------------------

def compute_scalar(rec):
    """
    scalar = log(upper_energy_cm1 + 1) / log(k_geo)
    upper_energy_cm1: upper state energy in wavenumbers.
    Returns float or None.
    """
    energy = rec.get("upper_energy_cm1") or rec.get("secondary_value")
    if energy is None:
        return None
    try:
        e = float(energy)
        if e <= 0:
            return None
        return math.log(e + 1.0) / LOG_K
    except (TypeError, ValueError):
        return None

# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------

def main():
    print("=" * 60)
    print("Q1 Atomic Spectra Lake Builder")
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
            else:
                failed += 1
                s = 0.0

            records.append({
                "entity_id":   str(uuid.uuid4()),
                "domain":      "quantum",
                "volume":      5,
                "lake_id":     "q1_atomic_spectra",
                "geometry_payload": {
                    "coordinates":    [],
                    "dimensionality": 0,
                    "geometry_type":  "unknown",
                },
                "scalar_kls":  s,
                "scalar_klc":  s,
                "meta": {
                    "source":          "NIST Atomic Spectra Database (ASD) — Empirical",
                    "ingest_timestamp": now_ts,
                    "sovereign":        True,
                    "audit_status":     "mondy_verified_2026-04",
                    "scalarization":    "log(upper_energy_cm1 + 1) / log(k_geo)",
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
    print("Next: add q1_atomic_spectra to configs/volumes.json")
    print("      domain: quantum, scale_rank: 0")

if __name__ == "__main__":
    main()