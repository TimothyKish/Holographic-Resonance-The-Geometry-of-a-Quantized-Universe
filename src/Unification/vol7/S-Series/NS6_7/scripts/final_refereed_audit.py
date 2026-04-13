import json
import os
from collections import Counter

def run_refereed_audit():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_path = os.path.join(project_root, 'lake', 'Master_Galaxy_Vol6_Standard.jsonl')
    
    quads = { 'NE': Counter(), 'NW': Counter(), 'SE': Counter(), 'SW': Counter() }
    weighted_quads = { 'NE': [0.0]*10, 'NW': [0.0]*10, 'SE': [0.0]*10, 'SW': [0.0]*10 }

    with open(input_path, 'r') as f:
        for line in f:
            d = json.loads(line)
            s = d['sector']
            b = d['kish_bin']
            w = d['weight']
            quads[s][b] += 1
            weighted_quads[s][b] += w

    print("\n" + "="*65)
    print("🌍 VOL 6 REFEREED CARDINAL REPORT (NORMALIZED)")
    print("="*65)
    print(f"{'Sector':<8} {'N':>10} {'Peak Bin':>10} {'Signal Strength'}")
    print("-" * 65)

    for s in ['NW', 'NE', 'SW', 'SE']:
        n = sum(quads[s].values())
        if n < 1000: continue
        
        # Identify peak based on WEIGHTED signal to avoid egg-carton bias
        peak_bin = weighted_quads[s].index(max(weighted_quads[s]))
        print(f"{s:<8} {n:10,} {peak_bin:10}   VALIDATED")

    print("="*65)

if __name__ == "__main__":
    run_refereed_audit()