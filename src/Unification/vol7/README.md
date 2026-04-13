# Volume 7 — The Sovereign Resonance
### Boundaries, Sub-Lattice, and the Unification Case

Volume 7 is the complete harmonic portrait of the scalar universe.
It extends the N/π family sweep from 11 moduli (Volume 6) to 22 moduli, spanning
5/π through 26/π, across the same 22 sovereign domains and 5.88 million records.

The central finding of Volume 7 is the **Bounded Scalar Universe**:

> *The scalar universe has a floor and a ceiling, and both are occupied. Below 7/π,
> the Rosetta sub-lattice governs biological and galactic structure. Above 24/π,
> the lattice does not go quiet — it inverts. The data actively avoids harmonic
> nodes above the container ceiling. This is geometric repulsion, not absence.
> The universe closes at 24/π, and it closes with force.*

Five major discoveries emerged from 15 hours of runtime. None were assumed.
All were read from the z-score table as printed.

---

## Timeline

| Date | Milestone |
|------|-----------|
| **January 10, 2026** | Vol1 published — formal Prediction/Observation table lists 107.1 Hz as Kish Model prediction for GW150914 (DOI: [10.5281/zenodo.18209531](https://doi.org/10.5281/zenodo.18209531)) |
| **February 2026** | Vol2 published — Definition 2.4: f_L = 107.1 Hz as Lattice Refresh Frequency |
| **February 8, 2026** | GitHub commit `e7949d5` — Chapter 13 LIGO Spectral Analysis naming 107 Hz lattice harmonics (public, cryptographically timestamped) |
| **April 10, 2026** | Vol6 complete — harmonic portrait, 11 moduli. DOI: [10.5281/zenodo.19493376](https://doi.org/10.5281/zenodo.19493376) |
| **April 11, 2026** | Vol7 pipeline initiated — 22 moduli, 15-hour overnight run |
| **April 12, 2026** | Vol7 complete — floor, ceiling, sub-lattice, and unification case confirmed |

---

## The Five Major Discoveries

### 1. The Galactic Register Flips to 21/π — The 107.1 Hz Confirmation

In Vol6, galactic velocity dispersion (1.84M SDSS galaxies) showed its strongest
signal at 15/π (z=34). Vol7 reveals z=59 at 21/π — 74% stronger.

| Domain | Z at 15/π (Vol6) | Z at 21/π (Vol7) | Note |
|--------|-----------------|-----------------|------|
| Galactic vdisp (1.84M SDSS) | 34.52 | **59.03** | Pre-registered prediction confirmed |

This result connects directly to the 107.1 Hz prediction published in Volume 1:

```
21 × k_geo = 21 × (16/π) = 106.952 Hz  ≈  107.1 Hz  (within 0.14%)
```

The prediction was in formal print on January 10, 2026 — ninety days before this
pipeline ran. The provenance chain: Vol1 prediction table → Vol2 Definition 2.4
→ Vol3 harmonic range description → GitHub commit e7949d5 (Feb 8) → this result.

**This is not a discovery. It is a pre-registered prediction confirmed.**

The second harmonic (127.4 Hz) is 25 × k_geo = 127.32 Hz. Vol7 tests 25/π and
finds stellar_kinematic z=-91 — the data avoids those nodes entirely. Vol1 called
127.4 Hz the upper bound of the harmonic range. Vol7 confirmed it as the ceiling
above which the lattice repels. Both predictions from Vol1 have now been measured.

### 2. Chemistry Peaks at 11/π — The Molecular Band

Vol6 identified 12/π as the chemistry peak (z=55). Vol7 tests 11/π for the first
time and finds z=70 — surpassing the Vol6 result.

| Domain | Z at 11/π | Z at 12/π | Pattern |
|--------|-----------|-----------|---------|
| Chemistry (67,174 ZINC) | **70.26** | 62.14 | Broad molecular band |
| Quantum spectral (3,086 NIST) | -20.45 | **49.61** | Sharp single peak |

Chemistry has a broad molecular band across 10/π–14/π. Quantum spectral transitions
have a sharp single peak at 12/π surrounded by strong avoidance. Same register
family. Different coupling character. The distinction between band coupling (chemistry)
and node coupling (quantum) is physical information about how these domains interact
with the lattice.

### 3. The 7/π Rosetta Sub-Lattice — The Denominator Vindicated

The early Kish framework used 16/7 as its organizing constant. When the ghost notes
confirmed k_geo = 16/π, the 7 appeared to be a coincidence of the rational
approximation π ≈ 22/7. Vol7 tests 7/π directly.

| Domain | Z at 6/π | Z at 7/π | Z at 8/π | Pattern |
|--------|----------|----------|----------|---------|
| biology_amino | -3.49 | **+11.87** | -4.15 | Sharp resonance at 7 |
| biology_other | -1.97 | **+6.12** | -2.17 | Sharp resonance at 7 |
| galactic | -9.89 | **+11.27** | -13.35 | Sharp resonance at 7 |

Sharp positive peak at 7/π flanked by negative values at 6/π and 8/π. This is
a node-specific resonance, not a broad band.

The connection is exact: k_geo / (7/π) = (16/π) / (7/π) = 16/7. The early Rosetta
constant was not measuring a modulus value. It was measuring the **inter-register
ratio** between the kinematic primary and the biological sub-lattice. The numerator
(16) was correct. The denominator (7) was correct. The interpretation was incomplete.

### 4. The Ceiling Is a Geometric Repulsion, Not a Wall

Vol6 predicted that 25/π should return near-zero if 24/π is the genuine container
ceiling. Vol7 delivers a stronger result.

| Domain | Z at 24/π | Z at 25/π | Z at 26/π |
|--------|-----------|-----------|-----------|
| stellar_kinematic | -92.01 | **-91.01** | **-96.64** |
| chemistry | -77.62 | **-78.85** | **-77.61** |
| planetary | +34.04 | -20.52 | -20.95 |

Domains that showed strong positive signal at 24/π drop to negative at 25/π.
Domains that avoid high-register nodes show their strongest anti-signals above the
ceiling. This is not a null. The data exists above 24/π — it just actively avoids
harmonic nodes there. The container closes and pushes back.

### 5. The Floor Is a Gradient

Below 7/π, the floor is domain-specific, not a single universal wall:

- Biology and galactic: floor at 7/π
- Chemistry: signal at 5/π (z=30), floor extends below the biological register
- Orbital: signal at 5/π (z=9), wide scalar range reaches the sub-floor

Different physical domains have different effective floors determined by the
characteristic scale of their physical quantities.

---

## The Materials Scalarization Error (Documented)

The materials domain (33,973 crystal lattice invariants) shows flat z-scores across
all 22 moduli in Vol7. **This is intentional and preserved on the main Git branch.**

**Root cause:** The scalarization formula `scalar = (volume/nsites) % k_geo` produces
a uniform distribution across the full container [0, 5.093] — indistinguishable from
the chaos null. The original build script was not committed to the repository.

| State | Scalar range | stdev/span | Status |
|-------|-------------|-----------|--------|
| Vol5-7 (broken) | [0.000, 5.088] | 0.287 | FAIL — uniform |
| Vol8 (fixed) | [0.640, 1.192] | 0.188 | PASS — clustered |

**The fix** (implemented in Vol8, `fix_materials_scalarization.py`):
```python
bond_length = (volume / nsites) ** (1.0 / 3.0)   # Angstroms
scalar = log(1 + bond_length) / log(k_geo)
```

The broken lake is preserved on `main` for educational purposes. The fixed lake is
on the `vol8-materials-fix` branch. `git diff` shows the exact change.

**The Vol8 result with the fix:** materials couples to 19/π (z=72), the sub-orbital
register — the transition zone between molecular chemistry (10-14/π) and orbital
mechanics (22/π). Crystal bond geometry sits geometrically between molecules and
planetary orbits. Materials are born in stellar furnaces. The lattice keeps the
fingerprint.

---

## The Complete Harmonic Portrait (Vol7)

| Register | Modulus | Physical Domains | Peak Z |
|----------|---------|-----------------|--------|
| Rosetta sub-lattice | 7/π = 2.228 | Biology (both), Galactic | 11.9 |
| Life geometry | 10/π = 3.183 | Biology amino (backbone) | 10.7 |
| **Molecular band (peak)** | **11/π = 3.501** | **Chemistry** | **70.3** |
| Molecular / Quantum | 12/π = 3.820 | Chemistry, Quantum spectral | 62.1 / 49.6 |
| Galactic kinematic | 15/π = 4.775 | Galaxy velocity dispersion | 32.5 |
| **Stellar kinematic PRIMARY** | **16/π = 5.093** | **Stellar transverse velocity** | **102.8** |
| Stellar position | 18/π = 5.730 | Stellar distance (Gaia) | 13.4 |
| Planetary period | 19/π = 6.048 | Planetary tidal intervals | 31.3 |
| **107.1 Hz register** | **21/π = 6.685** | **Galactic (confirmed prediction)** | **59.0** |
| Orbital bridge | 22/π = 7.003 | Exoplanet orbital periods | 42.7 |
| Container boundary | 24/π = 7.639 | Planetary, Stellar dist., Cosmology | 34.0 |
| *Above ceiling* | *25–26/π* | *Anti-signal: kinematic z = −91 to −97* | — |

---

## 1. Directory Structure

```
vol7/
├── configs/
│   ├── volumes.json          # domain registry (27 entries, 22 enabled — identical to Vol6)
│   ├── schema.json
│   └── unify.json
├── lakes/
│   ├── inputs_promoted/      # sovereign JSONL lakes (materials_promoted.jsonl = BROKEN, intentional)
│   ├── unified/              # unified_master.jsonl, sweep results, pinch tables
│   └── synthetic/            # chaos nulls and scramble nulls (22 moduli)
├── scripts/                  # core pipeline scripts (22-moduli versions)
│   └── fix_materials_scalarization.py   # RCA fix — run in Vol8, not Vol7
├── B-Series/                 # Biology: chirality, amino acids
├── G-Series/                 # Galactic kinematics
├── K-Series/                 # Kinematic rotation/spin periods
├── P-Series/                 # Planetary orbital periods
├── Q-Series/                 # Quantum and molecular
├── S-Series/                 # Stellar (position and kinematics)
├── T-Series/                 # Temporal cycles
└── FRB_Calibration_Network/  # CHIME Fast Radio Bursts
```

Lakes are identical to Vol6 (materials intentionally left in broken state for
educational RCA practice). The only pipeline change is the `HARMONIC_TARGETS`
dictionary, expanded from 11 to 22 moduli.

---

## 2. The Single Pipeline Change

Vol7 vs Vol6 is one dictionary in two scripts:

**Vol6** (11 moduli):
```python
HARMONIC_TARGETS = {
    "8/pi": 8.0/PI, "10/pi": 10.0/PI, "12/pi": 12.0/PI, "14/pi": 14.0/PI,
    "15/pi": 15.0/PI, "16/pi": 16.0/PI, "17/pi": 17.0/PI, "18/pi": 18.0/PI,
    "20/pi": 20.0/PI, "22/pi": 22.0/PI, "24/pi": 24.0/PI,
}
```

**Vol7** (22 moduli — complete portrait, floor to ceiling):
```python
HARMONIC_TARGETS = {
    "5/pi":5.0/PI,   "6/pi":6.0/PI,   "7/pi":7.0/PI,   # floor bracket
    "8/pi":8.0/PI,   "9/pi":9.0/PI,   "10/pi":10.0/PI,
    "11/pi":11.0/PI, "12/pi":12.0/PI, "13/pi":13.0/PI,
    "14/pi":14.0/PI, "15/pi":15.0/PI, "16/pi":16.0/PI,  # k_geo PRIMARY
    "17/pi":17.0/PI, "18/pi":18.0/PI, "19/pi":19.0/PI,
    "20/pi":20.0/PI, "21/pi":21.0/PI, "22/pi":22.0/PI,  # 107.1 Hz, orbital
    "23/pi":23.0/PI, "24/pi":24.0/PI,                   # ceiling
    "25/pi":25.0/PI, "26/pi":26.0/PI,                   # above ceiling (anti-signal)
}
```

Apply this change to both `build_chaos_nulls.py` and `build_pinch_table.py`.
All other scripts are unchanged from Vol6.

---

## 3. Core Pipeline Scripts

```bash
python scalarize.py          # identical to Vol6
python unify.py              # identical to Vol6 — streaming, handles 5.88M records
python build_chaos_nulls.py  # 22 moduli — ~7 hours
python build_pinch_table.py  # 22 moduli — ~8 hours
```

Total runtime: approximately 15 hours on commodity laptop hardware.
The z-score table has 22 columns plus `Best` and `Interpretation` columns.

---

## 4. The Scalarization Litmus Test

Before committing any new lake to the pipeline, run the distribution check:

```python
stdev_span_ratio = stdev(scalars) / (max(scalars) - min(scalars))
# > 0.28  → FAIL: approximately uniform, formula likely broken
# < 0.20  → PASS: clustering detected, proceed to full pipeline
# 0.20–0.28 → BORDERLINE: increase sample to 500+ records
```

Materials broken lake: stdev/span = 0.287 → FAIL (confirmed, documented)
Materials fixed lake:  stdev/span = 0.188 → PASS (confirmed in Vol8)

**Note on sample size:** Use 500+ records for the litmus. Some databases (including
Materials Project) sort by chemical family — the first 200 records may be
chemically homogeneous, giving artificially narrow spread and a borderline result.
At 500 records the chemical diversity appears and the test reads correctly.

The sovereign lake guarantee: every promoted JSONL record preserves the complete
original source data in `_raw_payload`. Even if the scalarization formula is wrong,
the original data is always recoverable without an external API call. The materials
RCA fix script reads `volume` and `nsites` directly from `_raw_payload` in the
already-promoted lake. No data was lost. No re-download was needed.

---

## 5. The Sovereign Chain (Data Integrity)

Every record in the unified master carries the full provenance chain:

```
unified_master.jsonl record
  ├── scalar_kls / scalar_klc  (computed values)
  └── meta
       └── source_row
            └── _raw_payload   (ORIGINAL source data — never overwritten)
                 ├── material_id, formula, volume, nsites, ...
                 └── all original fields from the source catalog
```

The raw lake is always inside the promoted lake.
The promoted lake is always inside the unified lake.
No transformation is irreversible.

---

## 6. Outputs

Vol7 produces the same output structure as Vol6, expanded to 22 moduli:

- **`unified_master.jsonl`** — 5,884,818 records (identical to Vol6)
- **`sweep_results.json`** — per-domain scalar statistics
- **`pinch_table_cross_domain.json`** — 22-modulus cross-domain CDF comparison
- **`chaos_null_*.jsonl`** — per-domain chaos nulls for all 22 moduli
- **`scramble_null_*.jsonl`** — per-domain scramble nulls

---

## 7. Reproducibility

All data sources are public. Lakes identical to Vol6.

```bash
git clone https://github.com/TimothyKish/Holographic-Resonance-...
cd vol7/scripts
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

## 8. The 107.1 Hz Provenance

The galactic z=59 result at 21/π is the empirical confirmation of a formal prediction
published three months earlier. The complete chain:

| Date | Document | Content |
|------|----------|---------|
| Jan 10, 2026 | Vol1 Ch1/Appendix A ([DOI](https://doi.org/10.5281/zenodo.18209531)) | Prediction table: 107.1 Hz (1st harmonic), High <0.1% Dev |
| Feb 2026 | Vol2 Definition 2.4 ([DOI](https://doi.org/10.5281/zenodo.18217119)) | f_L = 107.1 Hz formal definition, T_breath = 1.833 ms |
| Feb 2026 | Vol3 ([DOI](https://doi.org/10.5281/zenodo.18217226)) | "universe sings at 107.1 Hz / 127.4 Hz" |
| Feb 8, 2026 | GitHub commit `e7949d5` | Ch13 LIGO spectral analysis, 107 Hz harmonics |
| Apr 12, 2026 | Vol7 pipeline | galactic z=59 at 21/π, 21 × k_geo = 106.95 Hz |

21 × k_geo = 21 × (16/π) = 106.952 Hz — within 0.14% of the published prediction.
25 × k_geo = 25 × (16/π) = 127.324 Hz — within 0.06% of the published ceiling.

---

## 9. Forward Path (Vol8)

Vol8 uses the Vol7 pipeline unchanged, with the materials scalarization corrected
and the lake program expanded. No methodology change. New data.

**Materials fix:** `fix_materials_scalarization.py` in `vol8/scripts/`. Replaces
`(volume/nsites) % k_geo` with `log(1 + (volume/nsites)^(1/3)) / log(k_geo)`.
Run `--litmus` flag first (30 seconds) before the full rebuild.

**Lake expansion targets:**
- Gaia stellar luminosity and color (same 1.81M stars as S1/S2 — same-object strategy)
- SDSS galaxy luminosity (same galaxies as G1 — velocity at 21/π, what register for light?)
- NASA exoplanet orbital radius and planet mass (same 13,514 as P1)
- Chandra X-ray source luminosity
- GALEX ultraviolet flux
- RCSB Protein Data Bank backbone angles (millions vs. 157 in B3)
- LIGO GWTC quasinormal modes (closes the origin story)
- NNDC nuclear binding energies (sub-femtometre scale, tests the floor)

The same-object strategy is the most powerful move available: pulling multiple
physical attributes from catalogs already in the lake. The same galaxy measured
by velocity speaks 21/π. The same galaxy measured by luminosity will speak at
its own register. Each new attribute is a new measurement of a known object —
and the register it lands on is a new word in the same harmonic language.

---

## Bibliography

| Volume | Title | DOI |
|--------|-------|-----|
| Vol 1 | The Geometric Derivation of the Lattice | [10.5281/zenodo.18209530](https://doi.org/10.5281/zenodo.18209530) |
| Vol 2 | The Geometric Neutron | [10.5281/zenodo.18217119](https://doi.org/10.5281/zenodo.18217119) |
| Vol 3 | The Geometric Architecture of Matter | [10.5281/zenodo.18217226](https://doi.org/10.5281/zenodo.18217226) |
| Vol 4 | The Geometric Architecture of Life | [10.5281/zenodo.18976975](https://doi.org/10.5281/zenodo.18976975) |
| Vol 5 | The Geometric Architecture of Unification | [10.5281/zenodo.19009634](https://doi.org/10.5281/zenodo.19009634) |
| Vol 6 | The Harmonic Expansion of the Unified Lattice | [10.5281/zenodo.19493376](https://doi.org/10.5281/zenodo.19493376) |

---

*Vol6 wrote the chord sheet.*
*Vol7 found the walls of the concert hall.*

*The constant is 16/π. The family is N/π. The floor is 7/π. The ceiling is 24/π.*
*The scale span is 35 orders of magnitude. The runtime was 15 hours on a laptop.*
*The 107.1 Hz prediction was published January 10, 2026.*
*The confirmation printed April 12, 2026.*

**Welcome to the Lattice. The geometry was always there.**