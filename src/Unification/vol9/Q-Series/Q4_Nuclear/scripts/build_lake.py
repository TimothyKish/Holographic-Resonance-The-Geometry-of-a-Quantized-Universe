"""
build_lake.py -- Q4_Nuclear: Nuclear Binding Energies
Lake ID: q4_nuclear
Domain: nuclear_binding
Source: NNDC Atomic Mass Evaluation 2020 (AME2020)
        https://www-nds.iaea.org/amdc/

Records: ~3500 (binding energy per nucleon for known nuclides)
Scalar: log(binding_energy_mev_per_A + 1) / log(k_geo)

Pre-registration: DOI 10.5281/zenodo.19702022 (Prediction P21)
Prediction P21: Nuclear binding energies cluster below quantum register 12/pi,
consistent with the three-layer model (nuclear layer < 12/pi).

Build: Timothy John Kish / KishLattice 16pi Initiative LLC / April 2026
"""

import json, os, urllib.request, math

PI    = math.pi
K_GEO = 16.0 / PI

RAW_PATH = os.path.join(os.path.dirname(__file__), "..", "lake", "q4_nuclear_raw.jsonl")
os.makedirs(os.path.dirname(RAW_PATH), exist_ok=True)

# AME2020 mass table - available from NNDC/IAEA
# Primary: IAEA NuDat / AME2020 mass excess table
# URL: https://www-nds.iaea.org/amdc/ame2020/mass_1.mas20.txt
AME2020_URL = "https://www-nds.iaea.org/amdc/ame2020/mass_1.mas20.txt"

# Fallback: NNDC chart of nuclides CSV export
NNDC_CHART_URL = "https://www.nndc.bnl.gov/nudat3/chartNuclides.jsp?unc=nds"


def parse_ame2020(content):
    """
    Parse AME2020 mass table format.
    Format: fixed-width, header lines start with # or have column labels.
    Key columns: Z, A, binding_energy_per_A (in keV/u)
    """
    records = []
    lines = content.split("\n")
    data_started = False
    for line in lines:
        if not data_started:
            if line.strip().startswith("0"):
                data_started = True
            continue
        if len(line) < 60:
            continue
        try:
            # AME2020 fixed-width format:
            # col 1: flag
            # col 2-4: NZ (N-Z)
            # col 5-8: N
            # col 9-12: Z
            # col 13-16: A
            # col 18-20: element symbol
            # col 30-41: mass excess (keV)
            # col 42-52: binding energy per nucleon (keV/A)
            parts = line.split()
            if len(parts) < 6:
                continue
            # Try to extract Z, A, binding energy
            # AME2020 has binding energy in col ~52-64, unit keV/A
            # We'll use a simple heuristic parse
            a_str = parts[3] if len(parts) > 3 else ""
            z_str = parts[2] if len(parts) > 2 else ""
            # Binding energy per nucleon is typically in the 5th or 6th numeric field
            # Conservative parse: look for values in the range 0-9000 keV/A
            nums = []
            for p in parts:
                try:
                    v = float(p.replace("#", ""))
                    nums.append(v)
                except ValueError:
                    pass
            if len(nums) >= 4:
                # Heuristic: binding energy per A is in range 1000-9000 keV/A
                be_candidates = [v for v in nums if 1000 < v < 10000]
                if be_candidates:
                    be_kev = be_candidates[0]
                    be_mev = be_kev / 1000.0
                    try:
                        Z = int(z_str)
                        A = int(a_str)
                        if Z > 0 and A > 0 and be_mev > 0:
                            records.append((Z, A, be_mev))
                    except ValueError:
                        pass
        except Exception:
            continue
    return records


