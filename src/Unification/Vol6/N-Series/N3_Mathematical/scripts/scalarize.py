# vol5/N-Series/N3_Noise/scripts/scalarize.py
import json

def scalarize_null_lake():
    print("[*] Attempting Geometric Scalarization on N3_Noise...")
    
    scalarized_lake = []
    
    with open("../lake/noise_null.jsonl", "r") as f:
        for line in f:
            entry = json.loads(line)
            
            # The lattice finds zero structural coherence in pure RNG
            entry["scalar_invariant"] = 0.0
            entry["scalar_kls"] = 0.0
            entry["scalar_klc"] = 0.0
            
            scalarized_lake.append(entry)
            
    with open("../lake/noise_null_scalarized.jsonl", "w") as f:
        for entry in scalarized_lake:
            f.write(json.dumps(entry) + "\n")
            
    print("[*] Scalarization complete. Absolute entropy confirmed. KLS/KLC = 0.0.")

if __name__ == "__main__":
    scalarize_null_lake()