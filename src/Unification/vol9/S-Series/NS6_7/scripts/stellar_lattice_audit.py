import json
import os
from collections import Counter

# 🛡️ NS6_25: THE STELLAR LATTICE AUDITOR
# -----------------------------------------------------------
# Goal: Stream the Vol5 Stellar Lake and reveal the static 
#       zero-redshift geometry of the local Milky Way.

def audit_stellar_lattice():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_path = os.path.join(project_root, 'lake', 'Master_Stellar_Vol5.jsonl')
    
    print("✨ INITIATING STELLAR LATTICE AUDIT")
    print(f"Target: {os.path.basename(input_path)}\n")
    
    if not os.path.exists(input_path):
        print(f"❌ ERROR: Could not find {input_path}")
        return
        
    bin_counts = Counter()
    total_stars = 0
    
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                bin_idx = data.get('kish_bin')
                if bin_idx is not None:
                    bin_counts[bin_idx] += 1
                    total_stars += 1
            except json.JSONDecodeError:
                continue

    print(f"🏆 Total Local Anchors Audited: {total_stars:,}")
    print("--------------------------------------------------")
    print("📊 THE ZERO-REDSHIFT 16/π PHASE DISTRIBUTION:")
    
    if total_stars == 0:
        print("No data found to audit.")
        return

    # Print the Histogram
    for i in range(10):
        count = bin_counts.get(i, 0)
        percentage = (count / total_stars) * 100
        
        bar_length = int(percentage)
        bar = '█' * bar_length
        
        # Highlight major concentrations (> 11.5%)
        marker = " 🌟 LOCAL NODE" if percentage > 11.5 else ""
        
        print(f"Bin {i}: [{count:7d}] | {percentage:05.2f}% | {bar}{marker}")
        
    print("--------------------------------------------------")

if __name__ == "__main__":
    try:
        audit_stellar_lattice()
    except Exception as e:
        import traceback
        print(f"\n❌ SCRIPT CRASHED:")
        traceback.print_exc()
    finally:
        input("\nPress ENTER to close this window...")