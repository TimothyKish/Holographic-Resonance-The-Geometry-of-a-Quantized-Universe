import json
import os
import numpy as np
from collections import Counter

def run_hyperleda_audit():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_path = os.path.join(project_root, 'lake', 'HyperLeda_PHYSICAL.jsonl')
    
    counts = Counter()
    scalars = []

    print("📊 AUDITING HYPERLEDA REPLICATION...")
    
    with open(input_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            counts[data['kish_bin']] += 1
            scalars.append(data['scalar'])

    total = sum(counts.values())
    if total == 0:
        print("❌ No data to audit.")
        return

    print("\n" + "="*45)
    print(f"{'Bin':<10} | {'Count':<10} | {'Percentage':<10}")
    print("-" * 45)

    for b in range(10):
        pct = (counts[b] / total) * 100
        marker = " < TARGET" if b == 1 else ""
        print(f"{b:<10} | {counts[b]:<10} | {pct:<9.2f}% {marker}")
    
    print("="*45)
    
    # Simple Sigma check (Internal)
    expected = total / 10
    chi2 = sum((counts[b] - expected)**2 / expected for b in range(10))
    print(f"Chi-Squared: {chi2:.2f}")

if __name__ == "__main__":
    run_hyperleda_audit()