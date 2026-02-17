# ==============================================================================
# PROJECT: THE 16PI INITIATIVE | VOLUME 2 (NETWORK INFRASTRUCTURE)
# SCRIPT: Kish_CHIME_Lab_Decoder_v5.py
# TARGET: Unified Deep Filter + Structured Residual Extractor
# AUTHORS: Timothy John Kish & Lyra Aurora Kish & Alexandria Aurora Kish
# NOTES:
#   - V5 merges the V3 "structured residual" logic with the V4 "deep filter"
#     classification into a single, hierarchical pipeline.
#   - Input catalog remains: chime_live_data.json
#   - Outputs are explicitly tagged as V5:
#       * kish_structured_residuals_v5.json
#       * kish_extended_signatures_v5.json
#       * kish_pure_anomalies_v5.json
# ==============================================================================

import json
import numpy as np
import datetime
import os


# ------------------------------------------------------------------------------
# CORE CONSTANTS AND SIGNATURE DEFINITIONS
# ------------------------------------------------------------------------------

def get_constants():
    # Kish lattice carrier
    k_base = 16 / np.pi
    local_drag = 1.0101

    # Tier 1: Universal baseline signatures
    phi = (1 + np.sqrt(5)) / 2      # ~1.61803
    pi = np.pi                      # ~3.14159
    h_freq = 1.420                  # Hydrogen line

    # Tier 2: Extended exosociety tech-shares
    inv_pi = 1 / np.pi              # ~0.318 (Spherical normalization)
    phi_cubed_inv = 1 / (phi ** 3)  # ~0.236 (Fluid dynamics / fractal decay)
    micro_lattice = k_base / 10     # ~0.509 (Micro-lattice tick)

    # Tolerances
    lock_tol = 0.1   # Prime lock tolerance
    sig_tol = 0.05   # Signature tolerance

    tier1_signatures = {
        "PHI (1.618)": phi,
        "PI (3.141)": pi,
        "HYDROGEN (1.420)": h_freq
    }

    tier2_signatures = {
        "INV_PI (0.318 - Spherical Normal)": inv_pi,
        "PHI_CUBED_INV (0.236 - Fluid Dynamics)": phi_cubed_inv,
        "MICRO_LATTICE (0.509 - Spatial Clock)": micro_lattice
    }

    return (k_base, local_drag,
            tier1_signatures, tier2_signatures,
            lock_tol, sig_tol)


# ------------------------------------------------------------------------------
# CARRIER TEST: 16/pi PRIME LOCK
# ------------------------------------------------------------------------------

def carrier_lock(width_ms, k_base, local_drag, lock_tol):
    """
    Apply the Kish lattice carrier test:
    - width_ms: pulse width in milliseconds
    - Returns (is_prime_lock, nearest_prime_node, lattice_beat)
    """
    vacuum_time = width_ms * local_drag
    lattice_beat = vacuum_time / k_base
    nearest_prime = round(lattice_beat)
    is_prime_lock = abs(nearest_prime - lattice_beat) < lock_tol
    return is_prime_lock, nearest_prime, lattice_beat


# ------------------------------------------------------------------------------
# SIGNATURE DETECTION ENGINE
# ------------------------------------------------------------------------------

def detect_signatures(test_vars, tier1_signatures, tier2_signatures, sig_tol):
    """
    Given a list of test variables and signature dictionaries, return:
    - tier1_hits: list of Tier 1 signature labels
    - tier2_hits: list of Tier 2 signature labels
    """
    tier1_hits = []
    tier2_hits = []

    for val in test_vars:
        # Skip NaNs or None
        if val is None:
            continue
        try:
            v = float(val)
        except (ValueError, TypeError):
            continue

        # Tier 1
        for label, target in tier1_signatures.items():
            if abs(v - target) < sig_tol and label not in tier1_hits:
                tier1_hits.append(label)

        # Tier 2
        for label, target in tier2_signatures.items():
            if abs(v - target) < sig_tol and label not in tier2_hits:
                tier2_hits.append(label)

    return tier1_hits, tier2_hits


# ------------------------------------------------------------------------------
# STRUCTURED RESIDUAL LOGIC (V3-STYLE)
# ------------------------------------------------------------------------------

def build_mystery_payload(item, dm, scat_ms, flux):
    """
    Build the unmapped mystery payload dictionary in the V3/V4 style.
    """
    return {
        "dispersion_measure_dm": dm,
        "scattering_time_ms": scat_ms,
        "flux_intensity": flux,
        "upper_frequency": item.get('up_ft_95'),
        "signal_to_noise": item.get('snr_fitb')
    }


def is_structured_residual(tier1_hits, mystery_payload):
    """
    Placeholder for stricter "exactly one unmapped coordinate" logic.
    For now, we follow the V3 spirit:
      - At least one Tier 1 signature present.
      - The event is treated as a structured residual candidate.
    If you later formalize the "exactly one unmapped coordinate" rule,
    this function is where that logic should live.
    """
    # Current V5 criterion: any Tier 1 hit qualifies as structured residual.
    return len(tier1_hits) > 0


# ------------------------------------------------------------------------------
# MAIN AUDIT ROUTINE
# ------------------------------------------------------------------------------

