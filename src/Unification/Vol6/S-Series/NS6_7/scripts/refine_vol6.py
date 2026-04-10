import pandas as pd
import numpy as np
import os

def refine_vol6():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_path = os.path.join(project_root, 'lake', 'Master_Galaxy_Vol6.csv')
    output_path = os.path.join(project_root, 'lake', 'Processed_Vol6.csv')

    print(f"🧬 REFINING VOL 6 LAKE: {input_path}")
    df = pd.read_csv(input_path)

    # 1. Scalarize: Calculate the 42x Phase Wave
    # Using the 16/pi metric constant derived in previous audits
    def calculate_kish_bin(z):
        # Rolling phase velocity based on the 41.9x separator
        phase = (z * 16 / np.pi) % 1.0
        return int(phase * 10)

    print("🛰️  Calculating Global Phase Bins...")
    df['kish_bin'] = df['zsp'].apply(calculate_kish_bin)

    # 2. Assign Quadrants for the Cardinal Audit
    def get_quadrant(row):
        if row['DE_ICRS'] > 15:
            return 'NE' if row['RA_ICRS'] > 180 else 'NW'
        else:
            return 'SE' if row['RA_ICRS'] > 180 else 'SW'

    df['sector'] = df.apply(get_quadrant, axis=1)

    df.to_csv(output_path, index=False)
    print(f"✅ DONE: {len(df):,} galaxies scalarized and quadrant-mapped.")
    print(f"📂 Saved to: {output_path}")

if __name__ == "__main__":
    refine_vol6()