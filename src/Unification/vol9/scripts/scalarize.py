# ==============================================================================
# SCRIPT: scalarize.py
# TARGET: Apply domain-native scalarization to all promoted lakes
# AUTHORS: Timothy John Kish
# AUDIT STATUS: Mondy-verified 2026-04-24
#
# CHANGE LOG:
#   v9.0 2026-04-24: Added domain handlers for 11 new Vol9 sovereign lakes.
#     New domains: nuclear_binding, nuclear_decay, atomic_ionisation,
#     molecular_c60, stellar_cycle, gravitational_wave, planetary_atlantic,
#     planetary_gulf, planetary_pacific, planetary_indian, cmb_anisotropy.
#     New handlers read flat fields directly (no _raw_payload wrapper).
#     Existing handlers unchanged. Fallback preserved.
#   Prior: Added fallback to preserve existing scalar_kls when domain
#     scalarization returns zero.
#
# HOW TO ADD A NEW DOMAIN (Vol10+):
#   1. Add domain to schema.json allowed_domains
#   2. Add scalar formula to schema.json scalar_formulas
#   3. Add a scalarize_X() function below the NEW handlers section
#   4. Add one elif in the dispatch table
#   That is the complete process. No other files need changing.
#
# LICENSE: Sovereign Protected / KishLattice 16pi Initiative Copyright 2026
# ==============================================================================
#!/usr/bin/env python
import json
import math
from pathlib import Path
from typing import Dict, Any, Iterable

ROOT       = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "configs"
INPUT_DIR  = ROOT / "lakes" / "inputs_promoted"
OUTPUT_DIR = ROOT / "lakes" / "unified"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PI    = math.pi
K_GEO = 16.0 / PI
LOG_K = math.log(K_GEO)


def load_enabled_lakes():
    cfg = json.load(open(CONFIG_DIR / "volumes.json", "r", encoding="utf-8"))
    return tuple(n for n, m in cfg.get("volumes", {}).items() if m.get("enabled", False))


LAKES = load_enabled_lakes()
MODE  = "geometry"


def compute_geometry_payload(raw):
    return {"coordinates": [], "dimensionality": 0, "geometry_type": "unknown"}


# ==============================================================================
# EXISTING HANDLERS — unchanged, read from _raw_payload (legacy format)
# ==============================================================================

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
    return 0.0, 0.0


# ==============================================================================
# NEW HANDLERS (Vol9) — read flat fields from promoted records
# ==============================================================================

def _log_scalar(val):
    """Standard: log(val + 1) / log(k_geo). Returns 0.0 if invalid."""
    try:
        fval = float(val)
        if fval < 0: fval = abs(fval)
        if not math.isfinite(fval) or fval == 0: return 0.0
        sc = math.log(fval + 1.0) / LOG_K
        return sc if math.isfinite(sc) else 0.0
    except (TypeError, ValueError):
        return 0.0

def scalarize_nuclear_binding(record):
    sc = _log_scalar(record.get("binding_energy_mev_per_A"))
    return (sc, sc)

def scalarize_nuclear_decay(record):
    """Double-log: log(log(half_life_seconds + 1) + 1) / log(k_geo)"""
    try:
        hl = float(record.get("half_life_seconds", 0))
        if hl <= 0 or not math.isfinite(hl): return (0.0, 0.0)
        inner = math.log(hl + 1.0)
        if inner <= 0: return (0.0, 0.0)
        sc = math.log(inner + 1.0) / LOG_K
        sc = sc if math.isfinite(sc) else 0.0
        return (sc, sc)
    except (TypeError, ValueError):
        return (0.0, 0.0)

def scalarize_atomic_ionisation(record):
    sc = _log_scalar(record.get("ionisation_energy_eV"))
    return (sc, sc)

def scalarize_molecular_c60(record):
    sc = _log_scalar(record.get("frequency_cm1"))
    return (sc, sc)

def scalarize_stellar_cycle(record):
    sc = _log_scalar(record.get("interval_days"))
    return (sc, sc)

def scalarize_gravitational_wave(record):
    sc = _log_scalar(record.get("f_ring_hz"))
    return (sc, sc)

def scalarize_tidal(record):
    sc = _log_scalar(record.get("interval_hours"))
    return (sc, sc)

