#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kish_CHIME_Lab_Decoder_v4.1
---------------------------
Shadow-analysis re-run of v4 with:
- full lineage preservation
- full raw-event retention
- full signature evidence (all tests)
- grouped evidence by variable
- MATCH flag
- Tech1 / Tech2 tagging
- carrier-lock metadata
"""

import json
import numpy as np
import datetime
from pathlib import Path
from typing import Any, Dict, List

# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

INPUT_PATH = Path("chime_live_data.json")
OUTPUT_DIR = Path("outputs_v4_1")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PURE_ANOMALIES_PATH = OUTPUT_DIR / "kish_pure_anomalies_v4_1.json"
CATEGORIZED_PATH = OUTPUT_DIR / "kish_categorized_payloads_v4_1.json"

# ---------------------------------------------------------------------
# Constants (full precision + rounded)
# ---------------------------------------------------------------------

phi_full = (1 + np.sqrt(5)) / 2
phi_round = round(phi_full, 6)

pi_full = np.pi
pi_round = round(pi_full, 6)

h_freq_full = 1.420
h_freq_round = round(h_freq_full, 6)

inv_pi_full = 1 / np.pi
inv_pi_round = round(inv_pi_full, 6)

phi_cubed_inv_full = 1 / (phi_full ** 3)
phi_cubed_inv_round = round(phi_cubed_inv_full, 6)

k_base_full = 16 / np.pi
micro_lattice_full = k_base_full / 10
micro_lattice_round = round(micro_lattice_full, 6)

lock_tol = 0.1
sig_tol = 0.05
local_drag = 1.0101

# Signature dictionary for iteration
SIGNATURES = [
    ("PHI (1.618)", phi_full, phi_round),
    ("PI (3.141)", pi_full, pi_round),
    ("HYDROGEN (1.420)", h_freq_full, h_freq_round),
    ("INV_PI (0.318 - Spherical Normal)", inv_pi_full, inv_pi_round),
    ("PHI_CUBED_INV (0.236 - Fluid Dynamics)", phi_cubed_inv_full, phi_cubed_inv_round),
    ("MICRO_LATTICE (0.509 - Spatial Clock)", micro_lattice_full, micro_lattice_round),
]
def carrier_test(width_ms: float) -> Dict[str, Any]:
    """
    Performs the 16/pi carrier lock test.
    Returns lattice_beat, nearest_prime, is_prime_lock.
    """
    vacuum_time = width_ms * local_drag
    lattice_beat = vacuum_time / k_base_full
    nearest_prime = round(lattice_beat)
    is_prime_lock = abs(nearest_prime - lattice_beat) < lock_tol

    return {
        "lattice_beat": lattice_beat,
        "nearest_prime": nearest_prime,
        "is_prime_lock": is_prime_lock
    }
def build_signature_evidence(flux: float, scat: float, dm: float) -> Dict[str, List[Dict[str, Any]]]:
    """
    Builds grouped evidence (Option B) with full test list (Option A).
    Each variable group contains all comparisons to all 6 signatures.
    """
    evidence = {
        "flux": [],
        "scat": [],
        "dm_over_100": [],
        "dm_over_1000": []
    }

    test_values = {
        "flux": flux,
        "scat": scat,
        "dm_over_100": dm / 100.0,
        "dm_over_1000": dm / 1000.0
    }

    for var_name, value in test_values.items():
        for sig_name, const_full, const_round in SIGNATURES:
            diff = abs(value - const_full)
            evidence[var_name].append({
                "compared_to": sig_name,
                "constant_value_full": const_full,
                "constant_value_round": const_round,
                "value": value,
                "difference": diff,
                "within_tolerance": bool(diff < sig_tol)
            })

    return evidence
def extract_signature_matches(evidence: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    """
    Scans evidence for matches and returns:
    - match (bool)
    - tech1
    - tech2
    - known_signatures (list)
    """
    matches = []

    for var_group in evidence.values():
        for test in var_group:
            if test["within_tolerance"]:
                matches.append(test["compared_to"])

    match_flag = len(matches) > 0
    tech1 = matches[0] if len(matches) > 0 else "UNKNOWN"
    tech2 = matches[1] if len(matches) > 1 else "UNKNOWN"

    return {
        "match": match_flag,
        "tech1": tech1,
        "tech2": tech2,
        "known_signatures": matches
    }
def run_v4_1():
    print("--- KISH LATTICE: DEEP FILTER PAYLOAD EXTRACTOR V4.1 ---")

    if not INPUT_PATH.exists():
        print(f"[!] ERROR: {INPUT_PATH} not found.")
        return

    with INPUT_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        for v in data.values():
            if isinstance(v, list):
                data = v
                break

    categorized = []
    pure_anomalies = []

    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            continue
        if item.get("width_fitb") is None:
            continue

        try:
            w_ms = float(item["width_fitb"]) * 1000.0
            dm = float(item.get("dm_fitb", 0.0))
            flux = float(item.get("flux", 0.0))
            scat = float(item.get("scat_time", 0.0)) * 1000.0

            # Carrier test
            carrier = carrier_test(w_ms)
            if not carrier["is_prime_lock"]:
                continue

            # Evidence
            evidence = build_signature_evidence(flux, scat, dm)
            sig = extract_signature_matches(evidence)

            record = {
                "event_id": item.get("event_id"),
                "tns_name": item.get("tns_name", "UNKNOWN"),
                "local_index": idx,

                "width_ms": w_ms,
                "prime_locked_node": carrier["nearest_prime"],
                "lattice_beat": carrier["lattice_beat"],
                "is_prime_lock": carrier["is_prime_lock"],

                "match": sig["match"],
                "tech1": sig["tech1"],
                "tech2": sig["tech2"],
                "known_signatures": sig["known_signatures"],

                "signature_evidence": evidence,
                "raw_event": item
            }

            if sig["match"]:
                categorized.append(record)
            else:
                pure_anomalies.append(record)

        except Exception:
            continue

    with CATEGORIZED_PATH.open("w", encoding="utf-8") as f:
        json.dump(categorized, f, indent=2)

    with PURE_ANOMALIES_PATH.open("w", encoding="utf-8") as f:
        json.dump(pure_anomalies, f, indent=2)

    print(f"[+] Categorized saved: {len(categorized)}")
    print(f"[+] Pure anomalies saved: {len(pure_anomalies)}")
if __name__ == "__main__":
    run_v4_1()
