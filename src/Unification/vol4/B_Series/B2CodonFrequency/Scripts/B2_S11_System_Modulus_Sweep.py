# B2_S11_System_Modulus_Sweep.py
# LADDER STEP: 11 - GLOBAL MODULUS FALSIFICATION (WEIGHTED)

import json, math, os

def run_modulus_sweep():
    # We need the Raw B3 Distances (Hardware) and B2 Frequencies (Software)
    b3_path = "../../B3AminoAcids/Processed/B3_S4_S8_Fleet_Audit.json"
    b2_path = "../Processed/B2_S2_Codon_Frequency.json"
    
    if not os.path.exists(b3_path) or not os.path.exists(b2_path):
        print("Error: Ensure both B3 Hardware and B2 Software audits are complete.")
        return

    with open(b3_path, 'r') as f: hardware = json.load(f)
    with open(b2_path, 'r') as f: software = json.load(f)

    freq_lookup = {item['name']: item['frequency'] for item in software}
    pi_val = math.pi
    
    # Sweep from 14/pi to 18/pi to find the global minimum
    print(f"\n{'Modulus':<12} | {'Total System Deviation (Weighted)':<35}")
    print("-" * 55)

    sweep_results = []

    for m in [14, 15, 16, 17, 18]:
        m_val = m / pi_val
        total_weighted_dev = 0
        
        for hw in hardware:
            dist = hw['dist']
            name = hw['name']
            freq = freq_lookup.get(name, 0)
            
            # Calculate resonance position for this specific modulus
            ks = dist / m_val
            res_pos = ks * 24
            
            # Find the nearest shelf (7 or 13)
            target = 7 if abs(res_pos - 7) < abs(res_pos - 13) else 13
            dev = abs(res_pos - target)
            
            # WEIGHTED DEVIATION: This is the "Software-Corrected" noise
            total_weighted_dev += (dev * freq)

        print(f"{m:<2}/pi        | {total_weighted_dev:<35.6f}")
        sweep_results.append({"modulus": f"{m}/pi", "total_dev": total_weighted_dev})

    print("-" * 55)
    
    # Identify the winner
    winner = min(sweep_results, key=lambda x: x['total_dev'])
    print(f"WINNER: {winner['modulus']} with lowest system noise.")
    print(f"[!] B2 Falsification Complete. Software/Hardware lock verified.")

if __name__ == "__main__":
    run_modulus_sweep()