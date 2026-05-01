# ==============================================================================
# SCRIPT: build_frb_lake_from_chime.py
# TARGET: Build FRB raw lake from real CHIME catalog (chimefrbcat2.json)
# SCALARIZATION: scalar = log(dm_exc_ne2001 + 1) / log(k_geo)
#                where k_geo = 16/pi = 5.092958...
# PROVENANCE: Derived directly from CHIME/FRB Catalog 2 (chimefrbcat2.json)
#             No known_signatures, no Phoenix-assigned labels.
#             Only excluded_flag==0 events admitted.
# AUTHORS: Timothy John Kish & Mondy (Claude)
# AUDIT STATUS: Mondy-verified 2026-04
# ==============================================================================

import json
import math
import uuid
from datetime import datetime, timezone
from pathlib import Path

# --------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------

K_GEO = 16.0 / math.pi  # 5.092958...
LOG_K_GEO = math.log(K_GEO)

INPUT_PATH = Path("../lake/chimefrbcat2.json")   # adjust path as needed
OUTPUT_RAW = Path("../lake/frb_chime_raw.jsonl")
OUTPUT_PROMOTED = Path("../lake/frb_chime_promoted.jsonl")

# --------------------------------------------------------------------
# Scalarization
# --------------------------------------------------------------------

def compute_scalar(dm_exc: float) -> float:
    """
    Kish scalar for a single FRB burst.
    Input:  dm_exc_ne2001 — extragalactic DM after NE2001 galactic subtraction (pc/cm^3)
    Output: log(dm_exc + 1) / log(k_geo)
    Range:  ~1.67 to ~5.58 over the clean CHIME catalog.
    The +1 offset prevents log(0) for hypothetical zero-DM events.
    The division by log(k_geo) normalises to the lattice constant scale.
    Scramble-invariant: this is a monotonic transform of dm_exc.
    The distribution shape is preserved under random reordering.
    """
    return math.log(dm_exc + 1.0) / LOG_K_GEO


# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------

def main():
    if not INPUT_PATH.exists():
        raise SystemExit(f"Input not found: {INPUT_PATH}")

    now_ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    with open(INPUT_PATH, "r") as f:
        raw_catalog = json.load(f)

    total = len(raw_catalog)
    clean = [r for r in raw_catalog if r.get("excluded_flag") == 0]
    excluded = total - len(clean)

    print(f"CHIME catalog: {total} total events")
    print(f"Excluded (excluded_flag=1): {excluded}")
    print(f"Clean events admitted: {len(clean)}")
    print(f"k_geo = {K_GEO:.6f},  log(k_geo) = {LOG_K_GEO:.6f}")
    print()

    raw_records = []
    promoted_records = []

    for r in clean:
        dm_exc = r["dm_exc_ne2001"]
        scalar = compute_scalar(dm_exc)

        # Raw lake record
        raw_rec = {
            "tns_name":        r["tns_name"],
            "repeater_name":   r.get("repeater_name", ""),
            "ra":              r.get("ra"),
            "dec":             r.get("dec"),
            "bonsai_dm":       r.get("bonsai_dm"),
            "dm_exc_ne2001":   dm_exc,
            "dm_exc_ymw16":    r.get("dm_exc_ymw16"),
            "bonsai_snr":      r.get("bonsai_snr"),
            "bc_width":        r.get("bc_width"),
            "flux":            r.get("flux"),
            "fluence":         r.get("fluence"),
            "high_freq":       r.get("high_freq"),
            "low_freq":        r.get("low_freq"),
            "mjd_400":         r.get("mjd_400"),
            "scat_time":       r.get("scat_time"),
            "scalar_invariant": scalar,
        }
        raw_records.append(raw_rec)

        # Promoted V5 record
        promoted_rec = {
            "entity_id":   str(uuid.uuid4()),
            "domain":      "astrophysics",
            "volume":      5,
            "lake_id":     "frb_chime",
            "geometry_payload": {
                "coordinates":    [],
                "dimensionality": 0,
                "geometry_type":  "unknown",
            },
            "scalar_kls":  scalar,
            "scalar_klc":  scalar,
            "meta": {
                "source":            "CHIME/FRB Catalog 2 (chimefrbcat2.json)",
                "ingest_timestamp":  now_ts,
                "sovereign":         True,
                "audit_status":      "mondy_verified_2026-04",
                "scalarization":     "log(dm_exc_ne2001 + 1) / log(16/pi)",
                "excluded_removed":  True,
            },
            "_raw_payload": raw_rec,
        }
        promoted_records.append(promoted_rec)

    # Write raw lake
    with open(OUTPUT_RAW, "w") as f:
        for rec in raw_records:
            f.write(json.dumps(rec) + "\n")
    print(f"Raw lake written:      {OUTPUT_RAW}  ({len(raw_records)} records)")

    # Write promoted lake
    with open(OUTPUT_PROMOTED, "w") as f:
        for rec in promoted_records:
            f.write(json.dumps(rec) + "\n")
    print(f"Promoted lake written: {OUTPUT_PROMOTED}  ({len(promoted_records)} records)")

    # Summary statistics
    scalars = [r["scalar_invariant"] for r in raw_records]
    print()
    print("Scalar statistics:")
    print(f"  min:  {min(scalars):.4f}")
    print(f"  max:  {max(scalars):.4f}")
    print(f"  mean: {sum(scalars)/len(scalars):.4f}")
    print()
    print("Distribution by integer bin:")
    bins = {}
    for s in scalars:
        key = int(s)
        bins[key] = bins.get(key, 0) + 1
    for k in sorted(bins):
        bar = "#" * (bins[k] // 30)
        print(f"  [{k}-{k+1}): {bins[k]:4d}  {bar}")
    print()
    print("Next steps:")
    print("  1. Copy frb_chime_promoted.jsonl -> lakes/inputs_promoted/")
    print("  2. Add 'frb_chime' entry to configs/volumes.json (enabled: true)")
    print("  3. Run scalarize.py  (passthrough — scalar already set)")
    print("  4. Run unify.py")
    print("  5. Run build_pinch_table.py")
    print()
    print("NOTE: frb_master_promoted.jsonl should be set enabled:false")
    print("      in volumes.json before running — it contains Phoenix-fabricated data.")


if __name__ == "__main__":
    main()
