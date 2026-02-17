#!/usr/bin/env python3
# Kish_CHIME_Lab_Decoder_v7.py
# KISH LATTICE: STEPPED PAYLOAD EXTRACTOR V7 (LADDER ~43)

import json
import math
import os
from datetime import datetime

MASTER_CATALOG = "chime_live_data.json"

# ---------------------------------------------------------------------
# Global constants (copied from V6)
# ---------------------------------------------------------------------

k_base = 16.0 / math.pi
local_drag = 1.0101

# Tier 1 (V3)
phi = (1 + math.sqrt(5)) / 2.0   # 1.618...
pi = math.pi                     # 3.141...
h_freq = 1.420                   # Hydrogen line

# Tier 2 (V4)
inv_pi = 1.0 / math.pi           # ~0.318
phi_cubed_inv = 1.0 / (phi ** 3) # ~0.236
micro_lattice = k_base / 10.0    # ~0.509

lock_tol = 0.1   # Prime lock tolerance
sig_tol = 0.05   # Signature tolerance

# ---------------------------------------------------------------------
# Utility I/O
# ---------------------------------------------------------------------

def load_catalog(path):
    with open(path, "r") as f:
        data = json.load(f)
    # Handle possible dict-wrapped list (as in some CHIME dumps)
    if isinstance(data, dict):
        for _, value in data.items():
            if isinstance(value, list):
                return value
    return data

def save_json(path, obj):
    with open(path, "w") as f:
        json.dump(obj, f, indent=4, sort_keys=False)

def now_stamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ---------------------------------------------------------------------
# V6 logic, factored into helpers
# ---------------------------------------------------------------------

def extract_raw_fields(frb):
    """Mirror V6 field extraction from raw CHIME catalog."""
    try:
        w_ms = float(frb.get("width_fitb")) * 1000.0 if frb.get("width_fitb") is not None else None
    except (TypeError, ValueError):
        w_ms = None

    try:
        dm = float(frb.get("dm_fitb")) if frb.get("dm_fitb") else 0.0
    except (TypeError, ValueError):
        dm = 0.0

    try:
        flux = float(frb.get("flux")) if frb.get("flux") else 0.0
    except (TypeError, ValueError):
        flux = 0.0

    try:
        scat_ms = float(frb.get("scat_time")) * 1000.0 if frb.get("scat_time") else 0.0
    except (TypeError, ValueError):
        scat_ms = 0.0

    up_freq = frb.get("up_ft_95")
    snr = frb.get("snr_fitb")

    return w_ms, dm, flux, scat_ms, up_freq, snr

def is_carrier_locked_v6(frb):
    """Exact V6 carrier lock: 16/pi on width_fitb."""
    w_ms, dm, flux, scat_ms, up_freq, snr = extract_raw_fields(frb)
    if w_ms is None or not math.isfinite(w_ms):
        return False

    vacuum_time = w_ms * local_drag
    lattice_beat = vacuum_time / k_base
    nearest_prime = round(lattice_beat)
    is_prime_lock = abs(nearest_prime - lattice_beat) < lock_tol
    return is_prime_lock

def v6_prime_locked_node(frb):
    """Return the V6 prime-locked node index."""
    w_ms, dm, flux, scat_ms, up_freq, snr = extract_raw_fields(frb)
    vacuum_time = w_ms * local_drag
    lattice_beat = vacuum_time / k_base
    nearest_prime = round(lattice_beat)
    return nearest_prime

def classify_v3_payload(frb):
    """
    V3-style payload classification (3 base constants).
    Mirrors V6: test [flux, scat_ms, dm/100, dm/1000] against phi, pi, h_freq.
    """
    w_ms, dm, flux, scat_ms, up_freq, snr = extract_raw_fields(frb)

    test_vars = [flux, scat_ms, dm / 100.0, dm / 1000.0]
    v3_signatures = []

    for val in test_vars:
        if not math.isfinite(val):
            continue
        if abs(val - phi) < sig_tol and "PHI (1.618)" not in v3_signatures:
            v3_signatures.append("PHI (1.618)")
        if abs(val - pi) < sig_tol and "PI (3.141)" not in v3_signatures:
            v3_signatures.append("PI (3.141)")
        if abs(val - h_freq) < sig_tol and "HYDROGEN (1.420)" not in v3_signatures:
            v3_signatures.append("HYDROGEN (1.420)")

    mystery_payload = {
        "dispersion_measure_dm": dm,
        "scattering_time_ms": scat_ms,
        "flux_intensity": flux,
        "upper_frequency": up_freq,
        "signal_to_noise": snr,
    }

    return {
        "known_signatures": v3_signatures,
        "mystery_payload": mystery_payload,
    }

