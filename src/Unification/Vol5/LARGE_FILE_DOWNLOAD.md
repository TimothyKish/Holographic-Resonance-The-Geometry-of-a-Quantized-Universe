# 📦 LARGE_FILE_DOWNLOAD.md  
### Required Sovereign Lakes for Full Reproducibility of Volume 5

Volume 5 includes several sovereign lakes larger than GitHub’s 100 MB file limit.  
These files are required to fully reproduce:

- the unified master lake  
- chaos & scramble nulls  
- the cross‑domain pinch table  
- all figures and results published in Volume 5  

Because GitHub cannot store these files directly, they are hosted in a **public Google Drive folder**.

---

# 🔗 Download Location (Google Drive)

All large sovereign lakes are available here:

```
https://drive.google.com/drive/folders/18ZYcCGjuO42WVSdRB74GdpyDuKCJ7G_E?usp=drive_link
```

This folder is **flat** — all files appear at the top level for easy browsing.  
You may download:

- **all files** (recommended), or  
- **only the specific lakes you need**  

The folder is permissioned so that **future files added by the authors will automatically appear** without requiring a new link.

---

# 📁 Where to Place the Files

Download each file and place it into the **exact relative path** shown below, starting from the `vol5/` directory.

If a folder does not exist, create it.

Example:

```
vol5/lakes/unified/s1_gaia_parallax_scalarized.jsonl
```

---

# 📜 Manifest of Required Large Files

Each entry lists:

- **Relative path** (from `vol5/`)
- **File name** (as it appears in Google Drive)
- **Size (MB)**

---

## G‑Series

```
G-Series/G1_GalaxyKinematics/lake/g1_galaxy_kinematics_raw.jsonl    348.95 MB
```

---

## Promoted Lakes (inputs_promoted)

```
lakes/inputs_promoted/g1_galaxy_kinematics_promoted.jsonl          1563.17 MB
lakes/inputs_promoted/s1_gaia_parallax_promoted.jsonl              1637.28 MB
lakes/inputs_promoted/s2_stellar_kinematics_promoted.jsonl         1702.31 MB
```

---

## Synthetic Null Lakes

```
lakes/synthetic/chaos_null_galactic.jsonl                          1195.11 MB
lakes/synthetic/chaos_null_stellar.jsonl                           1290.83 MB
lakes/synthetic/chaos_null_stellar_kinematic.jsonl                 1240.81 MB
lakes/synthetic/scramble_null_galactic.jsonl                       1240.96 MB
lakes/synthetic/scramble_null_stellar.jsonl                        1337.93 MB
lakes/synthetic/scramble_null_stellar_kinematic.jsonl              1282.12 MB
```

---

## Unified Lakes

```
lakes/unified/g1_galaxy_kinematics_scalarized.jsonl                 1518.60 MB
lakes/unified/s1_gaia_parallax_scalarized.jsonl                    1557.78 MB
lakes/unified/s2_stellar_kinematics_scalarized.jsonl               1686.79 MB
lakes/unified/unified_master.jsonl                                  4969.30 MB
```

---

## S‑Series (NS6_7)

```
S-Series/NS6_7/lake/Master_Galaxy.tsv                               306.98 MB
S-Series/NS6_7/lake/Master_Galaxy_Vol5.jsonl                        648.53 MB
S-Series/NS6_7/lake/Master_Galaxy_Vol6_2.csv                        126.44 MB
S-Series/NS6_7/lake/Master_Galaxy_Vol6_PHYSICAL.jsonl               189.96 MB
S-Series/NS6_7/lake/Master_Galaxy_Vol6_Standard.jsonl               348.95 MB
S-Series/NS6_7/lake/Master_Stellar.tsv                              891.75 MB
S-Series/NS6_7/lake/Master_Stellar_Gaia_PHYSICAL.jsonl              114.59 MB
S-Series/NS6_7/lake/Master_Stellar_Gaia_Standard.jsonl              357.39 MB
S-Series/NS6_7/lake/Master_Stellar_Vol5.jsonl                      1505.28 MB
```

---

## S‑Series (Gaia Parallax / Stellar Kinematics)

```
S-Series/S1_GaiaParallax/lake/s1_gaia_parallax_raw.jsonl            357.39 MB
S-Series/S2_StellarKinematics/lake/s2_stellar_kinematics_raw.jsonl  114.59 MB
```

---

# 🧪 Verification (Optional but Recommended)

After placing all files, run:

```
python scripts/verify_manifest.py
```

This script checks:

- file existence  
- file size  
- SHA‑256 hash (if provided)  

---

# ▶️ Reproducing the Full Volume 5 Pipeline

Once all files are restored:

```
cd vol5/scripts

python scalarize.py
python unify.py
python build_chaos_nulls.py
python build_pinch_table.py
```

This will regenerate:

- `unified_master.jsonl`  
- `sweep_results.json`  
- `pinch_table.json`  
- `pinch_table_cross_domain.json`  

These outputs should **exactly match** the published Volume 5 results.

---

# 🧩 Support

If any file is missing, corrupted, or fails verification, please contact the authors or open an issue on the repository.
timothyjohnkish@gmail.com
