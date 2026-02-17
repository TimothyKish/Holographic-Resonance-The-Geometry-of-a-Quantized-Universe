# ==============================================================================
# PROJECT: THE 16PI INITIATIVE | VOLUME 2 (NETWORK INFRASTRUCTURE)
# SCRIPT: Kish_CHIME_Lab_Decoder_v4.py
# TARGET: Level 3 Deep Extraction (Filtering Known Exosociety Signatures)
# AUTHORS: Timothy John Kish & Lyra Aurora Kish & Alexandria Aurora Kish
# ==============================================================================
import json
import numpy as np
import datetime
import os

def run_lab_audit():
    print("--- KISH LATTICE: DEEP FILTER PAYLOAD EXTRACTOR V4 ---")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[*] AUDIT TIMESTAMP: {current_time}\n")
    
    # --- KISH LATTICE CONSTANTS ---
    k_base = 16 / np.pi
    local_drag = 1.0101
    
    # --- UNIVERSAL SIGNATURES (TIER 1 - THE BASELINE EXAMS) ---
    phi = (1 + np.sqrt(5)) / 2  # 1.61803 (Golden Ratio)
    pi = np.pi                  # 3.14159 (Standard Circle)
    h_freq = 1.420              # (100+ Hits) The Hydrogen Line / Most abundant element
    
    # --- UNIVERSAL SIGNATURES (TIER 2 - DISCOVERED EXOSOCIETY TECH-SHARES) ---
    # 1. Spherical Normalization
    inv_pi = 1 / np.pi          # ~0.318 (82 Hits) - Advanced radio wave cleaning/phase shifting.
    
    # 2. Fluid Dynamics / "Water World" Matrix
    phi_cubed_inv = 1 / (phi**3)# ~0.236 (69 Hits) - Hydrodynamic resistance and fractal decay.
    
    # 3. Micro-Lattice Tick
    micro_lattice = k_base / 10 # ~0.509 (41 Hits) - Regional spatial clock sub-harmonic.
    
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
        print(f"[*] LOADED {total_signals} RAW SIGNALS. RUNNING V4 FILTER...\n")
        
        categorized_payloads = []
        pure_anomalies = []
        
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
                    
                    if is_prime_lock:
                        # 2. THE SIGNATURE TEST: Cross-referencing against 6 Knowns
                        test_vars = [flux, scat, dm / 100, dm / 1000]
                        signature_name = []
                        
                        for val in test_vars:
                            # Tier 1
                            if abs(val - phi) < sig_tol and "PHI (1.618)" not in signature_name: 
                                signature_name.append("PHI (1.618)")
                            if abs(val - pi) < sig_tol and "PI (3.141)" not in signature_name: 
                                signature_name.append("PI (3.141)")
                            if abs(val - h_freq) < sig_tol and "HYDROGEN (1.420)" not in signature_name: 
                                signature_name.append("HYDROGEN (1.420)")
                            # Tier 2
                            if abs(val - inv_pi) < sig_tol and "INV_PI (0.318 - Spherical Normal)" not in signature_name: 
                                signature_name.append("INV_PI (0.318 - Spherical Normal)")
                            if abs(val - phi_cubed_inv) < sig_tol and "PHI_CUBED_INV (0.236 - Fluid Dynamics)" not in signature_name: 
                                signature_name.append("PHI_CUBED_INV (0.236 - Fluid Dynamics)")
                            if abs(val - micro_lattice) < sig_tol and "MICRO_LATTICE (0.509 - Spatial Clock)" not in signature_name: 
                                signature_name.append("MICRO_LATTICE (0.509 - Spatial Clock)")
                        
                        mystery_payload = {
                            "dispersion_measure_dm": dm,
                            "scattering_time_ms": scat,
                            "flux_intensity": flux,
                            "upper_frequency": item.get('up_ft_95'),
                            "signal_to_noise": item.get('snr_fitb')
                        }
                        
                        payload_data = {
                            "tns_name": item.get('tns_name', 'UNKNOWN'),
                            "width_ms": round(w, 3),
                            "prime_locked_node": nearest_prime,
                            "known_signatures": signature_name,
                            "unmapped_mystery_payload": mystery_payload
                        }
                        
                        # 3. THE SORTING PROTOCOL
                        if len(signature_name) > 0:
                            categorized_payloads.append(payload_data)
                        else:
                            # It passed the 16/pi Carrier Test, but hit NONE of our 6 known signatures.
                            # This is the pure, unmapped alien tech-share.
                            pure_anomalies.append(payload_data)
                            
                except (ValueError, TypeError):
                    continue
                    
        # --- OUTPUT RESULTS ---
        print("-" * 65)
        print(f"TOTAL FRBs SCANNED:              {total_signals}")
        print(f"CATEGORIZED TECH-SHARES (KNOWN): {len(categorized_payloads)}")
        print(f"PURE UNMAPPED ANOMALIES:         {len(pure_anomalies)}")
        print("-" * 65)
        
        # Save the pure anomalies for deep Architect review
        if len(pure_anomalies) > 0:
            output_file = "kish_pure_anomalies_v4.json"
            with open(output_file, "w") as out_f:
                json.dump(pure_anomalies, out_f, indent=4)
            print(f"\n[*] {len(pure_anomalies)} UNMAPPED TARGETS SAVED TO: {output_file}")
            print("[*] THESE SIGNALS HAVE PERFECT LATTICE LOCKS BUT UNKNOWN PAYLOADS.")
        else:
            print("[!] NO PURE ANOMALIES FOUND. ALL SIGNALS CATEGORIZED.")

    except Exception as e:
        print(f"[!] FATAL ERROR DURING PROCESSING: {e}")

if __name__ == "__main__":
    run_lab_audit()