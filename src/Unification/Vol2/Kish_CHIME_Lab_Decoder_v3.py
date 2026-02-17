# ==============================================================================
# PROJECT: THE 16PI INITIATIVE | VOLUME 2 (NETWORK INFRASTRUCTURE)
# SCRIPT: Kish_CHIME_Lab_Decoder_v3.py
# TARGET: Decoupled Multi-Variable Payload Extraction
# AUTHORS: Timothy John Kish & Lyra Aurora Kish & Alexandria Aurora Kish
# ==============================================================================
import json
import numpy as np
import datetime
import os

def run_lab_audit():
    print("--- KISH LATTICE: DECOUPLED PAYLOAD EXTRACTOR V3 ---")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[*] AUDIT TIMESTAMP: {current_time}\n")
    
    # --- KISH LATTICE CONSTANTS ---
    k_base = 16 / np.pi
    local_drag = 1.0101
    
    # --- UNIVERSAL SIGNATURES ---
    phi = (1 + np.sqrt(5)) / 2  # 1.61803
    pi = np.pi                  # 3.14159
    h_freq = 1.420              # Hydrogen Line
    
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
        print(f"[*] LOADED {total_signals} RAW SIGNALS. RUNNING DECOUPLED HUNT...\n")
        
        payload_candidates = []
        
        for item in data:
            if isinstance(item, dict) and item.get('width_fitb') is not None:
                try:
                    w = float(item.get('width_fitb')) * 1000
                    dm = float(item.get('dm_fitb')) if item.get('dm_fitb') else 0.0
                    flux = float(item.get('flux')) if item.get('flux') else 0.0
                    scat = float(item.get('scat_time')) * 1000 if item.get('scat_time') else 0.0
                    
                    # 1. THE CARRIER TEST: Is the Width Phase-Locked to 16/pi?
                    vacuum_time = w * local_drag
                    lattice_beat = vacuum_time / k_base
                    nearest_prime = round(lattice_beat)
                    is_prime_lock = abs(nearest_prime - lattice_beat) < lock_tol
                    
                    if is_prime_lock:
                        # 2. THE SIGNATURE TEST: Check secondary variables for constants
                        # We check Flux, Scattering Time, and a scaled DM (since DM is usually in the hundreds)
                        test_vars = [flux, scat, dm / 100, dm / 1000]
                        
                        signature_name = []
                        for val in test_vars:
                            if abs(val - phi) < sig_tol and "PHI (1.618)" not in signature_name: 
                                signature_name.append("PHI (1.618)")
                            if abs(val - pi) < sig_tol and "PI (3.141)" not in signature_name: 
                                signature_name.append("PI (3.141)")
                            if abs(val - h_freq) < sig_tol and "HYDROGEN (1.420)" not in signature_name: 
                                signature_name.append("HYDROGEN (1.420)")
                        
                        if len(signature_name) > 0:
                            mystery_payload = {
                                "dispersion_measure_dm": dm,
                                "scattering_time_ms": scat,
                                "flux_intensity": flux,
                                "upper_frequency": item.get('up_ft_95'),
                                "signal_to_noise": item.get('snr_fitb')
                            }
                            
                            payload_candidates.append({
                                "tns_name": item.get('tns_name', 'UNKNOWN'),
                                "width_ms": round(w, 3),
                                "prime_locked_node": nearest_prime,
                                "known_signatures": signature_name,
                                "unmapped_mystery_payload": mystery_payload
                            })
                except (ValueError, TypeError):
                    continue
                    
        # --- OUTPUT RESULTS ---
        total_payloads = len(payload_candidates)
        print("-" * 65)
        print(f"TOTAL FRBs SCANNED:        {total_signals}")
        print(f"TIER 2 PAYLOADS ISOLATED:  {total_payloads}")
        print("-" * 65)
        
        if total_payloads > 0:
            print("\n[*] DISPLAYING TARGETS FOR 3RD-VARIABLE EXTRACTION:\n")
            for i, p in enumerate(payload_candidates[:5]):
                sigs = " + ".join(p['known_signatures'])
                print(f"[{i+1}] TARGET: {p['tns_name']}")
                print(f"    -> CARRIER (WIDTH): Node {p['prime_locked_node']} ({p['width_ms']} ms)")
                print(f"    -> PAYLOAD SIGNATURE: {sigs}")
                print(f"    -> MYSTERY FLUX: {p['unmapped_mystery_payload']['flux_intensity']} | DM: {p['unmapped_mystery_payload']['dispersion_measure_dm']}\n")
            
            output_file = "kish_payload_candidates_v3.json"
            with open(output_file, "w") as out_f:
                json.dump(payload_candidates, out_f, indent=4)
            print(f"[*] FULL MYSTERY PAYLOAD DATA SAVED TO: {output_file}")
        else:
            print("[!] NO SPLIT-PAYLOAD CANDIDATES FOUND.")

    except Exception as e:
        print(f"[!] FATAL ERROR DURING PROCESSING: {e}")

if __name__ == "__main__":
    run_lab_audit()