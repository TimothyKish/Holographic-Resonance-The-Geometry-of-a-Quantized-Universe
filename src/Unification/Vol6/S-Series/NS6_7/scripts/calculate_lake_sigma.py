import json
import os
import math

# 🛡️ NS6_27: THE SOVEREIGN SIGMA CALCULATOR
# -----------------------------------------------------------
# Goal: Calculate Chi-Squared (X^2) and standard deviation 
#       sigma for both the Real and Null Galaxy Lakes.

def calculate_chi_square(file_name, lake_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    file_path = os.path.join(project_root, 'lake', file_name)
    
    if not os.path.exists(file_path):
        print(f"❌ ERROR: Cannot find {file_name}")
        return
        
    # Count the bins
    bins = {i: 0 for i in range(10)}
    total_count = 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                b = data.get('kish_bin')
                if b is not None:
                    bins[b] += 1
                    total_count += 1
            except json.JSONDecodeError:
                continue
                
    if total_count == 0:
        return

    # Calculate expected flat distribution (10% per bin)
    expected = total_count / 10.0
    
    # Calculate Chi-Squared
    chi_square = 0.0
    for i in range(10):
        observed = bins[i]
        chi_square += ((observed - expected) ** 2) / expected
        
    # Determine Physical Significance (df = 9)
    # 3 Sigma = 27.88 | 4 Sigma = 40.28 | 5 Sigma = 54.12
    if chi_square > 54.12:
        sigma_str = "> 5.0σ (DISCOVERY LEVEL)"
    elif chi_square > 40.28:
        sigma_str = "> 4.0σ (STRONG EVIDENCE)"
    elif chi_square > 27.88:
        sigma_str = "> 3.0σ (EVIDENCE)"
    else:
        sigma_str = "< 3.0σ (NOISE / BACKGROUND)"

    print(f"==================================================")
    print(f"📊 {lake_name.upper()} DATASET [N = {total_count:,}]")
    print(f"==================================================")
    print(f"Expected per bin : {expected:,.1f}")
    print(f"Chi-Squared (X²) : {chi_square:,.2f}")
    print(f"Degrees of Fr.   : 9")
    print(f"Significance     : {sigma_str}")
    print(f"==================================================\n")


if __name__ == "__main__":
    print("\n📐 INITIATING LATTICE SIGMA AUDIT...\n")
    try:
        calculate_chi_square('Master_Galaxy_Vol5.jsonl', "Real Galaxy Lake")
        calculate_chi_square('Master_Galaxy_Null_Vol5.jsonl', "Null Mirror Lake")
    except Exception as e:
        print(f"❌ CRITICAL CRASH: {e}")
    finally:
        input("Press ENTER to close this window...")