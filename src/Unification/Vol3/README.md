# Vol 3 — Materials + Chemistry Unification (M‑series, C‑series, UMC1–UMC7)

Vol 3 is the first volume where two scientific domains — **Materials** and **Chemistry** — coexist in a unified, geometry‑first framework.  
It contains:

- the **sovereign Materials lake** (M‑series)  
- the **sovereign Chemistry lake** (C‑series)  
- the **merged clean lake**  
- the **UMC1–UMC7 unification track**  
- the **figures and reports** that demonstrate cross‑domain harmonic alignment  

Vol 3 is the bridge between domain‑native pipelines (Vol 1–Vol 4) and the global unification layer (Vol 5).

---

## 1. Directory Overview

vol3/
│
├── lakes/
│   ├── materials/        # sovereign M-series lake
│   ├── chemicals/        # sovereign C-series lake
│   └── clean/            # merged + cleaned lake for UMC
│
├── scripts/
│   ├── mseries/          # materials pipeline
│   ├── cseries/          # chemistry pipeline
│   └── umc/              # UMC1–UMC7 runners
│
├── figures/
│   ├── mseries/
│   ├── cseries/
│   └── umc/
│
├── reports/
│   └── umc/
│
├── manuscript/
│
├── Title
│
├── Lattice_Audit_Chemistry_legacy/        # archived audit trail
├── Lattice_Audit_Chemistry_20260303_legacy/
└── Lattice_Audit_Materials_legacy/


The **legacy folders** contain historical extraction pipelines, raw ZINC tranches, manifests, and early geometry workflows.  
They are preserved for auditability but are no longer part of the active pipeline.

---

## 2. Purpose of Vol 3

Vol 3 has three responsibilities:

### 1. Produce sovereign domain lakes  
- **M‑series** → Materials  
- **C‑series** → Chemistry  

These lakes are geometry‑first, JSONL‑native, and scalarized using the Kish Lattice Scalar (KLS).

### 2. Merge and clean the lakes  
The merged lake is written to:


lakes/clean/


This lake is the input to UMC1–UMC7.

### 3. Run the UMC1–UMC7 unification track  
UMC is the **Materials ↔ Chemistry** unification ladder:

| Step | Name | Purpose |
|------|------|---------|
| UMC1 | Scalar Comparison | Compare KLS distributions |
| UMC2 | Distributions | Overlay domain distributions |
| UMC3 | Harmonic Shelves | Identify shared shelves |
| UMC4 | Resonance | Cross-domain resonance peaks |
| UMC5 | Coupling | Coupling strength + alignment |
| UMC6 | Cascade | Harmonic cascade across domains |
| UMC7 | Final Coordinate | Produce KLC‑MC (unified coordinate) |

UMC7 produces the first cross‑domain coordinate:


KLC-MC


This is later pulled into Vol 5.

---

## 3. Sovereign Lakes

### Materials Lake (M‑series)
Located in:


lakes/materials/


Produced by:

scripts/mseries/

### Chemistry Lake (C‑series)
Located in:

lakes/chemicals/

Produced by:
scripts/cseries/

### Clean Merged Lake
Located in:


lakes/clean/


This is the input to UMC1–UMC7.

---

## 4. UMC1–UMC7 Outputs

### Scripts
scripts/umc/

### Figures

figures/umc/
figures/umc/


### Reports
reports/umc/


### Final Unified Coordinate
UMC7 writes:

lakes/clean/klc_mc.jsonl


This file contains the **Kish Lattice Coordinate for Materials ↔ Chemistry**.

Vol 5 will ingest this file during the global unification.

---

## 5. Relationship to Vol 5

Vol 3 produces the **first cross‑domain unification coordinate** (KLC‑MC).  
Vol 5 later pulls:

- the sovereign lakes  
- the UMC7 output  
- the KLC‑MC coordinate  

and merges them into the **Vol 5 Unified Lake**.

Vol 3 is therefore the **first empirical test** of the Kish Lattice unification.

---

## 6. Status

- Sovereign M‑series and C‑series lakes: **complete**  
- Legacy audit trails: **archived**  
- Clean merged lake: **ready**  
- UMC1–UMC7: **to be implemented**  
- Vol 5 ingestion: **ready once UMC7 is complete**

Vol 3 is now structurally clean, sovereign, and ready for the UMC unification track.

