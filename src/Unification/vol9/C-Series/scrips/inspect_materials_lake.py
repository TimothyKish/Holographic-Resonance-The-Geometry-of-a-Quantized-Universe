import json
from pathlib import Path

path = Path(r"C:\Users\timot\Downloads\Science\src\Unification\Vol3\Lattice_Audit_Materials\Kish_Lattice_Empirical_Lake.json")

with path.open("r", encoding="utf-8") as f:
    data = json.load(f)

print("Number of entries:", len(data))
print("Keys in first entry:", list(data[0].keys()))
print("First entry:", data[0])