def scalarize_cmb_anisotropy(record):
    dt = record.get("delta_T_uK")
    if dt is None:
        dl = record.get("Dl_uK2", 0)
        try:
            dl_f = float(dl)
            dt = math.sqrt(dl_f) if dl_f > 0 else 0.0
        except (TypeError, ValueError):
            dt = 0.0
    sc = _log_scalar(dt)
    return (sc, sc)


# ==============================================================================
# DISPATCH TABLE — one elif per domain
# To add a new domain for Vol10+: add handler above, add elif here
# ==============================================================================

def scalarize_record(record, lake_id):
    domain       = (record.get("domain") or "").lower()
    domain_group = domain

    if domain in ("mechanical", "behavioral", "mathematical", "cosmological_null"):
        domain_group = "null"

    # --- Existing domains ---
    if domain_group == "biology":
        scalar_kls, scalar_klc = scalarize_biology(record)
    elif domain_group == "chemistry":
        scalar_kls, scalar_klc = scalarize_chemistry(record)
    elif domain_group == "materials":
        scalar_kls, scalar_klc = scalarize_materials(record)
    elif domain_group in ("astrophysics", "frb", "stellar", "planetary",
                          "cosmology"):
        scalar_kls, scalar_klc = scalarize_frb(record)
    elif domain_group == "null":
        scalar_kls, scalar_klc = scalarize_null(record)

    # --- Vol9 new domains ---
    elif domain_group == "nuclear_binding":
        scalar_kls, scalar_klc = scalarize_nuclear_binding(record)
    elif domain_group == "nuclear_decay":
        scalar_kls, scalar_klc = scalarize_nuclear_decay(record)
    elif domain_group == "atomic_ionisation":
        scalar_kls, scalar_klc = scalarize_atomic_ionisation(record)
    elif domain_group == "molecular_c60":
        scalar_kls, scalar_klc = scalarize_molecular_c60(record)
    elif domain_group == "stellar_cycle":
        scalar_kls, scalar_klc = scalarize_stellar_cycle(record)
    elif domain_group == "gravitational_wave":
        scalar_kls, scalar_klc = scalarize_gravitational_wave(record)
    elif domain_group in ("planetary_atlantic", "planetary_gulf",
                          "planetary_pacific", "planetary_indian"):
        scalar_kls, scalar_klc = scalarize_tidal(record)
    elif domain_group == "cmb_anisotropy":
        scalar_kls, scalar_klc = scalarize_cmb_anisotropy(record)

    else:
        scalar_kls, scalar_klc = (0.0, 0.0)

    # Fallback: use embedded scalar_kls if present and scalarization returned zero
    if scalar_kls == 0.0 and scalar_klc == 0.0:
        existing = record.get("scalar_kls", 0.0)
        if existing != 0.0:
            scalar_kls = existing
            scalar_klc = record.get("scalar_klc", existing)

    raw  = record.get("_raw_payload", {}) or {}
    meta = dict(record.get("meta", {}))
    meta.setdefault("source",           "vol9_promotion_raw_lake")
    meta.setdefault("ingest_timestamp", "2026-04-24T00:00:00Z")
    meta.setdefault("sovereign",        False)

    return {
        "entity_id":        record.get("entity_id"),
        "domain":           domain,
        "volume":           record.get("volume"),
        "lake_id":          lake_id,
        "geometry_payload": compute_geometry_payload(raw),
        "scalar_kls":       scalar_kls,
        "scalar_klc":       scalar_klc,
        "meta":             meta,
        "_raw_payload":     raw,
    }


def iter_jsonl(path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)

def write_jsonl(path, records):
    with path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

def scalarize_lake(lake_id, mode=MODE):
    in_path  = INPUT_DIR  / f"{lake_id}_promoted.jsonl"
    out_path = OUTPUT_DIR / f"{lake_id}_scalarized.jsonl"
    print(f"Scalarizing {lake_id}: {in_path} -> {out_path} (mode={mode})")
    if not in_path.exists():
        print(f"  [WARN] Input not found, skipping: {in_path}")
        return
    records = [scalarize_record(rec, lake_id) for rec in iter_jsonl(in_path)]
    write_jsonl(out_path, records)

if __name__ == "__main__":
    for lake in LAKES:
        scalarize_lake(lake, MODE)