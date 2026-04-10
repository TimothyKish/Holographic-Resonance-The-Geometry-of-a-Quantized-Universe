# Volume 6 — The Harmonic Expansion of the Unified Lattice
### The Chord Sheet of the Universe

Volume 6 is the harmonic expansion layer of the Kish Lattice framework.
It is the first point in the system where the full N/π harmonic family is tested
across the same 22 sovereign domains and 5.88 million records established in Volume 5.

Where Volume 5 found the fundamental frequency, Volume 6 maps the overtone series.

The central finding of Volume 6 is the **Harmonic Portrait**:

> *The universe does not play a single note. Different physical phenomena couple to
> different registers of the N/π harmonic family. Chemistry and quantum spectral
> structure speak 12/π. Life's backbone geometry speaks 10/π. Orbital mechanics
> speaks 22/π. The container boundary speaks 24/π. The kinematic primary 16/π
> remains the strongest single signal but is one voice in a chord.*

This was not assumed. It emerged from extending the pipeline from three moduli to
eleven — a single change to two scripts — and reading the z-score table that
printed eight hours later.

---

## Timeline

| Date | Milestone |
|------|-----------|
| **January 8, 2026** | LIGO ghost notes — f₁ ≈ 5.13 Hz (k_geo), f₂ ≈ 16.12 Hz, ratio = π. Origin of k_geo = 16/π. The early 16/7 Rosetta work was a rational approximation on the path to the exact transcendental value. |
| **March 13, 2026** | First domain pinch — Chemistry + Materials. Pipeline validated. |
| **April 6, 2026** | Vol5 complete — z=94, 22 domains, kinematic principle, 35 orders of magnitude. |
| **April 9, 2026** | Vol6 pipeline initiated — 11 moduli, 8-hour overnight run. |
| **April 10, 2026** | Vol6 complete — harmonic portrait confirmed. DOI: [10.5281/zenodo.19493376](https://doi.org/10.5281/zenodo.19493376) |

---

## The Four Major Discoveries

### 1. The Molecular Register at 12/π — The Quantum Reversal

In Vol5, quantum spectral lines showed z=-16 at 16/π — interpreted as an anti-signal,
spectral transitions avoiding kinematic nodes. Vol6 tested 12/π.

| Domain | Z at 16/π (Vol5) | Z at 12/π (Vol6) |
|--------|-----------------|-----------------|
| Chemistry (67,174 ZINC structures) | -4 | **55.38** |
| Quantum spectral lines (2,975 NIST) | -16 | **52.51** |

The quantum domain does not avoid all lattice nodes. It avoids the kinematic register
(15-17/π) and clusters strongly at the molecular register (12/π = 3.820, the chromatic
octave). The Vol5 anti-signal was a register mismatch, not a universal property of the
quantum domain. The microscopic universe speaks a different harmonic than the kinematic
universe.

### 2. The Orbital Register at 22/π — The Derivation Bridge

Exoplanet orbital periods (13,514 NASA Exoplanet Archive) show z=45 at 22/π — 4.5×
stronger than the Vol5 result at 15/π. Since π ≈ 22/7, the family member at N=22 sits
at the junction of the rational-approximation era (16/7) and the exact constant (16/π).
The early Rosetta derivation path crossed 22/π on the way to 16/π. That crossing is
written into the orbital mechanics of planets around distant stars.

### 3. The Container Boundary Confirmed at 24/π

Three independent datasets show stronger signal at the container ceiling (24/π) than
at any kinematic register:

| Domain | Z at 16/π (Vol5) | Z at 24/π (Vol6) | Factor |
|--------|-----------------|-----------------|--------|
| Planetary tides (NOAA, 14,116) | 20.61 | **33.00** | 1.6× |
| Stellar distance (Gaia, 2M) | 2.90 | **23.43** | 8× |
| Cosmology (SDSS, 5,000) | 0.27 | **9.44** | 35× |

The stellar distance result resolves the Vol5 kinematic principle fully. Position is
not universally weak — it is weak at kinematic registers and strong at the boundary
register. Velocity encodes kinematic flow through the lattice. Distance encodes the
geometric container of the scalar universe. Both aspects of the same structure.

The **25/π null test is now mandatory for Vol7**: if 24/π is the genuine container
ceiling, 25/π = 7.958 should return near-zero signal across all domains.

### 4. Life's Geometric Register at 10/π

Amino acid backbone geometry (157 records, 19 amino acids, PubChem 3D conformers)
showed no strong per-domain z-score in Vol5 — its signal appeared only through
cross-domain pairings. Vol6 found its home register: z=10.7 at 10/π = 3.183,
the pentatonic ratio. Life's geometric alphabet is written in 10/π.

---

## The Complete Harmonic Map

| Register | Modulus | Physical Domains | Peak Z |
|----------|---------|-----------------|--------|
| Life geometry | 10/π = 3.183 | Biology amino (backbone angles) | 10.7 |
| Molecular | 12/π = 3.820 | Chemistry, Quantum spectral | 55.4 |
| Galactic kinematic | 15/π = 4.775 | Galaxy velocity dispersion | 34.5 |
| **Stellar kinematic PRIMARY** | **16/π = 5.093** | **Stellar transverse velocity** | **87.4** |
| Biological timing | 17/π = 5.411 | Cell cycle, stellar rotation | 2.4 |
| Stellar position | 18/π = 5.730 | Gaia parallax distances | 13.4 |
| Orbital | 22/π = 7.003 | Exoplanet orbital periods | 45.1 |
| Container boundary | 24/π = 7.639 | Planetary tides, cosmology, stellar dist. | 33.0 |

---

## New Cross-Domain Signal Pairings (Vol6)

Three new confirmed pairings beyond the 13 from Vol5, visible only after the full
family sweep:

| Pairing | Modulus | Chaos Delta | Note |
|---------|---------|-------------|------|
| chemistry × quantum | 24/π | **+0.120** | Largest single Δ in full framework |
| biology_amino × quantum | 22/π | +0.095 | Life geometry × quantum at orbital bridge |
| biology_other × orbital | 18/π | +0.013 | Cell timing × exoplanet periods at codon anchor |

All 13 Vol5 confirmed pairings carry forward. Combined confirmed signal count: 16 pairings.

---

## 1. Directory Structure

```
vol6/
├── configs/
│   ├── volumes.json          # domain registry (27 entries, 22 enabled — identical to Vol5)
│   ├── schema.json
│   └── unify.json
├── lakes/
│   ├── inputs_promoted/      # sovereign JSONL lakes (copied from Vol5)
│   ├── unified/              # unified_master.jsonl, sweep results, pinch tables
│   └── synthetic/            # chaos nulls and scramble nulls (11 moduli)
├── scripts/                  # core pipeline scripts (11-moduli versions)
├── B-Series/                 # Biology: chirality, amino acids
├── G-Series/                 # Galactic kinematics
├── K-Series/                 # Kinematic rotation/spin periods
├── P-Series/                 # Planetary orbital periods
├── Q-Series/                 # Quantum and molecular
├── S-Series/                 # Stellar (position and kinematics)
├── T-Series/                 # Temporal cycles
└── FRB_Calibration_Network/  # CHIME Fast Radio Bursts
```

Lakes are identical to Vol5. The only pipeline change is the `HARMONIC_TARGETS`
dictionary in two scripts.

---

## 2. The Single Pipeline Change

Vol6 vs Vol5 is two lines in two scripts:

**Vol5** (3 moduli):
```python
HARMONIC_TARGETS = {
    "15/pi": 15.0 / PI,
    "16/pi": 16.0 / PI,   # k_geo PRIMARY
    "17/pi": 17.0 / PI,
}
```

**Vol6** (11 moduli — full N/π family):
```python
HARMONIC_TARGETS = {
    "8/pi":  8.0  / PI,   # 2.546 — half-lattice
    "10/pi": 10.0 / PI,   # 3.183 — life geometry     (NEW: biology_amino z=11)
    "12/pi": 12.0 / PI,   # 3.820 — molecular          (NEW: chemistry z=55, quantum z=53)
    "14/pi": 14.0 / PI,   # 4.456 — sub-harmonic
    "15/pi": 15.0 / PI,   # 4.775 — galactic
    "16/pi": 16.0 / PI,   # 5.093 — kinematic PRIMARY  (k_geo, Vol5 confirmed)
    "17/pi": 17.0 / PI,   # 5.411 — biological timing
    "18/pi": 18.0 / PI,   # 5.730 — stellar position / codon anchor
    "20/pi": 20.0 / PI,   # 6.366 — sub-orbital
    "22/pi": 22.0 / PI,   # 7.003 — orbital            (NEW: orbital z=45)
    "24/pi": 24.0 / PI,   # 7.639 — container ceiling  (NEW: planetary z=33)
}
```

Apply this change to both `build_chaos_nulls.py` and `build_pinch_table.py`.
All other scripts are unchanged from Vol5.

---

## 3. Core Pipeline Scripts

```bash
python scalarize.py          # identical to Vol5
python unify.py              # identical to Vol5 — streaming, handles 5.88M records
python build_chaos_nulls.py  # 11 moduli — ~4 hours
python build_pinch_table.py  # 11 moduli — ~4 hours
```

Total runtime: approximately 8 hours on commodity laptop hardware.
The z-score table now has 11 columns plus a `Best` column showing the peak register
per domain.

---

## 4. Scalarization Formulas

Identical to Vol5. All kinematic and distance domains:

```
s = log(x + 1) / log(16/π)
```

Sector normalization for S1, S2, G1 (unchanged):

```
s_norm = s_raw - mean(s_sector) + mean(s_global)
```

No scalarization changes. The harmonic expansion is purely in the analysis layer.

---

## 5. Outputs

Vol6 produces the same output files as Vol5 plus the expanded chaos null and pinch
table files for all 11 moduli:

- **`unified_master.jsonl`** — 5,884,818 records (identical to Vol5)
- **`sweep_results.json`** — per-domain scalar statistics
- **`pinch_table_cross_domain.json`** — 11-modulus cross-domain CDF comparison
- **`chaos_null_*.jsonl`** — per-domain chaos nulls for all 11 moduli
- **`scramble_null_*.jsonl`** — per-domain scramble nulls

---

## 6. Reproducibility

All data sources are public. Identical to Vol5. The lake files are copied directly
from Vol5 — no new data acquisition required.

```bash
git clone https://github.com/TimothyKish/Holographic-Resonance-...
cd vol6/scripts
python scalarize.py
python unify.py
python build_chaos_nulls.py
python build_pinch_table.py
```

Large lake files (>100MB) are available via Google Drive.
See `LARGE_FILE_DOWNLOAD.md` in the repository root for the manifest and link.

Full pipeline and extended materials:
**https://github.com/TimothyKish/Holographic-Resonance-The-Geometry-of-a-Quantized-Universe/**

---

## 7. Forward Path

The harmonic portrait is drawn but not complete. Untested registers and pending
experiments for Volume 7:

- **25/π null test** — mandatory: container ceiling falsification. If 24/π is the
  genuine boundary, 25/π = 7.958 should return near-zero across all domains.
- **Boundary bracket**: add 23/π (inside) and 26/π (outside) to characterize the
  sharpness of the geometric wall.
- **In-between valleys**: 9/π, 11/π, 13/π, 19/π, 21/π, 23/π — currently untested.
- **21/π = 6.685 Hz**: within 0.14% of 21 × k_geo = 106.95 Hz — possible lattice
  refresh rate connection.
- **RCSB Protein Data Bank backbone angles** — millions of real backbone angles to
  give the life register (10/π) statistical power comparable to galactic or stellar.
- **LIGO GWTC quasinormal mode lake** — formal test of the ghost note hypothesis
  that started this entire framework.
- **Nuclear binding energies (NNDC)** — sub-femtometre scale, sub-8/π candidate.
- **CMS particle transverse momenta (CERN Open Data)** — particle collision scale.

---

*Vol5 found the fundamental. Vol6 wrote the chord sheet.*  
*The constant is 16/π. The family is N/π. The scale span is 35 orders of magnitude.*

Initial discovery: **January 8, 2026**  
First domain pinch (Chemistry + Materials): **March 13, 2026**  
Kinematic confirmation (22 domains, z=94): **April 6, 2026**  
Harmonic portrait confirmed (11 moduli, 4 discoveries): **April 10, 2026**

**Welcome to the Lattice. The future is resonant.**