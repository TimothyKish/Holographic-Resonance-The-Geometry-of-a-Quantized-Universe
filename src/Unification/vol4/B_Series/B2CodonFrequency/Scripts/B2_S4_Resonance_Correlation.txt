# B2_S4_Resonance_Correlation.py
# LADDER STEP: 4 - HARDWARE/SOFTWARE CORRELATION (REVISED PATHS)

import json, os

def run_correlation():
    # UPDATED PATH: Pointing to your actual B3 file name
    b3_audit_path = "../../B3AminoAcids/Processed/B3_S4_S8_Fleet_Audit.json"
    b2_freq_path = "../Processed/B2_S2_Codon_Frequency.json"
    
    if not os.path.exists(b3_audit_path):
        print(f"Error: B3 Hardware Audit not found at {b3_audit_path}")
        return

    with open(b3_audit_path, 'r') as f:
        hardware = json.load(f)
    with open(b2_freq_path, 'r') as f:
        software = json.load(f)

    # Create a lookup for software frequency
    freq_lookup = {item['name']: item['frequency'] for item in software}

    print(f"\n{'Amino Acid':<20} | {'B3 Dev (HW)':<12} | {'Codons (SW)':<12} | {'Burden Score':<12}")
    print("-" * 70)

    results = []
    for hw in hardware:
        name = hw['name']
        dev = hw['deviation']
        sw_freq = freq_lookup.get(name, 0)
        
        # Calculate the "Resonance Burden" (Dev * Frequency)
        # Higher number = High redundancy for high noise
        burden = dev * sw_freq 
        
        results.append({
            "name": name,
            "hardware_dev": dev,
            "software_freq": sw_freq,
            "burden": round(burden, 4)
        })
        
        print(f"{name:<20} | {dev:<12.6f} | {sw_freq:<12} | {burden:<12.4f}")

    with open("../Processed/B2_S4_Correlation_Summary.json", "w") as out:
        out.write(json.dumps(results, indent=4))
    
    print(f"\n[!] B2 Correlation Complete. Hardware/Software bridge established.")

if __name__ == "__main__":
    run_correlation()