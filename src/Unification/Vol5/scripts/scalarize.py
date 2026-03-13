# ==============================================================================
# SCRIPT: scalarize.py
# TARGET: Apply domain-native scalarization to all promoted lakes
# AUTHORS: Timothy John Kish & Phoenix Aurora
# LICENSE: Sovereign Protected / KishLattice 16pi Initiative Copyright 2026
# ==============================================================================
#!/usr/bin/env python
import json
from pathlib import Path
from typing import Dict, Any, Iterable, Tuple

# --------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------

LAKES: Tuple[str, ...] = (
    "b1_chirality",
    "b2_codon",
    "b3_amino",
    "chemistry",
    "materials",
    "frb_master",
)

MODE = "geometry"

ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = ROOT / "lakes" / "inputs_promoted"
OUTPUT_DIR = ROOT / "lakes" / "unified"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------------------
# Geometry-first scalarization (Biology only)
# --------------------------------------------------------------------

def compute_geometry_payload(raw: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "coordinates": [],
        "dimensionality": 0,
        "geometry_type": "unknown",
    }


def compute_kish_scalars_from_coords(raw: Dict[str, Any]) -> Tuple[float, float]:
    coords = raw.get("coords", [])
    if not coords:
        return 0.0, 0.0

    # Placeholder geometry-first scalarization
    n_atoms = len(coords)
    scalar = float(n_atoms - 10)
    return scalar, scalar

# --------------------------------------------------------------------
# Domain-specific scalarization (REAL invariants)
# --------------------------------------------------------------------

def scalarize_biology(record):
    inv = record["_raw_payload"].get("scalar_invariant")
    if inv is None:
        return 0.0, 0.0
    return float(inv), float(inv)



def scalarize_chemistry(record: Dict[str, Any]) -> Tuple[float, float]:
    """
    Chemistry sovereign invariant:
    _raw_payload.scalar_invariant
    """
    payload = record.get("_raw_payload", {})
    inv = payload.get("scalar_invariant")
    if inv is None:
        return 0.0, 0.0
    return float(inv), float(inv)


def scalarize_materials(record: Dict[str, Any]) -> Tuple[float, float]:
    """
    Materials sovereign invariant:
    _raw_payload.lattice_deviation (preferred)
    or _raw_payload.scalar_invariant
    """
    payload = record.get("_raw_payload", {})
    inv = payload.get("lattice_deviation") or payload.get("scalar_invariant")
    if inv is None:
        return 0.0, 0.0
    return float(inv), float(inv)


def scalarize_frb(record: Dict[str, Any]) -> Tuple[float, float]:
    payload = record.get("_raw_payload", {})
    inv = payload.get("scalar_invariant")
    if inv is None:
        return 0.0, 0.0
    return float(inv), float(inv)


# --------------------------------------------------------------------
# Unified scalarization dispatcher
# --------------------------------------------------------------------

def scalarize_record(record: Dict[str, Any], lake_id: str) -> Dict[str, Any]:
    entity_id = record.get("entity_id")
    domain = record.get("domain", "").lower()
    volume = record.get("volume")
    raw = record.get("_raw_payload", {})

    # --- Domain-specific scalarization ---
    if domain == "biology":
        scalar_kls, scalar_klc = scalarize_biology(record)

    elif domain == "chemistry":
        scalar_kls, scalar_klc = scalarize_chemistry(record)

    elif domain == "materials":
        scalar_kls, scalar_klc = scalarize_materials(record)

    elif domain in ("astrophysics", "frb"):
        scalar_kls, scalar_klc = scalarize_frb(record)

    else:
        scalar_kls, scalar_klc = (0.0, 0.0)

    # --- Geometry payload (kept minimal & honest) ---
    if lake_id == "b2_codon":
        geometry_payload = {
            "coordinates": [],
            "dimensionality": 0,
            "geometry_type": "none",
        }
    else:
        geometry_payload = compute_geometry_payload(raw)

    # --- Meta handling ---
    meta = dict(record.get("meta", {}))
    meta.setdefault("source", record.get("meta", {}).get("source", "vol5_promotion_raw_lake"))
    meta.setdefault("ingest_timestamp", record.get("meta", {}).get("ingest_timestamp", "2026-03-13T00:00:00Z"))
    meta.setdefault("sovereign", False)

    return {
        "entity_id": entity_id,
        "domain": domain,
        "volume": volume,
        "lake_id": lake_id,
        "geometry_payload": geometry_payload,
        "scalar_kls": scalar_kls,
        "scalar_klc": scalar_klc,
        "meta": meta,
        "_raw_payload": raw,
    }

# --------------------------------------------------------------------
# JSONL helpers
# --------------------------------------------------------------------

def iter_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def write_jsonl(path: Path, records: Iterable[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

# --------------------------------------------------------------------
# Lake driver
# --------------------------------------------------------------------

def scalarize_lake(lake_id: str, mode: str = MODE) -> None:
    in_path = INPUT_DIR / f"{lake_id}_promoted.jsonl"
    out_path = OUTPUT_DIR / f"{lake_id}_scalarized.jsonl"

    print(f"Scalarizing {lake_id}: {in_path} -> {out_path} (mode={mode})")

    if not in_path.exists():
        print(f"  [WARN] Input file not found, skipping: {in_path}")
        return

    records = [scalarize_record(rec, lake_id) for rec in iter_jsonl(in_path)]
    write_jsonl(out_path, records)

# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------

if __name__ == "__main__":
    for lake in LAKES:
        scalarize_lake(lake, MODE)