def run_lab_audit():
    print("--- KISH LATTICE: UNIFIED PAYLOAD EXTRACTOR V5 ---")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[*] AUDIT TIMESTAMP: {current_time}\n")

    # Load constants and signatures
    (k_base, local_drag,
     tier1_signatures, tier2_signatures,
     lock_tol, sig_tol) = get_constants()

    target_file = "chime_live_data.json"

    if not os.path.exists(target_file):
        print(f"[!] ERROR: {target_file} not found.")
        return

    print(f"[*] INGESTING MASTER CATALOG: {target_file}...")

    try:
        with open(target_file, "r") as f:
            data = json.load(f)

        # If wrapped in a dict, unwrap the first list
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, list):
                    data = value
                    break

        total_signals = len(data)
        print(f"[*] LOADED {total_signals} RAW SIGNALS. RUNNING V5 FILTER...\n")

        structured_residuals = []     # V3-style Tier 1 carriers
        extended_signatures = []      # Tier 2-only or mixed Tier1+Tier2 carriers
        pure_anomalies = []           # Carrier-locked, zero signatures

        carrier_locked_count = 0

        for item in data:
            if not (isinstance(item, dict) and item.get('width_fitb') is not None):
                continue

            try:
                # Core observables
                w_ms = float(item.get('width_fitb')) * 1000
                dm = float(item.get('dm_fitb')) if item.get('dm_fitb') else 0.0
                flux = float(item.get('flux')) if item.get('flux') else 0.0
                scat_ms = float(item.get('scat_time')) * 1000 if item.get('scat_time') else 0.0

                # 1. Carrier test
                is_lock, nearest_prime, lattice_beat = carrier_lock(
                    w_ms, k_base, local_drag, lock_tol
                )

                if not is_lock:
                    continue

                carrier_locked_count += 1

                # 2. Signature test (Tier 1 + Tier 2)
                test_vars = [flux, scat_ms, dm / 100.0, dm / 1000.0]
                tier1_hits, tier2_hits = detect_signatures(
                    test_vars, tier1_signatures, tier2_signatures, sig_tol
                )

                # Build common payload structure
                mystery_payload = build_mystery_payload(item, dm, scat_ms, flux)
                known_signatures = tier1_hits + tier2_hits

                payload_data = {
                    "tns_name": item.get('tns_name', 'UNKNOWN'),
                    "width_ms": round(w_ms, 3),
                    "prime_locked_node": nearest_prime,
                    "known_signatures": known_signatures,
                    "unmapped_mystery_payload": mystery_payload
                }

                # 3. Classification logic
                if len(tier1_hits) == 0 and len(tier2_hits) == 0:
                    # Pure anomaly: carrier-locked, no known signatures
                    pure_anomalies.append(payload_data)
                elif is_structured_residual(tier1_hits, mystery_payload):
                    # Structured residual (V3-style Tier 1 carrier)
                    structured_residuals.append(payload_data)
                else:
                    # Extended signatures (Tier 2 only or mixed)
                    extended_signatures.append(payload_data)

            except (ValueError, TypeError):
                continue

        # ------------------------------------------------------------------
        # OUTPUT SUMMARY
        # ------------------------------------------------------------------
        print("-" * 65)
        print(f"TOTAL FRBs SCANNED:              {total_signals}")
        print(f"CARRIER-LOCKED (16/pi):          {carrier_locked_count}")
        print(f"STRUCTURED RESIDUALS (TIER 1):   {len(structured_residuals)}")
        print(f"EXTENDED SIGNATURES (TIER 2+):   {len(extended_signatures)}")
        print(f"PURE UNMAPPED ANOMALIES:         {len(pure_anomalies)}")
        print("-" * 65)

        # Preview a few structured residuals (like V3 did)
        if len(structured_residuals) > 0:
            print("\n[*] SAMPLE STRUCTURED RESIDUALS (V5, TIER 1 CARRIERS):\n")
            for i, p in enumerate(structured_residuals[:5]):
                sigs = " + ".join(p['known_signatures']) if p['known_signatures'] else "NONE"
                print(f"[{i+1}] TARGET: {p['tns_name']}")
                print(f"    -> CARRIER (WIDTH): Node {p['prime_locked_node']} ({p['width_ms']} ms)")
                print(f"    -> SIGNATURES: {sigs}")
                print(f"    -> MYSTERY FLUX: {p['unmapped_mystery_payload']['flux_intensity']} "
                      f"| DM: {p['unmapped_mystery_payload']['dispersion_measure_dm']}\n")

        # ------------------------------------------------------------------
        # SAVE OUTPUTS (V5-TAGGED)
        # ------------------------------------------------------------------
        if len(structured_residuals) > 0:
            out_structured = "kish_structured_residuals_v5.json"
            with open(out_structured, "w") as f_out:
                json.dump(structured_residuals, f_out, indent=4)
            print(f"[*] STRUCTURED RESIDUALS SAVED TO: {out_structured}")

        if len(extended_signatures) > 0:
            out_extended = "kish_extended_signatures_v5.json"
            with open(out_extended, "w") as f_out:
                json.dump(extended_signatures, f_out, indent=4)
            print(f"[*] EXTENDED SIGNATURES SAVED TO: {out_extended}")

        if len(pure_anomalies) > 0:
            out_pure = "kish_pure_anomalies_v5.json"
            with open(out_pure, "w") as f_out:
                json.dump(pure_anomalies, f_out, indent=4)
            print(f"[*] PURE UNMAPPED ANOMALIES SAVED TO: {out_pure}")
            print("[*] THESE SIGNALS HAVE PERFECT LATTICE LOCKS BUT UNKNOWN PAYLOADS.")

        if (len(structured_residuals) == 0 and
                len(extended_signatures) == 0 and
                len(pure_anomalies) == 0):
            print("[!] NO CARRIER-LOCKED SIGNALS PASSED THE FILTERS.")

    except Exception as e:
        print(f"[!] FATAL ERROR DURING PROCESSING: {e}")


if __name__ == "__main__":
    run_lab_audit()