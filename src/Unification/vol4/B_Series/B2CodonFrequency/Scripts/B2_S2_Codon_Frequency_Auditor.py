# B2_S2_Codon_Frequency_Auditor.py
# LADDER STEP: 2 - SOFTWARE FREQUENCY AUDIT

import json, os

def run_frequency_audit():
    lake_dir = "../Lake/"
    processed_dir = "../Processed/"
    os.makedirs(processed_dir, exist_ok=True)
    
    # Load the Map
    with open(f"{lake_dir}B2_S1_Codon_Map_lake.jsonl", "r") as f:
        codon_map = json.loads(f.readline())

    # Map the Frequency (How many codons per Amino Acid)
    # Using 1-letter codes as the key
    freq_map = {}
    for codon, aa in codon_map.items():
        if aa == "_": continue # Skip Stop Codons for the resonance audit
        freq_map[aa] = freq_map.get(aa, 0) + 1

    # Standard 20-mode mapping (1-letter to Name for B3/B1 alignment)
    AA_REFS = {
        'A': 'Alanine', 'R': 'Arginine', 'N': 'Asparagine', 'D': 'Aspartic_Acid',
        'C': 'Cysteine', 'E': 'Glutamic_Acid', 'Q': 'Glutamine', 'G': 'Glycine',
        'H': 'Histidine', 'I': 'Isoleucine', 'L': 'Leucine', 'K': 'Lysine',
        'M': 'Methionine', 'F': 'Phenylalanine', 'P': 'Proline', 'S': 'Serine',
        'T': 'Threonine', 'W': 'Tryptophan', 'Y': 'Tyrosine', 'V': 'Valine'
    }

    results = []
    print(f"{'Amino Acid':<20} | {'Codon Count':<12}")
    print("-" * 35)
    
    for code, name in AA_REFS.items():
        count = freq_map.get(code, 0)
        results.append({"name": name, "symbol": code, "frequency": count})
        print(f"{name:<20} | {count:<12}")

    with open(f"{processed_dir}B2_S2_Codon_Frequency.json", "w") as out:
        out.write(json.dumps(results, indent=4))
    
    print(f"\n[!] Frequency Audit complete. Data stored in Processed for B3 Correlation.")

if __name__ == "__main__":
    run_frequency_audit()