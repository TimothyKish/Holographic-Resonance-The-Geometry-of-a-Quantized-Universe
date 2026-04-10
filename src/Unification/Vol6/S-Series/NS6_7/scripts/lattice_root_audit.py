import json
import os
from collections import Counter

# 🛡️ NS6_20: THE LATTICE ROOT AUDITOR
# -----------------------------------------------------------
# Goal: Stream the Vol5 JSONL and reveal the 16/pi geometry.

def audit_lattice():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_path = os.path.join(project_root, 'lake', 'Master_Galaxy_Vol5.jsonl')
    
    print("🌌 INITIATING LATTICE ROOT AUDIT")
    print(f"Target: {os.path.basename(input_path)}\n")
    
    if not os.path.exists(input_path):
        print(f"❌ ERROR: Could not find {input_path}")
        return
        
    bin_counts = Counter()
    total_galaxies = 0
    
    # Stream the JSONL
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                bin_idx = data.get('kish_bin')
                if bin_idx is not None:
                    bin_counts[bin_idx] += 1
                    total_galaxies += 1
            except json.JSONDecodeError:
                continue

    print(f"🏆 Total Probes Audited: {total_galaxies:,}")
    print("--------------------------------------------------")
    print("📊 THE 16/π PHASE DISTRIBUTION:")
    
    if total_galaxies == 0:
        print("No data found to audit.")
        return

    # Print the Histogram
    for i in range(10):
        count = bin_counts.get(i, 0)
        percentage = (count / total_galaxies) * 100
        
        # Create a visual ASCII bar
        bar_length = int(percentage)
        bar = '█' * bar_length
        
        # Highlight Bin 7 (The Root Note)
        marker = " 🌟 ROOT NOTE" if i == 7 else ""
        
        print(f"Bin {i}: [{count:7d}] | {percentage:05.2f}% | {bar}{marker}")
        
    print("--------------------------------------------------")

if __name__ == "__main__":
    try:
        audit_lattice()
    except Exception as e:
        print(f"\n❌ SCRIPT CRASHED: {e}")
    finally:
        input("\nPress ENTER to close this window...")