import csv, json
from pathlib import Path

src = Path(r"C:\Users\timot\Downloads\gaia_tap_result.csv")
dst = Path(r"S-Series\S3_GalacticNASA\lake\s3_gaia_luminosity_raw.jsonl")
dst.parent.mkdir(parents=True, exist_ok=True)
with open(src, newline='', encoding='utf-8') as fin, \
     open(dst, 'w', encoding='utf-8') as fout:
    for row in csv.DictReader(fin):
        fout.write(json.dumps(row) + '\n')
print(f"Done: {dst}")