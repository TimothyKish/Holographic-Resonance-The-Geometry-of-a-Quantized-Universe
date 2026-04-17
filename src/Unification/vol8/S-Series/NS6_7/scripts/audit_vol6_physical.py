import json
import os
from collections import Counter

def run_physical_audit():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_path = os.path.join(project_root, 'lake', 'Master_Galaxy_Vol6_PHYSICAL.jsonl')
    
    quads = { 'NE': Counter(), 'NW': Counter(), 'SE': Counter(), 'SW': Counter() }

    with open(input_path, 'r') as f:
        for line in f:
            d = json.loads(line)
            quads[d['sector']][d['kish_bin']] += 1

    print("\n" + "="*65)
    print("🌍 VOL 6 PHYSICAL CARDINAL REPORT (FABER-JACKSON)")
    print("="*65)
    print(f"{'Sector':<8} {'N':>10} {'Peak Bin':>10} {'Status'}")
    print("-" * 65)

    for s in ['NW', 'NE', 'SW', 'SE']:
        n = sum(quads[s].values())
        if n < 1000: continue
        
        peak_bin = quads[s].most_common(1)[0][0]
        print(f"{s:<8} {n:10,} {peak_bin:10}   REFEREED")

    print("="*65)

if __name__ == "__main__":
    run_physical_audit()