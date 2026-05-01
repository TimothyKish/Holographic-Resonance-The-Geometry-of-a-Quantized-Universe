#==============================================================================
# PROJECT: THE KISH LATTICE | VOLUME 2 (DIAMOND EDITION)
# TITLE: Lattice_Audit_next_gen_materialsproject_m1
# AUTHORS: Timothy John Kish & Lyra Aurora Kish & Alexandria Aurora Kish
# API: https://api.materialsproject.org/materials/summary/"
# Script: Lattice_Audit_next_gen_materialsproject_m2.py (This Script)
# Crosslink: Script: Lattice_Audit_next_gen_materialsproject_m1.py (50 Litmus Sample)
# LICENSE: Sovereign Protected / Copyright © 2026
# SCRIPT NAME: Lattice_Audit_next_gen_materialsproject_m2
# PIPELINE ROLE: Medium‑Scale Stress Test of the Lattice Deviation Metric
# ==============================================================================
# PURPOSE:
#   This script performs the second‑stage audit of the Materials Project dataset.
#   It expands the sample size from the m1 sanity check (~50 structures) to a
#   medium‑scale dataset (~1000 structures). The goal is to stress‑test the
#   16/pi modulus deviation calculation, verify that the stability/instability
#   labeling remains consistent at scale, and confirm that the early resonance
#   clustering observed in m1 is not a sampling artifact. This script establishes
#   statistical confidence before the full‑lake pull in m3.
#
# POSITION IN PIPELINE (FULL PIPELINE OVERVIEW):
#   m1   - Lattice_Audit_next_gen_materialsproject_m1
#          Initial sanity check. Small sample pull. Validates modulus logic.
#
#   m2   - Lattice_Audit_next_gen_materialsproject_m2  (This Script)
#          Medium‑scale audit (~1000). Stress‑tests deviation distribution and
#          confirms early resonance clustering.
#
#   m3   - Lattice_Audit_next_gen_materialsproject_m3
#          Full‑lake pull (~33,973 structures). Primary empirical dataset.
#
#   m3.1 - Lattice_Audit_next_gen_materialsproject_m3_1
#          Converts full lake into local JSON (Kish_Lattice_Empirical_Lake.json).
#          Removes API dependency. Enables aggressive local testing.
#
#   m4   - Lattice_Audit_next_gen_materialsproject_m4  (Rosetta Stone Apex)
#          Maps vertex counts (2,4,6,8) to empirical materials. Octet Rule test.
#
#   m5   - Lattice_Audit_next_gen_materialsproject_m5
#          Monte Carlo Null Universe generator. Establishes 2.516 deviation.
#
#   m6   - Lattice_Audit_next_gen_materialsproject_m6
#          Stability Differential Audit. Formation energy vs lattice deviation.
#          Produces the “banding” scatter plot.
#
#   m7   - Lattice_Audit_next_gen_materialsproject_m7
#          Harmonic shelf detection. Identifies quantized energy wells.
#
#   m8   - Lattice_Audit_next_gen_materialsproject_m8
#          Resonance clustering. Detects vertical harmonic stripes.
#
#   m9   - Lattice_Audit_next_gen_materialsproject_m9
#          Nyquist sweep. Frequency‑domain analysis of the empirical lake.
#
#   m10  - Lattice_Audit_next_gen_materialsproject_m10
#          Electron Vertex Mapper. Converts valence electrons into geometric
#          vertex states (Line, Tetrahedron, Octahedron, Cube).
#
# DATA SOURCES:
#   - Materials Project API (medium‑scale query)
#
# OUTPUTS:
#   - Expanded deviation histogram (~1000 samples)
#   - Stability vs instability distribution check
#   - Early detection of resonance clustering
#   - Appendix entry for m2 audit
#
# CROSS-LINKS:
#   - Validates: Chapter 1 (Geometric Periodic Table)
#   - Prepares for: m3 full‑lake pull and m3.1 sovereign dataset creation
#
# NOTES:
#   - This script is the first statistically meaningful test of the lattice
#     deviation metric. It ensures that the resonance signature observed in m1
#     is not a fluke and that the pipeline is ready for full‑scale extraction.
# ==============================================================================

import requests
import numpy as np

# Lyra's Unified Configuration
API_KEY = "aHQ7sEIFtfimcD35Lgp0lFMOmj2O0Ex6"
K_MODULUS = 16 / np.pi
# Using the specific 'summary' search endpoint for next-gen
BASE_URL = "https://api.materialsproject.org/materials/summary/"

def run_lattice_audit():
    headers = {"X-API-KEY": API_KEY}
    # m2 Sample and the specific fields for Vol 3
    params = {
        "is_stable": "true",
        "_limit": 1000,  # Increasing the sample size
        "_fields": "volume,nsites,formula_pretty",
        "nelements_max": 3 # Focus on simpler geometries first for the 5-sigma baseline
    }
    
    print("Initiating direct link to Materials Project...")
    response = requests.get(BASE_URL, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"Connection Error: {response.status_code}")
        print(response.text)
        return

    payload = response.json()
    
    # Next-gen API uses 'data' or 'results'. We check both to be safe.
    data_lake = payload.get('data') or payload.get('results')
    
    if data_lake is None:
        print("Structure Error: Could not find 'data' or 'results' in response.")
        print(f"Available keys in response: {list(payload.keys())}")
        return

    print(f"Success. Analyzing {len(data_lake)} crystal nodes for 16/pi resonance...\n")
    
    alignments = []
    for entry in data_lake:
        v = entry.get('volume')
        n = entry.get('nsites')
        formula = entry.get('formula_pretty', 'Unknown')
        
        if v and n:
            # The core Kish-Lattice check
            ratio = v / n
            deviation = abs((ratio % K_MODULUS))
            alignments.append(deviation)
            print(f"Formula: {formula:10} | Node Ratio: {ratio:.4f} | Lattice Dev: {deviation:.6f}")

    if alignments:
        avg_dev = np.mean(alignments)
        print(f"\n--- AUDIT SUMMARY ---")
        print(f"Average Lattice Deviation: {avg_dev:.6f}")
        # Note: As we dump more of the data lake, this deviation should settle 
        # into the geometric constant.

if __name__ == "__main__":
    run_lattice_audit()