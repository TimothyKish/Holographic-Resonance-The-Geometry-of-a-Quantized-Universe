import pandas as pd
import os

def final_vol6_audit():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    file_path = os.path.join(project_root, 'lake', 'Processed_Vol6.csv')
    
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found.")
        return

    df = pd.read_csv(file_path)
    
    print("\n" + "="*65)
    print("🌍 VOL 6 GLOBAL CARDINAL VALIDATION (SDSS DR16)")
    print("="*65)
    print(f"{'Sector':<8} {'N':>10} {'Peak Bin':>10} {'Peak %':>10}")
    print("-" * 65)

    for sector in ['NW', 'NE', 'SW', 'SE']:
        sub = df[df['sector'] == sector]
        if len(sub) < 5000:
            print(f"{sector:<8} {len(sub):10,}    [INSUFFICIENT DENSITY]")
            continue
        
        # Calculate distribution
        counts = sub['kish_bin'].value_counts(normalize=True).sort_index()
        peak_bin = counts.idxmax()
        peak_pct = counts.max() * 100
        
        print(f"{sector:<8} {len(sub):10,} {peak_bin:10} {peak_pct:9.2f}%")

    print("="*65)
    print(f"TOTAL SAMPLE SIZE: {len(df):,}")

if __name__ == "__main__":
    final_vol6_audit()