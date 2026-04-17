import json
import math
import os
import time
import re
import traceback

# 🛡️ NS6_24: THE STELLAR REFINERY
# -----------------------------------------------------------
# Goal: Stream the 350MB+ Milky Way Lake, extract Proper Motions,
#       and lock down the Zero-Redshift 16/pi Nodes.

def extract_pure_number(value):
    if not value: return 0.0
    clean = re.sub(r'[^\d\.\-]', '', str(value))
    try:
        return float(clean) if clean and clean not in ['-', '.'] else 0.0
    except:
        return 0.0

def refine_stellar_lake():
    L = 16.0 / math.pi
    ANCHOR = 6.6069e10 # Universal S-Series Anchor
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_path = os.path.join(project_root, 'lake', 'Master_Stellar.tsv')
    output_path = os.path.join(project_root, 'lake', 'Master_Stellar_Vol5.jsonl')
    
    print(f"🏭 STELLAR REFINERY INITIATED")
    print(f"Target: Master_Stellar.tsv")
    print(f"Output: Master_Stellar_Vol5.jsonl\n")
    
    if not os.path.exists(input_path):
        print(f"❌ ERROR: Cannot find {input_path}")
        return

    processed = 0
    validated = 0
    start_time = time.time()
    
    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:
        
        # 1. Skip VizieR comments
        lines = (line for line in infile if not line.startswith('#') and line.strip())
        
        # 2. Extract Header and Auto-Detect Delimiter
        header_line = next(lines)
        delimiter = '\t' if '\t' in header_line else '|'
        headers = [h.strip() for h in header_line.split(delimiter)]
        
        # 3. Stream the Stars
        for raw_line in lines:
            if '---' in raw_line or 'deg' in raw_line:
                continue
                
            processed += 1
            values = [v.strip() for v in raw_line.split(delimiter)]
            row = dict(zip(headers, values))
            
            # Extract Stellar Physics
            pmRA = extract_pure_number(row.get('pmRA', 0))
            pmDE = extract_pure_number(row.get('pmDE', 0))
            rpmag = extract_pure_number(row.get('rpmag', 0))
            
            # Filter for clean data (Must have light and motion)
            if rpmag > 0 and (pmRA != 0 or pmDE != 0):
                # Calculate Total Kinetic Proper Motion
                pm_total = math.sqrt(pmRA**2 + pmDE**2)
                
                if pm_total > 0:
                    lum = 10**((25 - rpmag) / 2.5)
                    ks = ((pm_total**4) / lum) / ANCHOR
                    phi = math.log(ks) % L
                    bin_idx = min(int((phi / L) * 10), 9)
                    
                    row['pm_total'] = round(pm_total, 4)
                    row['kish_phi'] = round(phi, 6)
                    row['kish_bin'] = bin_idx
                    row['vol5_status'] = "VALIDATED_STAR"
                    
                    outfile.write(json.dumps(row) + '\n')
                    validated += 1
                    
            if processed % 100000 == 0:
                print(f"  ... scanned {processed:,} stars ... Validated: {validated:,}")

    elapsed = time.time() - start_time
    print(f"\n🏆 STELLAR REFINERY COMPLETE!")
    print(f"Time: {elapsed:.2f} seconds")
    print(f"Total Rows Scanned: {processed:,}")
    print(f"Vol5 Validated Stars: {validated:,}")

if __name__ == "__main__":
    try:
        refine_stellar_lake()
    except Exception as e:
        print("\n❌ CRITICAL SYSTEM CRASH:")
        traceback.print_exc()
    finally:
        input("\nPress ENTER to close this window...")