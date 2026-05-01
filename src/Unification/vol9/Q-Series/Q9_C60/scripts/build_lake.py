"""
build_lake.py -- Q9_C60: C60 Buckminsterfullerene Vibrational Modes
Lake ID: q9_c60
Domain: molecular_c60
Source: NIST CCCBDB + Dresselhaus et al. (1996) + Bethune et al. (1991)
Records: 46 (symmetry-distinct vibrational modes, Ih point group)

Pre-registration: DOI 10.5281/zenodo.19702022 (Prediction P17)
Prediction P17: C60 modes cluster at quantum register 12/pi (scalar=3.8197)
Basis: P11 confirmed molecular vibration register at 12/pi, z=53.25, N~5000

Gamma_vib = 2Ag + 3T1g + 4T2g + 6Gg + 8Hg + Au + 4T1u + 5T2u + 6Gu + 7Hu = 46 modes

Build: Timothy John Kish / KishLattice 16pi Initiative LLC / April 2026
"""

import json, os

RAW_PATH = os.path.join(os.path.dirname(__file__), "..", "lake", "q9_c60_raw.jsonl")
os.makedirs(os.path.dirname(RAW_PATH), exist_ok=True)

# ==============================================================================
# C60 VIBRATIONAL MODE DATA
# Sources:
#   [1] NIST CCCBDB: https://cccbdb.nist.gov
#   [2] Dresselhaus et al., Science of Fullerenes and Carbon Nanotubes (1996)
#   [3] Bethune et al., Chem. Phys. Lett. 179, 181 (1991)
#   [4] Schettino et al., J. Chem. Phys. 114, 8801 (2001)
# Units: cm^-1 (wavenumber)
# Ih symmetry: 60 atoms, 3N-6 = 174 modes, 46 distinct by symmetry
# ==============================================================================
C60_MODES = [
    # (irrep, freq_cm1, activity, mode_index, description)
    ("Ag",   496,  "raman",  1, "Breathing mode - totally symmetric radial"),
    ("Ag",  1469,  "raman",  2, "Pentagonal pinch - totally symmetric C-C stretch"),
    ("T1g",  567,  "silent", 1, "T1g(1)"),
    ("T1g",  860,  "silent", 2, "T1g(2)"),
    ("T1g", 1310,  "silent", 3, "T1g(3)"),
    ("T2g",  397,  "silent", 1, "T2g(1)"),
    ("T2g",  753,  "silent", 2, "T2g(2)"),
    ("T2g", 1054,  "silent", 3, "T2g(3)"),
    ("T2g", 1320,  "silent", 4, "T2g(4)"),
    ("Gg",   345,  "silent", 1, "Gg(1)"),
    ("Gg",   757,  "silent", 2, "Gg(2)"),
    ("Gg",   964,  "silent", 3, "Gg(3)"),
    ("Gg",  1099,  "silent", 4, "Gg(4)"),
    ("Gg",  1310,  "silent", 5, "Gg(5)"),
    ("Gg",  1540,  "silent", 6, "Gg(6)"),
    ("Hg",   273,  "raman",  1, "Hg(1) squashing mode"),
    ("Hg",   437,  "raman",  2, "Hg(2)"),
    ("Hg",   710,  "raman",  3, "Hg(3)"),
    ("Hg",   774,  "raman",  4, "Hg(4)"),
    ("Hg",  1099,  "raman",  5, "Hg(5)"),
    ("Hg",  1250,  "raman",  6, "Hg(6)"),
    ("Hg",  1425,  "raman",  7, "Hg(7)"),
    ("Hg",  1575,  "raman",  8, "Hg(8)"),
    ("Au",   976,  "silent", 1, "Au(1)"),
    ("T1u",  527,  "ir",     1, "T1u(1) IR active"),
    ("T1u",  577,  "ir",     2, "T1u(2) IR active"),
    ("T1u", 1183,  "ir",     3, "T1u(3) IR active"),
    ("T1u", 1429,  "ir",     4, "T1u(4) IR active strongest"),
    ("T2u",  354,  "silent", 1, "T2u(1)"),
    ("T2u",  715,  "silent", 2, "T2u(2)"),
    ("T2u", 1030,  "silent", 3, "T2u(3)"),
    ("T2u", 1208,  "silent", 4, "T2u(4)"),
    ("T2u", 1410,  "silent", 5, "T2u(5)"),
    ("Gu",   485,  "silent", 1, "Gu(1)"),
    ("Gu",   667,  "silent", 2, "Gu(2)"),
    ("Gu",   920,  "silent", 3, "Gu(3)"),
    ("Gu",  1190,  "silent", 4, "Gu(4)"),
    ("Gu",  1316,  "silent", 5, "Gu(5)"),
    ("Gu",  1480,  "silent", 6, "Gu(6)"),
    ("Hu",   403,  "silent", 1, "Hu(1)"),
    ("Hu",   664,  "silent", 2, "Hu(2)"),
    ("Hu",   776,  "silent", 3, "Hu(3)"),
    ("Hu",   978,  "silent", 4, "Hu(4)"),
    ("Hu",  1155,  "silent", 5, "Hu(5)"),
    ("Hu",  1396,  "silent", 6, "Hu(6)"),
    ("Hu",  1546,  "silent", 7, "Hu(7)"),
]


def build():
    records = []
    for irrep, freq_cm1, activity, idx, desc in C60_MODES:
        record = {
            "id": f"c60_{irrep.lower()}_{idx}",
            "molecule": "C60",
            "formula": "C60",
            "symmetry_group": "Ih",
            "irrep": irrep,
            "mode_index": idx,
            "frequency_cm1": freq_cm1,
            "activity": activity,
            "description": desc,
            "source": "NIST_CCCBDB",
            "source_refs": [
                "Dresselhaus1996_Fullerenes",
                "Bethune1991_ChemPhysLett_179_181",
                "Schettino2001_JChemPhys_114_8801"
            ],
            "domain": "molecular_c60",
            "lake_id": "q9_c60",
            "preregistration_doi": "10.5281/zenodo.19702022",
            "prediction": "P17"
        }
        records.append(record)

    with open(RAW_PATH, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

    print(f"[Q9_C60] build_lake complete")
    print(f"  Records: {len(records)}")
    print(f"  Output:  {RAW_PATH}")
    print(f"  Domain:  molecular_c60")
    print(f"  Modes:   2Ag+3T1g+4T2g+6Gg+8Hg+Au+4T1u+5T2u+6Gu+7Hu = 46")


if __name__ == "__main__":
    build()