def classify_v4_tech_share(frb, v3_payload):
    """
    V4-style tech-share classification (6 constants).
    Mirrors V6: same test_vars, but with Tier 2 constants added.
    """
    w_ms, dm, flux, scat_ms, up_freq, snr = extract_raw_fields(frb)
    test_vars = [flux, scat_ms, dm / 100.0, dm / 1000.0]

    v4_signatures = []

    for val in test_vars:
        if not math.isfinite(val):
            continue
        # Tier 1
        if abs(val - phi) < sig_tol and "PHI (1.618)" not in v4_signatures:
            v4_signatures.append("PHI (1.618)")
        if abs(val - pi) < sig_tol and "PI (3.141)" not in v4_signatures:
            v4_signatures.append("PI (3.141)")
        if abs(val - h_freq) < sig_tol and "HYDROGEN (1.420)" not in v4_signatures:
            v4_signatures.append("HYDROGEN (1.420)")
        # Tier 2
        if abs(val - inv_pi) < sig_tol and "INV_PI (0.318 - Spherical Normal)" not in v4_signatures:
            v4_signatures.append("INV_PI (0.318 - Spherical Normal)")
        if abs(val - phi_cubed_inv) < sig_tol and "PHI_CUBED_INV (0.236 - Fluid Dynamics)" not in v4_signatures:
            v4_signatures.append("PHI_CUBED_INV (0.236 - Fluid Dynamics)")
        if abs(val - micro_lattice) < sig_tol and "MICRO_LATTICE (0.509 - Spatial Clock)" not in v4_signatures:
            v4_signatures.append("MICRO_LATTICE (0.509 - Spatial Clock)")

    is_known_tech_share = len(v4_signatures) > 0
    return is_known_tech_share, v4_signatures

def is_pure_anomaly_v4(frb, v3_payload, is_tech_share, v4_signatures):
    """
    Mirror V6: pure anomalies are those with NO V4 signatures.
    (V6 does not require V3 signatures to be empty.)
    """
    return len(v4_signatures) == 0

def build_v6_structured_residual(frb, signatures, mystery_payload):
    """Build the V6-style structured residual record."""
    w_ms, dm, flux, scat_ms, up_freq, snr = extract_raw_fields(frb)
    node = v6_prime_locked_node(frb)
    return {
        "tns_name": frb.get("tns_name", "UNKNOWN"),
        "width_ms": round(w_ms, 3) if w_ms is not None else None,
        "prime_locked_node": node,
        "known_signatures": signatures,
        "unmapped_mystery_payload": mystery_payload,
    }

# ---------------------------------------------------------------------
# V7 ladder logic
# ---------------------------------------------------------------------

def ladder_score(residual):
    """
    Scalar ladder score for each structured residual.
    Placeholder: DM * flux / width, with NaN guard.
    """
    payload = residual.get("unmapped_mystery_payload", {})
    dm = payload.get("dispersion_measure_dm", float("nan"))
    flux = payload.get("flux_intensity", float("nan"))
    width = residual.get("width_ms", float("nan"))

    if not (math.isfinite(dm) and math.isfinite(flux) and math.isfinite(width) and width > 0):
        return float("inf")

    return dm * flux / width

def select_v7_ladder(structured_residuals, target_count=43):
    """
    Take V6-style structured residuals and select a V7 ladder subset.
    Force ladder size to ~target_count by cutting at the target-th score.
    """
    if not structured_residuals:
        return []

    scored = []
    for r in structured_residuals:
        s = ladder_score(r)
        scored.append((s, r))

    scored.sort(key=lambda x: x[0])  # smaller score = more special

    k = min(target_count, len(scored))
    ladder = [r for (_, r) in scored[:k]]
    return ladder

# ---------------------------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------------------------

