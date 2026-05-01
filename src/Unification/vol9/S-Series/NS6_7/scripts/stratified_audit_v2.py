import json
import os
from collections import Counter

# 🛡️ NS6_22: THE STRATIFIED EPOCH AUDITOR (Float-Normalized)
# -----------------------------------------------------------
def audit_strata():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_path = os.path.join(project_root, 'lake', 'Master_Galaxy_Vol5.jsonl')
    
    print("⏳ INITIATING STRATIFIED TIME AUDIT")
    print(f"Target: {os.path.basename(input_path)}\n")
    
    epochs = {
        "Epoch 1 (Local)    | z: 0.01 - 0.10": Counter(),
        "Epoch 2 (Near)     | z: 0.10 - 0.20": Counter(),
        "Epoch 3 (Mid)      | z: 0.20 - 0.30": Counter(),
        "Epoch 4 (Deep)     | z: 0.30 - 0.50": Counter(),
        "Epoch 5 (Ancient)  | z: 0.50 - 0.70": Counter()
    }
    
    epoch_totals = {key: 0 for key in epochs}
    
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                bin_idx = data.get('kish_bin')
                raw_zsp = data.get('zsp')
                
                if bin_idx is not None and raw_zsp is not None:
                    try:
                        # Normalize the string into a pure mathematical decimal
                        zsp = float(raw_zsp)
                    except ValueError:
                        continue # Skip if the text is somehow corrupted
                        
                    # Sort the galaxy into its proper Epoch
                    if 0.01 <= zsp < 0.10:
                        epochs["Epoch 1 (Local)    | z: 0.01 - 0.10"][bin_idx] += 1
                        epoch_totals["Epoch 1 (Local)    | z: 0.01 - 0.10"] += 1
                    elif 0.10 <= zsp < 0.20:
                        epochs["Epoch 2 (Near)     | z: 0.10 - 0.20"][bin_idx] += 1
                        epoch_totals["Epoch 2 (Near)     | z: 0.10 - 0.20"] += 1
                    elif 0.20 <= zsp < 0.30:
                        epochs["Epoch 3 (Mid)      | z: 0.20 - 0.30"][bin_idx] += 1
                        epoch_totals["Epoch 3 (Mid)      | z: 0.20 - 0.30"] += 1
                    elif 0.30 <= zsp < 0.50:
                        epochs["Epoch 4 (Deep)     | z: 0.30 - 0.50"][bin_idx] += 1
                        epoch_totals["Epoch 4 (Deep)     | z: 0.30 - 0.50"] += 1
                    elif 0.50 <= zsp <= 0.70:
                        epochs["Epoch 5 (Ancient)  | z: 0.50 - 0.70"][bin_idx] += 1
                        epoch_totals["Epoch 5 (Ancient)  | z: 0.50 - 0.70"] += 1
                        
            except json.JSONDecodeError:
                continue

    for epoch_name, counts in epochs.items():
        total = epoch_totals[epoch_name]
        print(f"\n==================================================")
        print(f"🌌 {epoch_name} [Total: {total:,}]")
        print(f"==================================================")
        
        if total == 0:
            print("No galaxies found in this epoch.")
            continue
            
        for i in range(10):
            count = counts.get(i, 0)
            percentage = (count / total) * 100
            bar = '█' * int(percentage)
            marker = " 🌟" if percentage > 11.5 else "" 
            print(f"Bin {i}: [{count:6d}] | {percentage:05.2f}% | {bar}{marker}")

if __name__ == "__main__":
    try:
        audit_strata()
    except Exception as e:
        import traceback
        print("\n❌ CRITICAL SYSTEM CRASH:")
        traceback.print_exc()
    finally:
        input("\nPress ENTER to close this window...")