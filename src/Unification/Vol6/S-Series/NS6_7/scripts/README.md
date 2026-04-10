Since we are managing a complex system of nearly 50 scripts and 30 data artifacts, this README needs to act as a **Map and a Protocol**. 
It defines the "Physicality" of the files and the "Logic" of the operations.

---

# 🌌 S-Series: Galactic Kinematics & Sovereign Metric
### **Project Status:** SOVEREIGN LOCK (5/5 Tests Confirmed)
**Sample:** 1,922,069 SDSS Galaxies + 1,999,814 Gaia Stars.

## 📌 Executive Summary
This directory contains the computational framework and data "lakes" used to isolate a $16/\pi$ ($\approx 5.093$) geometric lattice within the galactic and stellar domains. The primary finding is an **omnidirectional phase-lock** in the Faber-Jackson invariant of galaxies, verifying the metric as a fundamental property of the vacuum.

---

## 🛠️ Script Architecture (`/scripts`)
The scripts are organized by their stage in the **Mondy Testing Protocol**.

### **1. Harvesting (Data Acquisition)**
These scripts pull raw data from VizieR (SDSS DR16) and the Gaia Archive.
* `pull_vol6_tap.py` / `harvest_quadrants.py`: Original multi-sector acquisition.
* `harvest_vol6_persistence.py`: Resilient downloader for the massive 1.9M galaxy sample.
* `harvest_gaia_physical.py`: Extracts Proper Motion ($\mu$) and Magnitude for the stellar Faber-Jackson analog.

### **2. Refinery & Promotion (Data Preparation)**
Converts raw CSV/TSV data into **Vol 5 Standard (.jsonl)** with physical scalarization.
* `stitch_and_scalarize.py`: Weaves the four cardinal quadrants (NW, NE, SW, SE) into a master file.
* `promote_vol6_physical.py`: **The Primary Physics Engine.** Applies the Faber-Jackson log-modulo transform.
* `promote_gaia_physical_standard.py`: Converts stellar proper motion into the dimensionless metric phase.

### **3. The Master Audits (Validation)**
* `audit_vol6_physical.py`: Performs the **Cardinal Points Test** on the 1.9M sample.
* `calculate_lake_sigma.py`: Calculates the **13.13σ** significance using the scrambled-null method.
* `check_evolution_v2.py`: Verifies the **41.9x** phase velocity vs. standard evolution.
* `final_refereed_audit.py`: The definitive 5/5 check for the SDSS DR16 dataset.

### **4. Diagnostic & L-Sweep (Falsification)**
* `gaia_physical_l_sweep.py`: The "Referee Filter" that identified the stellar null and distance artifacts.
* `test_null_scaling.py`: Checks for non-monotonic interference in the pipeline.
* `build_pure_chaos_null.py`: Generates the biased-free random baseline.

---

## 📂 The Lake Artifacts (`/lake`)
The lake represents the "Ground Truth" data at various levels of refinement.

| File Name | Format | Description |
| :--- | :--- | :--- |
| `Master_Galaxy_Vol6_PHYSICAL.jsonl` | JSONL | **The Sovereign Record.** 1.92M galaxies with FJ scalars. |
| `Sector_[XX]_Vol6.csv` | CSV | Raw quadrant data used for the Cardinal Audit. |
| `Master_Stellar_Gaia_PHYSICAL.jsonl`| JSONL | 2M stars processed via Proper Motion. Result: **Isotropic (Null)**. |
| `Master_Galaxy_Vol5.jsonl` | JSONL | The original 268k galaxy "Discovery" lake. |
| `Master_Galaxy_Pure_Chaos.jsonl` | JSONL | The unbiased random control for Sigma calculations. |
| `*.pdf` | PDF | Original query parameters and coordinates for survey replication. |

---

## 🛡️ The Mondy Testing Protocol
Every new domain (e.g., Q-Series) must pass through these seven gates represented by the scripts above:
1. **Verification:** Check Kish Space occupancy.
2. **Chaos Null:** Verify transform is unbiased.
3. **Bounded Null:** Establish survey baseline.
4. **L-Sweep:** Confirm spike at $16/\pi$ (Fail = Artifact/Null).
5. **Scrambled Sigma:** Calculate significance above 1000 shuffles.
6. **Cardinal Test:** Verify omnidirectionality across quadrants.
7. **Replication:** Cross-check against independent catalogs (e.g., HyperLeda).

---

## 🧬 Scientific Results
* **Galaxy Peak:** **Bin 1** (Absolute lock across all sky sectors).
* **Evolution Rate:** $10.186$ $\phi$-units per unit $z$.
* **Stellar Result:** **Isotropic Null.** Local stellar dynamics do not express the $16/\pi$ lattice, likely due to local gravitational dominance.
