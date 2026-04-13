import pandas as pd
import requests
import io
import os

def build_validated_quantum_lake():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # Target fundamental spectra
    spec = "H I; He I"
    
    # NIST ASD refined parameter mapping for 2026
    params = {
        "spectra": spec,
        "format": "0",          # Must be 0 for the script to trigger
        "display_out": "1",     # THIS triggers the CSV/Text output
        "unit": "1",            # nm
        "line_out": "0",        # All lines
        "remove_js": "on",      # Kill the javascript wrappers
        "action": "Retrieve Data"
    }

    script_dir = os.path.dirname(os.path.abspath(__file__))
    lake_dir = os.path.join(os.path.dirname(script_dir), 'lake')
    if not os.path.exists(lake_dir): os.makedirs(lake_dir)
    output_path = os.path.join(lake_dir, 'nist_raw_v1.csv')

    print(f"🛰️  HARVESTING VALIDATED QUANTUM DATA: {spec}...")

    try:
        r = requests.get("https://physics.nist.gov/cgi-bin/ASD/lines1.pl", 
                         params=params, headers=headers, timeout=30)
        
        if r.status_code == 200:
            raw_text = r.text
            
            # If it still gives a 500 or HTML, we go to Plan B
            if "<!DOCTYPE" in raw_text[:200] and "Unknown parameter" in raw_text:
                print("❌ REJECTED: NIST has changed the API parameters again.")
                return

            # Clean up the NIST text-stream
            lines = raw_text.splitlines()
            # Find where the data actually starts (skip the "NIST Atomic Spectra" header)
            start_line = 0
            for i, line in enumerate(lines):
                if "element" in line.lower() or 'ritz' in line.lower():
                    start_line = i
                    break
            
            clean_data = "\n".join(lines[start_line:])
            df = pd.read_csv(io.StringIO(clean_data), on_bad_lines='skip')
            
            if not df.empty:
                df.to_csv(output_path, index=False)
                print(f"✅ SUCCESS: {len(df)} lines captured in {output_path}")
            else:
                print("❌ ERROR: Stream received but no data parsed.")
        else:
            print(f"❌ SERVER ERROR: {r.status_code}")
            
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {e}")

if __name__ == "__main__":
    build_validated_quantum_lake()