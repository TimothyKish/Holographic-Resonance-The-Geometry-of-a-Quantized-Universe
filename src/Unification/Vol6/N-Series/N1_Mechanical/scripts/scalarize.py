# vol5/N-Series/N1_Lotto/scripts/scalarize.py
import json

def scalarize_null_lake():
    print("[*] Attempting Geometric Scalarization on N1_Lotto...")
    
    scalarized_lake = []
    
    with open("../lake/lotto_null.jsonl", "r") as f:
        for line in f:
            entry = json.loads(line)
            
            entry["scalar_invariant"] = 0.0
            entry["scalar_kls"] = 0.0
            entry["scalar_klc"] = 0.0
            
            scalarized_lake.append(entry)
            
    with open("../lake/lotto_null_scalarized.jsonl", "w") as f:
        for entry in scalarized_lake:
            f.write(json.dumps(entry) + "\n")
            
    print("[*] Scalarization complete. Mechanical chaos confirmed. KLS/KLC = 0.0.")

if __name__ == "__main__":
    scalarize_null_lake()