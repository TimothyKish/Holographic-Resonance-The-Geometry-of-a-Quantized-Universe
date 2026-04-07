# ==============================================================================
# SCRIPT: scalarize.py
# TARGET: Apply domain-native scalarization to all promoted lakes
# AUTHORS: Timothy John Kish
# AUDIT STATUS: Mondy-verified 2026-04
# CHANGE: Added fallback to preserve existing scalar_kls when domain
#         scalarization returns zero (e.g. chemistry, materials, frb_chime
#         which embed scalar_kls directly in the promoted record).
# LICENSE: Sovereign Protected / KishLattice 16pi Initiative Copyright 2026
# ==============================================================================
#!/usr/bin/env python
import json
from pathlib import Path
from typing import Dict, Any, Iterable, Tuple

# --------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "configs"
INPUT_DIR = ROOT / "lakes" / "inputs_promoted"
OUTPUT_DIR = ROOT / "lakes" / "unified"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_enabled_lakes():
    """Load all enabled lakes from volumes.json."""
    cfg = json.load(open(CONFIG_DIR / "volumes.json", "r", encoding="utf-8"))
    volumes = cfg.get("volumes", {})
    return tuple(name for name, meta in volumes.items() if meta.get("enabled", False))


LAKES = load_enabled_lakes()
MODE = "geometry"


# --------------------------------------------------------------------
# Geometry-first scalarization (placeholder)
# --------------------------------------------------------------------

def compute_geometry_payload(raw: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "coordinates": [],
        "dimensionality": 0,
        "geometry_type": "unknown",
    }


# --------------------------------------------------------------------
# Domain-specific scalarization
# --------------------------------------------------------------------

def scalarize_biology(record):
    payload = record.get("_raw_payload", {}) or {}
    inv = payload.get("scalar_invariant")
    return (float(inv), float(inv)) if inv is not None else (0.0, 0.0)


def scalarize_chemistry(record):
    payload = record.get("_raw_payload", {}) or {}
    inv = payload.get("scalar_invariant")
    return (float(inv), float(inv)) if inv is not None else (0.0, 0.0)


def scalarize_materials(record):
    payload = record.get("_raw_payload", {}) or {}
    inv = payload.get("lattice_deviation") or payload.get("scalar_invariant")
    return (float(inv), float(inv)) if inv is not None else (0.0, 0.0)


def scalarize_frb(record):
    payload = record.get("_raw_payload", {}) or {}
    inv = payload.get("scalar_invariant")
    return (float(inv), float(inv)) if inv is not None else (0.0, 0.0)


def scalarize_null(record):
    """Null lakes always scalarize to zero."""
    return 0.0, 0.0


# --------------------------------------------------------------------
# Unified scalarization dispatcher
# --------------------------------------------------------------------

def scalarize_record(record: Dict[str, Any], lake_id: str) -> Dict[str, Any]:
    entity_id = record.get("entity_id")
    domain = (record.get("domain") or "").lower()
    volume = record.get("volume")
    raw = record.get("_raw_payload", {}) or {}

    # --- Domain normalization ---
    if domain in ("mechanical", "behavioral", "mathematical", "cosmological_null"):
        domain_group = "null"
    else:
        domain_group = domain

    # --- Domain-specific scalarization ---
    if domain_group == "biology":
        scalar_kls, scalar_klc = scalarize_biology(record)

    elif domain_group == "chemistry":
        scalar_kls, scalar_klc = scalarize_chemistry(record)

    elif domain_group == "materials":
        scalar_kls, scalar_klc = scalarize_materials(record)

    elif domain_group in ("astrophysics", "frb", "stellar", "planetary", "cosmology"):
        scalar_kls, scalar_klc = scalarize_frb(record)

    elif domain_group == "null":
        scalar_kls, scalar_klc = scalarize_null(record)

    else:
        scalar_kls, scalar_klc = (0.0, 0.0)

    # --- Fallback: preserve existing scalar_kls when scalarization returns zero ---
    # Some lakes (chemistry, materials, frb_chime) compute their scalar upstream
    # and embed it directly as scalar_kls in the promoted record.
    # Without this fallback, re-running scalarize.py overwrites them with zeros.
    if scalar_kls == 0.0 and scalar_klc == 0.0:
        existing_kls = record.get("scalar_kls", 0.0)
        if existing_kls != 0.0:
            scalar_kls = existing_kls
            scalar_klc = record.get("scalar_klc", existing_kls)

    # --- Geometry payload ---
    geometry_payload = compute_geometry_payload(raw)

    # --- Meta handling ---
    meta = dict(record.get("meta", {}))
    meta.setdefault("source", "vol5_promotion_raw_lake")
    meta.setdefault("ingest_timestamp", "2026-03-13T00:00:00Z")
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