def main():
    print("--- KISH LATTICE: STEPPED PAYLOAD EXTRACTOR V7 ---")
    print(f"[*] AUDIT TIMESTAMP: {now_stamp()}\n")

    if not os.path.exists(MASTER_CATALOG):
        print(f"[!] ERROR: {MASTER_CATALOG} not found.")
        return

    print(f"[*] INGESTING MASTER CATALOG: {MASTER_CATALOG}...")
    catalog = load_catalog(MASTER_CATALOG)
    total_frbs = len(catalog)
    print(f"[*] LOADED {total_frbs} RAW SIGNALS. RUNNING V7 STEPPED FILTER...\n")

    carrier_locked_v7 = []
    v3_payloads_v7 = []
    v4_tech_shares_v7 = []
    v4_pure_anomalies_v7 = []
    v6_structured_residuals_v7 = []

    for frb in catalog:
        if not isinstance(frb, dict):
            continue

        # 1. Carrier lock (exact V6 logic)
        if not is_carrier_locked_v6(frb):
            continue
        carrier_locked_v7.append(frb)

        # 2. V3 payload
        v3_payload = classify_v3_payload(frb)
        v3_payloads_v7.append({
            "tns_name": frb.get("tns_name", "UNKNOWN"),
            "width_ms": extract_raw_fields(frb)[0],
            "prime_locked_node": v6_prime_locked_node(frb),
            "known_signatures": v3_payload["known_signatures"],
            "unmapped_mystery_payload": v3_payload["mystery_payload"],
        })

        # 3. V4 tech-share classification
        is_tech_share, v4_sigs = classify_v4_tech_share(frb, v3_payload)
        if is_tech_share:
            v4_tech_shares_v7.append({
                "tns_name": frb.get("tns_name", "UNKNOWN"),
                "width_ms": extract_raw_fields(frb)[0],
                "prime_locked_node": v6_prime_locked_node(frb),
                "known_signatures": v4_sigs,
                "unmapped_mystery_payload": v3_payload["mystery_payload"],
            })

        # 4. V4 pure anomalies (mirror V6: no V4 signatures)
        if is_pure_anomaly_v4(frb, v3_payload, is_tech_share, v4_sigs):
            v4_pure_anomalies_v7.append({
                "tns_name": frb.get("tns_name", "UNKNOWN"),
                "width_ms": extract_raw_fields(frb)[0],
                "prime_locked_node": v6_prime_locked_node(frb),
                "known_signatures": [],
                "unmapped_mystery_payload": v3_payload["mystery_payload"],
            })

        # 5. V6-style structured residuals (for ladder input)
        residual = build_v6_structured_residual(
            frb,
            signatures=v4_sigs,
            mystery_payload=v3_payload["mystery_payload"],
        )
        v6_structured_residuals_v7.append(residual)

    # 6. V7 ladder selection (~43)
    v7_ladder = select_v7_ladder(v6_structured_residuals_v7, target_count=43)

    # -----------------------------------------------------------------
    # STATS
    # -----------------------------------------------------------------
    n_carrier = len(carrier_locked_v7)
    n_v3 = len(v3_payloads_v7)
    n_v4_tech = len(v4_tech_shares_v7)
    n_v4_anom = len(v4_pure_anomalies_v7)
    n_v6_struct = len(v6_structured_residuals_v7)
    n_v7_ladder = len(v7_ladder)

    print("-----------------------------------------------------------------")
    print(f"TOTAL FRBs SCANNED:              {total_frbs}")
    print(f"CARRIER-LOCKED (V7=V6):          {n_carrier}")
    print(f"V3 PAYLOADS (3 BASE CONSTANTS):  {n_v3}")
    print(f"V4 KNOWN TECH-SHARES (6 CONST):  {n_v4_tech}")
    print(f"V4 PURE UNMAPPED ANOMALIES:      {n_v4_anom}")
    print(f"V6 STRUCTURED RESIDUALS (V7):    {n_v6_struct}")
    print(f"V7 LADDER (TARGET ~43):          {n_v7_ladder}")
    print("-----------------------------------------------------------------\n")

    # -----------------------------------------------------------------
    # SAMPLE PRINT (if available)
    # -----------------------------------------------------------------
    if v7_ladder:
        print("[*] SAMPLE V7 STRUCTURED RESIDUALS (LADDER):")
        for i, r in enumerate(v7_ladder[:5], start=1):
            payload = r.get("unmapped_mystery_payload", {})
            print(f"\n[{i}] TARGET: {r.get('tns_name')}")
            print(f"    -> CARRIER (WIDTH): Node {r.get('prime_locked_node', 0)} ({r.get('width_ms')} ms)")
            print(f"    -> SIGNATURES: {', '.join(r.get('known_signatures', [])) or 'NONE'}")
            print(f"    -> MYSTERY FLUX: {payload.get('flux_intensity')} | DM: {payload.get('dispersion_measure_dm')}")
    else:
        print("[*] SAMPLE V7 STRUCTURED RESIDUALS: NONE (ladder empty)")

    # -----------------------------------------------------------------
    # SAVE OUTPUTS
    # -----------------------------------------------------------------
    save_json("kish_payload_candidates_v7_v3.json", v3_payloads_v7)
    save_json("kish_categorized_v7_v4.json", v4_tech_shares_v7)
    save_json("kish_pure_anomalies_v7_v4.json", v4_pure_anomalies_v7)
    save_json("kish_payload_candidates_v7_v6.json", v6_structured_residuals_v7)
    save_json("kish_structured_residuals_v7.json", v7_ladder)

    print("[*] V3-STYLE PAYLOAD CANDIDATES (V7) SAVED TO: kish_payload_candidates_v7_v3.json")
    print("[*] V4 CATEGORIZED TECH-SHARES (V7) SAVED TO: kish_categorized_v7_v4.json")
    print("[*] V4 PURE UNMAPPED ANOMALIES (V7) SAVED TO: kish_pure_anomalies_v7_v4.json")
    print("[*] V6-STYLE STRUCTURED RESIDUALS (V7) SAVED TO: kish_payload_candidates_v7_v6.json")
    print("[*] V7 LADDER STRUCTURED SET SAVED TO: kish_structured_residuals_v7.json")

if __name__ == "__main__":
    main()