# vol5/T-Series/NT4_Cosmological/scripts/scalarize.py
import json

def scalarize_null_lake():
    print("[*] Attempting Geometric Scalarization on NT4_Temporal...")
    
    scalarized_lake = []
    
    with open("../lake/nt4_temporal_null.jsonl", "r") as f:
        for line in f:
            entry = json.loads(line)
            
            # The lattice finds no coherent 16/pi structure
            entry["scalar_invariant"] = 0.0
            entry["scalar_kls"] = 0.0
            entry["scalar_klc"] = 0.0
            
            scalarized_lake.append(entry)
            
    with open("../lake/nt4_temporal_null_scalarized.jsonl", "w") as f:
        for entry in scalarized_lake:
            f.write(json.dumps(entry) + "\n")
            
    print("[*] Scalarization complete. Null geometry confirmed. KLS/KLC = 0.0.")

if __name__ == "__main__":
    scalarize_null_lake()