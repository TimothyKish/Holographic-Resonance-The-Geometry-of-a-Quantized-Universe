import os
import pandas as pd
import json

def scout():
    files = ['Master_Galaxy_Vol6.csv', 'Processed_Vol6.csv', 'Master_Galaxy_Vol6_PHYSICAL.jsonl']
    for f in files:
        if not os.path.exists(f): continue
        print(f"\n🔍 Checking {f}...")
        if f.endswith('.csv'):
            df = pd.read_csv(f, nrows=1)
            print(f"   Headers: {list(df.columns)}")
        else:
            with open(f, 'r') as j:
                line = j.readline()
                print(f"   Keys: {list(json.loads(line).keys())}")

if __name__ == "__main__":
    scout()