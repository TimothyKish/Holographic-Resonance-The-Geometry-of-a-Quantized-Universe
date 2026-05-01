import json
import os
import numpy as np

def peek_ledger():
    base_dir = os.getcwd()
    ledger = os.path.join(base_dir, 'NS6_7', 'lake', 'Master_Galaxy_Vol6_PHYSICAL.jsonl')
    
    if not os.path.exists(ledger):
        print("❌ Ledger not found.")
        return
        
    v_vals = []
    m_vals = []
    
    print(f"🔍 Scanning first 50,000 galaxies in {ledger}...")
    with open(ledger, 'r') as f:
        for i, line in enumerate(f):
            if i >= 50000: break
            try:
                data = json.loads(line)
                v_vals.append(float(data['v']))
                m_vals.append(float(data['m']))
            except:
                continue
                
    v_unique = len(set(v_vals))
    m_unique = len(set(m_vals))
    
    print("\n📊 DIAGNOSTIC RESULTS:")
    print(f"Velocity (v) unique values:  {v_unique} out of {len(v_vals)}")
    print(f"Magnitude (m) unique values: {m_unique} out of {len(m_vals)}")
    
    print("\n   [Sample Data]")
    for i in range(5):
        print(f"   Galaxy {i+1} -> v: {v_vals[i]}, m: {m_vals[i]}")

if __name__ == "__main__":
    peek_ledger()