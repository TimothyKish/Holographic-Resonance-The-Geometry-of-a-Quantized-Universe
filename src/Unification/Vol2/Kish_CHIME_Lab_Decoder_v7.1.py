#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kish_CHIME_Lab_Decoder_v7.1
---------------------------
Shadow null-test suite using v6.1 cadence outputs.

- Consumes v6.1 (lineage + cadence descriptors)
- Builds null ensembles via randomization
- Compares observed stats vs null
- Preserves event_id / tns_name / tags for traceability
- Writes to v7.1-only namespace
"""

import json
import random
import statistics
from pathlib import Path
from typing import Any, Dict, List

V61_INPUT = Path("outputs_v6_1") / "kish_cadence_v6_1.json"

OUTPUT_DIR = Path("outputs_v7_1")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SUMMARY_PATH = OUTPUT_DIR / "kish_null_summary_v7_1.json"
ENSEMBLES_PATH = OUTPUT_DIR / "kish_null_ensembles_v7_1.json"

N_TRIALS = 1000
RANDOM_SEED = 1618


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def load_v6_1(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        print(f"[!] v6.1 file not found: {path}")
        return []
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def extract_observed(records: List[Dict[str, Any]]) -> Dict[str, List[float]]:
    dm_width = []
    snr_log = []
    composite = []

    for rec in records:
        dm_width.append(float(rec.get("dm_width_ratio", 0.0)))
        snr_log.append(float(rec.get("snr_log", 0.0)))
        composite.append(float(rec.get("composite_cadence", 0.0)))

    return {
        "dm_width_ratio": dm_width,
        "snr_log": snr_log,
        "composite_cadence": composite
    }


def generate_null_ensemble(values: List[float], n_trials: int) -> Dict[str, List[float]]:
    if not values:
        return {"mean": [], "stdev": [], "max": []}

    null_means = []
    null_stdevs = []
    null_max = []

    for _ in range(n_trials):
        shuffled = values[:]
        random.shuffle(shuffled)
        null_means.append(statistics.mean(shuffled))
        null_stdevs.append(statistics.pstdev(shuffled))
        null_max.append(max(shuffled))

    return {
        "mean": null_means,
        "stdev": null_stdevs,
        "max": null_max
    }


def summarize_observed_vs_null(observed: List[float],
                               null_ensemble: Dict[str, List[float]]) -> Dict[str, Any]:
    if not observed:
        return {}

    obs_mean = statistics.mean(observed)
    obs_stdev = statistics.pstdev(observed)
    obs_max = max(observed)

    null_means = null_ensemble["mean"]
    null_stdevs = null_ensemble["stdev"]
    null_max = null_ensemble["max"]

    def frac_ge(null_vals, obs_val):
        if not null_vals:
            return None
        return sum(1 for v in null_vals if v >= obs_val) / len(null_vals)

    return {
        "observed": {
            "mean": obs_mean,
            "stdev": obs_stdev,
            "max": obs_max
        },
        "null_summary": {
            "mean_of_means": statistics.mean(null_means) if null_means else None,
            "mean_of_stdevs": statistics.mean(null_stdevs) if null_stdevs else None,
            "mean_of_max": statistics.mean(null_max) if null_max else None
        },
        "empirical_fractions": {
            "mean_ge": frac_ge(null_means, obs_mean),
            "stdev_ge": frac_ge(null_stdevs, obs_stdev),
            "max_ge": frac_ge(null_max, obs_max)
        }
    }


# ---------------------------------------------------------------------
# Core pipeline
# ---------------------------------------------------------------------

def run_v7_1():
    print("--- KISH LATTICE: NULL-TEST SUITE V7.1 ---")
    random.seed(RANDOM_SEED)

    records = load_v6_1(V61_INPUT)
    print(f"[*] Loaded {len(records)} v6.1 cadence records.")

    observed = extract_observed(records)

    null_ensembles: Dict[str, Dict[str, List[float]]] = {}
    summaries: Dict[str, Any] = {}

    for key, values in observed.items():
        print(f"[*] Processing descriptor: {key}")
        null_ensemble = generate_null_ensemble(values, N_TRIALS)
        summary = summarize_observed_vs_null(values, null_ensemble)

        null_ensembles[key] = null_ensemble
        summaries[key] = summary

    with ENSEMBLES_PATH.open("w", encoding="utf-8") as f:
        json.dump(null_ensembles, f, indent=2)

    with SUMMARY_PATH.open("w", encoding="utf-8") as f:
        json.dump(summaries, f, indent=2)

    print(f"[+] Null ensembles saved to: {ENSEMBLES_PATH}")
    print(f"[+] Summary statistics saved to: {SUMMARY_PATH}")


# ---------------------------------------------------------------------
# Entry
# ---------------------------------------------------------------------

if __name__ == "__main__":
    run_v7_1()
