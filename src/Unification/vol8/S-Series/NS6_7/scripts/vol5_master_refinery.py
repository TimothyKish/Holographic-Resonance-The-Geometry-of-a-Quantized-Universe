import json
import math
import os
import time
import re
import traceback

# 🛡️ NS6_19: THE VOL5 AUTO-DETECT REFINERY
# -----------------------------------------------------------
def extract_pure_number(value):
    if not value: return 0.0
    clean = re.sub(r'[^\d\.\-]', '', str(value))
    try:
        return float(clean) if clean and clean not in ['-', '.'] else 0.0
    except:
        return 0.0

def refine_lake(input_filename, is_galaxy=True):
    L = 16.0 / math.pi
    ANCHOR = 6.6069e10 
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_path = os.path.join(project_root, 'lake', input_filename)
    output_filename = input_filename.replace('.tsv', '_Vol5.jsonl')
    output_path = os.path.join(project_root, 'lake', output_filename)
    
    print(f"🏭 REFINERY INITIATED: {input_filename}")
    
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
        print(f"🔍 Auto-Detected Delimiter: {'[TAB]' if delimiter == r'\t' else '[PIPE]'}")
        
        headers = [h.strip() for h in header_line.split(delimiter)]
        
        # 3. Stream the Data
        for raw_line in lines:
            # Skip the VizieR 'dash' and 'unit' rows
            if '---' in raw_line or 'deg' in raw_line:
                continue
                
            processed += 1
            values = [v.strip() for v in raw_line.split(delimiter)]
            
            # Map the row dynamically
            row = dict(zip(headers, values))
            
            if is_galaxy:
                vdisp = extract_pure_number(row.get('Vdisp', 0))
                rpmag = extract_pure_number(row.get('rpmag', 0))
                zsp   = extract_pure_number(row.get('zsp', 0))
                
                if vdisp > 70 and rpmag > 0 and zsp > 0:
                    lum = 10**((25 - rpmag) / 2.5)
                    ks = ((vdisp**4) / lum) / ANCHOR
                    phi = math.log(ks) % L
                    bin_idx = min(int((phi / L) * 10), 9)
                    
                    row['kish_phi'] = round(phi, 6)
                    row['kish_bin'] = bin_idx
                    row['vol5_status'] = "VALIDATED"
                    
                    outfile.write(json.dumps(row) + '\n')
                    validated += 1
                    
            if processed % 50000 == 0:
                print(f"  ... scanned {processed} rows ... Validated: {validated}")

    elapsed = time.time() - start_time
    print(f"\n🏆 REFINERY COMPLETE!")
    print(f"Time: {elapsed:.2f} seconds")
    print(f"Total Rows Scanned: {processed}")
    print(f"Vol5 Validated Rows: {validated}")

if __name__ == "__main__":
    print("--- S-SERIES MASTER REFINERY ---")
    try:
        refine_lake('Master_Galaxy.tsv', is_galaxy=True)
    except Exception as e:
        print("\n❌ CRITICAL SYSTEM CRASH:")
        traceback.print_exc()
    finally:
        input("\nPress ENTER to close this window...")