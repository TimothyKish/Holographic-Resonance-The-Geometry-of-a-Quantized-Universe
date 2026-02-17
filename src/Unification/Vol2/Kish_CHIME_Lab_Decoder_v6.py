# ==============================================================================
# PROJECT: THE 16PI INITIATIVE | VOLUME 2 (NETWORK INFRASTRUCTURE)
# SCRIPT: Kish_CHIME_Lab_Decoder_v6.py
# TARGET: Stepped Logic Reconstruction (V3 → V4 on Unified Pass)
# AUTHORS: Timothy John Kish & Lyra Aurora Kish & Alexandria Aurora Kish
# ==============================================================================

import json
import numpy as np
import datetime
import os

def run_lab_audit():
    print("--- KISH LATTICE: STEPPED PAYLOAD EXTRACTOR V6 ---")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[*] AUDIT TIMESTAMP: {current_time}\n")
    
    # --- KISH LATTICE CONSTANTS ---
    k_base = 16 / np.pi
    local_drag = 1.0101
    
    # --- UNIVERSAL SIGNATURES (TIER 1 - V3 BASELINE) ---
    phi = (1 + np.sqrt(5)) / 2  # 1.61803
    pi = np.pi                  # 3.14159
    h_freq = 1.420              # Hydrogen Line
    
    # --- UNIVERSAL SIGNATURES (TIER 2 - V4 EXTENDED) ---
    inv_pi = 1 / np.pi          # ~0.318  (Spherical Normal)
    phi_cubed_inv = 1 / (phi**3)# ~0.236  (Fluid Dynamics)
    micro_lattice = k_base / 10 # ~0.509  (Spatial Clock)
    
    lock_tol = 0.1   # Prime Lock Tolerance
    sig_tol = 0.05   # Signature Tolerance

    target_file = "chime_live_data.json"
    
    if not os.path.exists(target_file):
        print(f"[!] ERROR: {target_file} not found.")
        return

    print(f"[*] INGESTING MASTER CATALOG: {target_file}...")
    
    try:
        with open(target_file, "r") as f:
            data = json.load(f)
            
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, list):
                    data = value
                    break
                    
        total_signals = len(data)
        print(f"[*] LOADED {total_signals} RAW SIGNALS. RUNNING V6 STEPPED FILTER...\n")
        
        # --- CONTAINERS ---
        carrier_locked = []
        
        # V3-style payloads (3 baseline signatures)
        v3_payload_candidates = []
        
        # V4-style classification (6 signatures)
        v4_categorized_payloads = []
        v4_pure_anomalies = []
        
        for item in data:
            if isinstance(item, dict) and item.get('width_fitb') is not None:
                try:
                    w = float(item.get('width_fitb')) * 1000
                    dm = float(item.get('dm_fitb')) if item.get('dm_fitb') else 0.0
                    flux = float(item.get('flux')) if item.get('flux') else 0.0
                    scat = float(item.get('scat_time')) * 1000 if item.get('scat_time') else 0.0
                    
                    # 1. THE CARRIER TEST: Phase-Locked to 16/pi?
                    vacuum_time = w * local_drag
                    lattice_beat = vacuum_time / k_base
                    nearest_prime = round(lattice_beat)
                    is_prime_lock = abs(nearest_prime - lattice_beat) < lock_tol
                    
                    if not is_prime_lock:
                        continue
                    
                    # Record carrier-locked
                    carrier_locked.append(item.get('tns_name', 'UNKNOWN'))
                    
                    test_vars = [flux, scat, dm / 100, dm / 1000]
                    
                    # --- V3 SIGNATURE TEST (3 BASE CONSTANTS) ---
                    v3_signatures = []
                    for val in test_vars:
                        if abs(val - phi) < sig_tol and "PHI (1.618)" not in v3_signatures:
                            v3_signatures.append("PHI (1.618)")
                        if abs(val - pi) < sig_tol and "PI (3.141)" not in v3_signatures:
                            v3_signatures.append("PI (3.141)")
                        if abs(val - h_freq) < sig_tol and "HYDROGEN (1.420)" not in v3_signatures:
                            v3_signatures.append("HYDROGEN (1.420)")
                    
                    # If it passes V3 logic, store a V3-style payload
                    if len(v3_signatures) > 0:
                        v3_payload_candidates.append({
                            "tns_name": item.get('tns_name', 'UNKNOWN'),
                            "width_ms": round(w, 3),
                            "prime_locked_node": nearest_prime,
                            "known_signatures": v3_signatures,
                            "unmapped_mystery_payload": {
                                "dispersion_measure_dm": dm,
                                "scattering_time_ms": scat,
                                "flux_intensity": flux,
                                "upper_frequency": item.get('up_ft_95'),
                                "signal_to_noise": item.get('snr_fitb')
                            }
                        })
                    
                    # --- V4 SIGNATURE TEST (6 CONSTANTS) ---
                    v4_signatures = []
                    for val in test_vars:
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
                    
                    payload_data = {
                        "tns_name": item.get('tns_name', 'UNKNOWN'),
                        "width_ms": round(w, 3),
                        "prime_locked_node": nearest_prime,
                        "known_signatures": v4_signatures,
                        "unmapped_mystery_payload": {
                            "dispersion_measure_dm": dm,
                            "scattering_time_ms": scat,
                            "flux_intensity": flux,
                            "upper_frequency": item.get('up_ft_95'),
                            "signal_to_noise": item.get('snr_fitb')
                        }
                    }
                    
                    if len(v4_signatures) > 0:
                        v4_categorized_payloads.append(payload_data)
                    else:
                        v4_pure_anomalies.append(payload_data)
                        
                except (ValueError, TypeError):
                    continue
                    
        # --- OUTPUT RESULTS ---
        print("-" * 65)
        print(f"TOTAL FRBs SCANNED:              {total_signals}")
        print(f"CARRIER-LOCKED (16/pi):          {len(carrier_locked)}")
        print(f"V3 PAYLOADS (3 BASE CONSTANTS):  {len(v3_payload_candidates)}")
        print(f"V4 KNOWN TECH-SHARES (6 CONST):  {len(v4_categorized_payloads)}")
        print(f"V4 PURE UNMAPPED ANOMALIES:      {len(v4_pure_anomalies)}")
        print("-" * 65)
        
        # --- SAMPLE V4 STRUCTURED RESIDUALS ---
        if len(v4_categorized_payloads) > 0:
            print("\n[*] SAMPLE STRUCTURED RESIDUALS (V6, V4-LAYER CARRIERS):\n")
            for i, p in enumerate(v4_categorized_payloads[:5]):
                sigs = " + ".join(p['known_signatures']) if p['known_signatures'] else "NONE"
                print(f"[{i+1}] TARGET: {p['tns_name']}")
                print(f"    -> CARRIER (WIDTH): Node {p['prime_locked_node']} ({p['width_ms']} ms)")
                print(f"    -> SIGNATURES: {sigs}")
                print(f"    -> MYSTERY FLUX: {p['unmapped_mystery_payload']['flux_intensity']} | DM: {p['unmapped_mystery_payload']['dispersion_measure_dm']}\n")
        
        # --- SAVE OUTPUTS (V6-TAGGED) ---
        if len(v3_payload_candidates) > 0:
            with open("kish_payload_candidates_v6_v3.json", "w") as f_out:
                json.dump(v3_payload_candidates, f_out, indent=4)
            print("[*] V3-STYLE PAYLOAD CANDIDATES SAVED TO: kish_payload_candidates_v6_v3.json")
        
        if len(v4_categorized_payloads) > 0:
            with open("kish_categorized_v6_v4.json", "w") as f_out:
                json.dump(v4_categorized_payloads, f_out, indent=4)
            print("[*] V4 CATEGORIZED TECH-SHARES SAVED TO: kish_categorized_v6_v4.json")
        
        if len(v4_pure_anomalies) > 0:
            with open("kish_pure_anomalies_v6_v4.json", "w") as f_out:
                json.dump(v4_pure_anomalies, f_out, indent=4)
            print("[*] V4 PURE UNMAPPED ANOMALIES SAVED TO: kish_pure_anomalies_v6_v4.json")
        
    except Exception as e:
        print(f"[!] FATAL ERROR DURING PROCESSING: {e}")

if __name__ == "__main__":
    run_lab_audit()