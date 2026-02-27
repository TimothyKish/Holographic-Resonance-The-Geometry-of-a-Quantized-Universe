#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kish_CHIME_Lab_Decoder_v6.1
---------------------------
Shadow cadence analysis using v4.1 lineage-preserved outputs.
- Consumes v4.1 categorized + pure anomalies
- Computes cadence descriptors
- Preserves event_id, tns_name, local_index
- Preserves MATCH, Tech1, Tech2, known_signatures
- Preserves carrier-lock metadata
- Outputs to v6.1-only namespace
"""

import json
import numpy as np
from pathlib import Path
from typing import Any, Dict, List

V41_PURE = Path("outputs_v4_1") / "kish_pure_anomalies_v4_1.json"
V41_CAT = Path("outputs_v4_1") / "kish_categorized_payloads_v4_1.json"

OUTPUT_DIR = Path("outputs_v6_1")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = OUTPUT_DIR / "kish_cadence_v6_1.json"
def compute_cadence_descriptors(record: Dict[str, Any]) -> Dict[str, float]:
    """
    Computes cadence descriptors from raw_event fields.
    This is conceptual and non-interpretive.
    """
    raw = record["raw_event"]

    dm = float(raw.get("dm_fitb", 0.0))
    width = float(raw.get("width_fitb", 0.0)) * 1000.0
    snr = float(raw.get("snr_fitb", 0.0))
    flux = float(raw.get("flux", 0.0))

    eps = 1e-6

    dm_width_ratio = dm / (width + eps)
    snr_log = np.log1p(max(snr, 0.0))
    composite = dm_width_ratio * snr_log

    return {
        "dm_width_ratio": dm_width_ratio,
        "snr_log": snr_log,
        "composite_cadence": composite,
        "base_width_ms": width,
        "base_dm": dm,
        "base_flux": flux
    }
def run_v6_1():
    print("--- KISH LATTICE: CADENCE ANALYZER V6.1 ---")

    # Load v4.1 outputs
    records = []
    if V41_PURE.exists():
        with V41_PURE.open("r", encoding="utf-8") as f:
            records.extend(json.load(f))
    if V41_CAT.exists():
        with V41_CAT.open("r", encoding="utf-8") as f:
            records.extend(json.load(f))

    print(f"[*] Loaded {len(records)} v4.1 lineage records.")

    results = []

    for rec in records:
        cadence = compute_cadence_descriptors(rec)

        out = {
            # Lineage
            "event_id": rec["event_id"],
            "tns_name": rec["tns_name"],
            "local_index": rec["local_index"],

            # v4.1 tags
            "match": rec["match"],
            "tech1": rec["tech1"],
            "tech2": rec["tech2"],
            "known_signatures": rec["known_signatures"],

            # Carrier lock
            "prime_locked_node": rec["prime_locked_node"],
            "lattice_beat": rec["lattice_beat"],
            "is_prime_lock": rec["is_prime_lock"],

            # Cadence descriptors
            "dm_width_ratio": cadence["dm_width_ratio"],
            "snr_log": cadence["snr_log"],
            "composite_cadence": cadence["composite_cadence"],
            "base_width_ms": cadence["base_width_ms"],
            "base_dm": cadence["base_dm"],
            "base_flux": cadence["base_flux"],

            # Full evidence + raw event preserved
            "signature_evidence": rec["signature_evidence"],
            "raw_event": rec["raw_event"]
        }

        results.append(out)

    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"[+] Cadence analysis saved to: {OUTPUT_PATH}")
    print(f"[+] Total processed: {len(results)}")
if __name__ == "__main__":
    run_v6_1()
