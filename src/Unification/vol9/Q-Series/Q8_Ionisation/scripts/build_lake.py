"""
build_lake.py -- Q8_Ionisation: Atomic First Ionisation Energies
Lake ID: q8_ionisation
Domain: atomic_ionisation
Source: NIST Atomic Spectra Database (ASD)
        https://physics.nist.gov/cgi-bin/ASD/ionEnergy.pl
Records: 118 (first ionisation energy for all known elements)
Scalar: log(ionisation_eV + 1) / log(k_geo)

Pre-registration: DOI 10.5281/zenodo.19702022
Prediction: Same-object test — same atoms as Q1 (spectral lines) and Q3 (vibrations),
different physical attribute (ionisation energy). Should show different register.

Build: Timothy John Kish / KishLattice 16pi Initiative LLC / April 2026
"""

import json, os, math

PI    = math.pi
K_GEO = 16.0 / PI

RAW_PATH = os.path.join(os.path.dirname(__file__), "..", "lake", "q8_ionisation_raw.jsonl")
os.makedirs(os.path.dirname(RAW_PATH), exist_ok=True)

# NIST ASD first ionisation energies (eV)
# Source: NIST ASD https://physics.nist.gov/PhysRefData/ASD/ionEnergy.html
# NIST Handbook of Basic Atomic Spectroscopic Data
# All 118 elements, values in electron volts (eV)
IONISATION_ENERGIES = [
    # (Z, symbol, name, ie_eV)
    (1,  "H",  "Hydrogen",       13.5984),
    (2,  "He", "Helium",         24.5874),
    (3,  "Li", "Lithium",         5.3917),
    (4,  "Be", "Beryllium",       9.3227),
    (5,  "B",  "Boron",           8.2980),
    (6,  "C",  "Carbon",         11.2603),
    (7,  "N",  "Nitrogen",       14.5341),
    (8,  "O",  "Oxygen",         13.6181),
    (9,  "F",  "Fluorine",       17.4228),
    (10, "Ne", "Neon",           21.5645),
    (11, "Na", "Sodium",          5.1391),
    (12, "Mg", "Magnesium",       7.6462),
    (13, "Al", "Aluminum",        5.9858),
    (14, "Si", "Silicon",         8.1517),
    (15, "P",  "Phosphorus",     10.4867),
    (16, "S",  "Sulfur",         10.3600),
    (17, "Cl", "Chlorine",       12.9676),
    (18, "Ar", "Argon",          15.7596),
    (19, "K",  "Potassium",       4.3407),
    (20, "Ca", "Calcium",         6.1132),
    (21, "Sc", "Scandium",        6.5615),
    (22, "Ti", "Titanium",        6.8281),
    (23, "V",  "Vanadium",        6.7462),
    (24, "Cr", "Chromium",        6.7665),
    (25, "Mn", "Manganese",       7.4340),
    (26, "Fe", "Iron",            7.9024),
    (27, "Co", "Cobalt",          7.8810),
    (28, "Ni", "Nickel",          7.6398),
    (29, "Cu", "Copper",          7.7264),
    (30, "Zn", "Zinc",            9.3942),
    (31, "Ga", "Gallium",         5.9993),
    (32, "Ge", "Germanium",       7.8994),
    (33, "As", "Arsenic",         9.7886),
    (34, "Se", "Selenium",        9.7524),
    (35, "Br", "Bromine",        11.8138),
    (36, "Kr", "Krypton",        13.9996),
    (37, "Rb", "Rubidium",        4.1771),
    (38, "Sr", "Strontium",       5.6949),
    (39, "Y",  "Yttrium",         6.2173),
    (40, "Zr", "Zirconium",       6.6339),
    (41, "Nb", "Niobium",         6.7589),
    (42, "Mo", "Molybdenum",      7.0924),
    (43, "Tc", "Technetium",      7.28  ),
    (44, "Ru", "Ruthenium",       7.3605),
    (45, "Rh", "Rhodium",         7.4589),
    (46, "Pd", "Palladium",       8.3369),
    (47, "Ag", "Silver",          7.5762),
    (48, "Cd", "Cadmium",         8.9938),
    (49, "In", "Indium",          5.7864),
    (50, "Sn", "Tin",             7.3439),
    (51, "Sb", "Antimony",        8.6084),
    (52, "Te", "Tellurium",       9.0096),
    (53, "I",  "Iodine",         10.4513),
    (54, "Xe", "Xenon",          12.1298),
    (55, "Cs", "Cesium",          3.8939),
    (56, "Ba", "Barium",          5.2117),
    (57, "La", "Lanthanum",       5.5769),
    (58, "Ce", "Cerium",          5.5387),
    (59, "Pr", "Praseodymium",    5.4730),
    (60, "Nd", "Neodymium",       5.5250),
    (61, "Pm", "Promethium",      5.582 ),
    (62, "Sm", "Samarium",        5.6437),
    (63, "Eu", "Europium",        5.6704),
    (64, "Gd", "Gadolinium",      6.1501),
    (65, "Tb", "Terbium",         5.8638),
    (66, "Dy", "Dysprosium",      5.9389),
    (67, "Ho", "Holmium",         6.0215),
    (68, "Er", "Erbium",          6.1077),
    (69, "Tm", "Thulium",         6.1843),
    (70, "Yb", "Ytterbium",       6.2542),
    (71, "Lu", "Lutetium",        5.4259),
    (72, "Hf", "Hafnium",         6.8251),
    (73, "Ta", "Tantalum",        7.5496),
    (74, "W",  "Tungsten",        7.8640),
    (75, "Re", "Rhenium",         7.8335),
    (76, "Os", "Osmium",          8.4382),
    (77, "Ir", "Iridium",         8.9670),
    (78, "Pt", "Platinum",        8.9587),
    (79, "Au", "Gold",            9.2255),
    (80, "Hg", "Mercury",        10.4375),
    (81, "Tl", "Thallium",        6.1082),
    (82, "Pb", "Lead",            7.4167),
    (83, "Bi", "Bismuth",         7.2856),
    (84, "Po", "Polonium",        8.417 ),
    (85, "At", "Astatine",        9.3   ),
    (86, "Rn", "Radon",          10.7485),
    (87, "Fr", "Francium",        4.0727),
    (88, "Ra", "Radium",          5.2784),
    (89, "Ac", "Actinium",        5.17  ),
    (90, "Th", "Thorium",         6.3067),
    (91, "Pa", "Protactinium",    5.89  ),
    (92, "U",  "Uranium",         6.1941),
    (93, "Np", "Neptunium",       6.2657),
    (94, "Pu", "Plutonium",       6.0262),
    (95, "Am", "Americium",       5.9738),
    (96, "Cm", "Curium",          5.9915),
    (97, "Bk", "Berkelium",       6.1979),
    (98, "Cf", "Californium",     6.2817),
    (99, "Es", "Einsteinium",     6.3676),
    (100,"Fm", "Fermium",         6.50  ),
    (101,"Md", "Mendelevium",     6.58  ),
    (102,"No", "Nobelium",        6.65  ),
    (103,"Lr", "Lawrencium",      4.96  ),
    (104,"Rf", "Rutherfordium",   6.02  ),
    (105,"Db", "Dubnium",         6.8   ),
    (106,"Sg", "Seaborgium",      7.8   ),
    (107,"Bh", "Bohrium",         7.7   ),
    (108,"Hs", "Hassium",         7.6   ),
    (109,"Mt", "Meitnerium",      8.7   ),
    (110,"Ds", "Darmstadtium",    9.6   ),
    (111,"Rg", "Roentgenium",    10.6   ),
    (112,"Cn", "Copernicium",    11.97  ),
    (113,"Nh", "Nihonium",        6.5   ),
    (114,"Fl", "Flerovium",       8.5   ),
    (115,"Mc", "Moscovium",       5.4   ),
    (116,"Lv", "Livermorium",     6.6   ),
    (117,"Ts", "Tennessine",      7.7   ),
    (118,"Og", "Oganesson",       8.7   ),
]


