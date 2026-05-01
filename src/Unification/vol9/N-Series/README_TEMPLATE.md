# N-Series: The Methodological Null [Domain Name, e.g., N4_Temporal]

## 🎯 Purpose
This domain serves as a methodological control group for Volume 5 of the Kish Lattice framework. It tests whether the geometric resonances observed in the primary physical domains (M-Series, C-Series, B-Series) are artifacts of the pipeline or true physical properties. By processing pure noise or scrambled data through the exact same unification pipeline, we establish a baseline for collapse.

## 📊 Data Source & Construction
* **Source:** [e.g., Authentic Temporal Lake observations (Redshift z, Distance d)]
* **Null Construction:** [e.g., Z-values remain fixed, but distance values are randomly shuffled, destroying the physical relationship while preserving the statistical distribution.]

## ⚙️ Expected Behavior (The Collapse)
Because this lake lacks true $16/\pi$ geometric structure, it must:
1. Yield an empty `geometry_payload`.
2. Return `0.0` for all scalar invariants (`scalar_kls`, `scalar_klc`).
3. Completely collapse in the Volume 5 Pinch Table, showing zero cross-domain resonance.


## 🧪 Reproducibility Chain-of-Custody
To verify the collapse, run the pipeline in strict sequential order:
1. `python scripts/build_lake.py`
2. `python scripts/promote.py`
3. `python scripts/scalarize.py`
4. `python scripts/validate.py`
5. `python scripts/pinch.py`