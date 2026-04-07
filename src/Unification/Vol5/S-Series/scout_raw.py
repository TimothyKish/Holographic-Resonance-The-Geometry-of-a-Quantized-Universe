import os
import pandas as pd

def scout_raw_ledgers():
    base_dir = os.getcwd()
    lake_dir = os.path.join(base_dir, 'NS6_7', 'lake')
    
    candidates = [
        'Master_Galaxy_Vol6.csv',
        'Master_Galaxy_Vol6_2.csv',
        'Processed_Vol6.csv'
    ]
    
    print("🛰️ SCOUTING VAULT FOR RAW, UN-NORMALIZED SDSS LEDGERS...\n")
    
    for filename in candidates:
        filepath = os.path.join(lake_dir, filename)
        if not os.path.exists(filepath):
            continue
            
        try:
            # Just read the first 10,000 rows to check for variance
            df = pd.read_csv(filepath, nrows=10000, on_bad_lines='skip')
            
            # Look for velocity and magnitude columns
            v_col = next((c for c in df.columns if c.lower() in ['v', 'vel', 'veldisp', 'sigma']), None)
            m_col = next((c for c in df.columns if c.lower() in ['m', 'mag', 'petrorad', 'dered_r']), None)
            
            print(f"📄 File: {filename}")
            print(f"   Columns found: {list(df.columns)}")
            
            if v_col and m_col:
                v_unique = df[v_col].nunique()
                m_unique = df[m_col].nunique()
                print(f"   Variance Check -> V unique: {v_unique}, M unique: {m_unique}")
                
                if m_unique > 100:
                    print("   ✅ TRUE RAW DATA DETECTED (Varying Magnitudes)")
                else:
                    print("   ❌ NORMALIZED/FLAT DATA DETECTED")
            else:
                print("   ⚠️ Physics columns not clearly identified.")
            print("-" * 60)
            
        except Exception as e:
            print(f"❌ Error reading {filename}: {e}")

if __name__ == "__main__":
    scout_raw_ledgers()