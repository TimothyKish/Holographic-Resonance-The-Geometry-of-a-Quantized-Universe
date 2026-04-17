import csv
import os

# 🛡️ NS6_23: THE STELLAR DIAGNOSTIC PROBE
# -----------------------------------------------------------
def run_stellar_probe():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_path = os.path.join(project_root, 'lake', 'Master_Stellar.tsv')
    
    print(f"🛰️ LAUNCHING PROBE INTO: Master_Stellar.tsv\n")
    
    if not os.path.exists(input_path):
        print(f"❌ ERROR: Cannot find {input_path}")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        # 1. Skip VizieR comments
        lines = (line for line in f if not line.startswith('#') and line.strip())
        
        # 2. Extract Header and Auto-Detect Delimiter
        try:
            header_line = next(lines)
            delimiter = '\t' if '\t' in header_line else '|'
            headers = [h.strip() for h in header_line.split(delimiter)]
            
            print("🔍 EXACT COLUMN NAMES FOUND (First 20):")
            print(headers[:20]) # Print first 20 to avoid flooding the screen
            if 'pmRA' in headers: print("  ✅ Contains Proper Motion (pmRA/pmDE)")
            if 'Plx' in headers or 'parallax' in headers: print("  ✅ Contains Parallax")
            
            # 3. Stream to the first actual data row
            print("\n📊 FIRST STELLAR DATA ROW:")
            for raw_line in lines:
                if '---' in raw_line or 'deg' in raw_line:
                    continue
                
                first_data = [d.strip() for d in raw_line.split(delimiter)]
                
                # Zip them together and print the key physics columns
                for k, v in zip(headers, first_data):
                    if k in ['pmRA', 'pmDE', 'rpmag', 'zsp', 'class', 'spCl']:
                        print(f"  {k}: {v}")
                break
                
        except StopIteration:
            print("File is empty or unreadable.")

if __name__ == "__main__":
    try:
        run_stellar_probe()
    except Exception as e:
        print(f"❌ CRITICAL CRASH: {e}")
    finally:
        input("\nPress ENTER to close this window...")