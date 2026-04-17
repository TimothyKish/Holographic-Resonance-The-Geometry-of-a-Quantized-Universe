import json
import os
from collections import Counter

def run_6dfgs_audit():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_path = os.path.join(project_root, 'lake', '6dFGS_PHYSICAL.jsonl')
    
    counts = Counter()

    print("📊 AUDITING 6dFGS (SOUTHERN SKY / INFRARED PHASE SHIFT)...")
    
    try:
        with open(input_path, 'r') as f:
            for line in f:
                data = json.loads(line)
                counts[data['kish_bin']] += 1
    except FileNotFoundError:
        print("❌ ERROR: 6dFGS_PHYSICAL.jsonl not found. Run the harvester first.")
        return

    total = sum(counts.values())
    if total == 0:
        print("❌ No data to audit.")
        return

    print("\n" + "="*55)
    print(f"{'Bin':<10} | {'Count':<10} | {'Percentage':<10} | {'Status'}")
    print("-" * 55)

    for b in range(10):
        pct = (counts[b] / total) * 100
        marker = ""
        if b in [7, 8]:
            marker = " < EXPECTED PHASE SHIFT (Infrared)"
        elif b == 1:
            marker = " (Original SDSS Optical Peak)"
            
        print(f"{b:<10} | {counts[b]:<10} | {pct:<9.2f}% {marker}")
    
    print("="*55)
    print("🔭 THE MONDY CHECK:")
    print("If the peak lands in Bin 7 or 8, the lattice survives the Color Index shift.")
    print("This proves Electromagnetic Invariance.")

if __name__ == "__main__":
    run_6dfgs_audit()