def build():
    records = []
    for Z, sym, name, ie_eV in IONISATION_ENERGIES:
        records.append({
            "id": f"q8_{Z}_{sym}",
            "Z": Z,
            "symbol": sym,
            "element_name": name,
            "ionisation_energy_eV": ie_eV,
            "ionisation_order": 1,
            "source": "NIST_ASD",
            "source_url": "https://physics.nist.gov/PhysRefData/ASD/ionEnergy.html",
            "domain": "atomic_ionisation",
            "lake_id": "q8_ionisation",
            "preregistration_doi": "10.5281/zenodo.19702022",
            "prediction": "P_same_object_atomic"
        })

    with open(RAW_PATH, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

    ie_vals = [r["ionisation_energy_eV"] for r in records]
    print(f"[Q8_Ionisation] build_lake complete")
    print(f"  Records: {len(records)} (all 118 elements)")
    print(f"  IE range: {min(ie_vals):.4f} - {max(ie_vals):.4f} eV")
    print(f"  Output:  {RAW_PATH}")
    # Preview key scalars
    import math
    log_k = math.log(K_GEO)
    h_sc  = math.log(13.5984 + 1) / log_k
    he_sc = math.log(24.5874 + 1) / log_k
    cs_sc = math.log(3.8939  + 1) / log_k
    print(f"  H  IE={13.5984}eV  scalar={h_sc:.4f}  N~{h_sc*PI:.2f}")
    print(f"  He IE={24.5874}eV  scalar={he_sc:.4f}  N~{he_sc*PI:.2f}")
    print(f"  Cs IE={3.8939}eV   scalar={cs_sc:.4f}  N~{cs_sc*PI:.2f}")


if __name__ == "__main__":
    build()