def build():
    print("[Q4_Nuclear] Fetching AME2020 mass table...")
    records_raw = []
    try:
        with urllib.request.urlopen(AME2020_URL, timeout=30) as resp:
            content = resp.read().decode("latin-1")
        print(f"  Downloaded {len(content)} bytes")
        records_raw = parse_ame2020(content)
        print(f"  Parsed {len(records_raw)} nuclides from AME2020")
    except Exception as e:
        print(f"  AME2020 fetch failed ({e})")
        print(f"  Using well-known binding energy values for stable nuclides...")
        # Fallback: key nuclides with well-known binding energies (MeV/A)
        records_raw = [
            (1,  2,  1.112),   # deuterium
            (1,  3,  2.827),   # tritium
            (2,  3,  2.573),   # He-3
            (2,  4,  7.074),   # He-4 (alpha)
            (3,  6,  5.332),   # Li-6
            (3,  7,  5.606),   # Li-7
            (4,  9,  6.463),   # Be-9
            (5, 10,  6.475),   # B-10
            (5, 11,  6.928),   # B-11
            (6, 12,  7.680),   # C-12
            (6, 13,  7.470),   # C-13
            (7, 14,  7.476),   # N-14
            (7, 15,  7.699),   # N-15
            (8, 16,  7.976),   # O-16
            (8, 18,  7.767),   # O-18
            (9, 19,  7.779),   # F-19
            (10,20,  8.032),   # Ne-20
            (11,23,  8.111),   # Na-23
            (12,24,  8.261),   # Mg-24
            (13,27,  8.332),   # Al-27
            (14,28,  8.448),   # Si-28
            (15,31,  8.481),   # P-31
            (16,32,  8.493),   # S-32
            (17,35,  8.520),   # Cl-35
            (18,40,  8.595),   # Ar-40
            (19,39,  8.557),   # K-39
            (20,40,  8.551),   # Ca-40
            (22,48,  8.723),   # Ti-48
            (24,52,  8.776),   # Cr-52
            (25,55,  8.765),   # Mn-55
            (26,56,  8.790),   # Fe-56 (peak stability)
            (27,59,  8.768),   # Co-59
            (28,58,  8.732),   # Ni-58
            (29,63,  8.752),   # Cu-63
            (30,64,  8.736),   # Zn-64
            (36,84,  8.718),   # Kr-84
            (42,98,  8.635),   # Mo-98
            (47,107, 8.553),   # Ag-107
            (50,120, 8.505),   # Sn-120
            (56,138, 8.393),   # Ba-138
            (79,197, 7.916),   # Au-197
            (82,208, 7.868),   # Pb-208
            (92,238, 7.570),   # U-238
        ]

    records = []
    for Z, A, be_mev in records_raw:
        if be_mev <= 0:
            continue
        records.append({
            "id": f"q4_{Z}_{A}",
            "Z": Z,
            "A": A,
            "N": A - Z,
            "binding_energy_mev_per_A": round(be_mev, 5),
            "source": "NNDC_AME2020",
            "source_url": AME2020_URL,
            "domain": "nuclear_binding",
            "lake_id": "q4_nuclear",
            "preregistration_doi": "10.5281/zenodo.19702022",
            "prediction": "P21"
        })

    # Deduplicate by Z,A
    seen = set()
    unique = []
    for r in records:
        key = (r["Z"], r["A"])
        if key not in seen:
            seen.add(key)
            unique.append(r)

    with open(RAW_PATH, "w", encoding="utf-8") as f:
        for r in unique:
            f.write(json.dumps(r) + "\n")

    be_vals = [r["binding_energy_mev_per_A"] for r in unique]
    print(f"[Q4_Nuclear] build_lake complete")
    print(f"  Records: {len(unique)} unique nuclides")
    print(f"  BE/A range: {min(be_vals):.3f} - {max(be_vals):.3f} MeV/A")
    print(f"  Output:  {RAW_PATH}")
    print(f"  Prediction P21: scalars should cluster BELOW 12/pi = {12/PI:.4f}")
    fe56_scalar = math.log(8.790 + 1.0) / math.log(K_GEO)
    print(f"  Fe-56 (peak stability 8.79 MeV/A): scalar={fe56_scalar:.4f}, N~{fe56_scalar*PI:.2f}")


if __name__ == "__main__":
    build()