import csv
import os

def run_probe():
    # Find the lake folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_path = os.path.join(project_root, 'lake', 'Master_Galaxy.tsv')
    
    print(f"🛰️ LAUNCHING PROBE INTO: Master_Galaxy.tsv\n")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        # Ignore the VizieR comment block
        clean_lines = filter(lambda row: not row.startswith('#') and row.strip(), f)
        reader = csv.reader(clean_lines, delimiter='|')
        
        headers = [h.strip() for h in next(reader)]
        
        print("🔍 EXACT COLUMN NAMES FOUND:")
        print(headers)
        
        # VizieR usually puts a row of dashes next (---|---|---), so we skip it
        dashes = next(reader)
        
        print("\n📊 FIRST GALAXY DATA ROW:")
        first_data = [d.strip() for d in next(reader)]
        
        # Zip them together so we can read it easily
        for k, v in zip(headers, first_data):
            if k in ['zsp', 'Vdisp', 'rpmag', 'RA_ICRS', 'DE_ICRS']:
                print(f"  {k}: {v}")
                
        # Also print what it thinks the keys are overall to catch typos
        print("\n⚙️ Do we have our 3 core targets?")
        print(f"  Has 'Vdisp'? {'Vdisp' in headers}")
        print(f"  Has 'rpmag'? {'rpmag' in headers}")
        print(f"  Has 'zsp'? {'zsp' in headers}")

if __name__ == "__main__":
    run_probe()