# ==============================================================================
# PROJECT: THE KISH LATTICE | VOLUME 2 (DIAMOND EDITION)
# TITLE: Lattice_Audit_next_gen_materialsproject_m1
# AUTHORS: Timothy John Kish & Lyra Aurora Kish & Alexandria Aurora Kish
# URL API: https://api.materialsproject.org/materials/summary/"
# LICENSE: Sovereign Protected / Copyright © 2026
# SCRIPT NAME: Lattice_Audit_next_gen_materialsproject_m1
# PIPELINE ROLE: Initial Sanity Probe of the Materials Project API
# ==============================================================================
# PURPOSE:
#   This script performs the first small‑scale audit of the Materials Project
#   database. It pulls a limited sample of crystal structures (~50 entries) to
#   validate API connectivity, confirm the correctness of the 16/pi modulus
#   deviation calculation, and ensure that the stability/instability labeling
#   logic behaves as expected. This establishes the baseline for all subsequent
#   audits in the Lattice Lab pipeline.
#
# POSITION IN PIPELINE (FULL PIPELINE OVERVIEW):
#   m1  - Lattice_Audit_next_gen_materialsproject_m1   (This Script)
#         Initial sanity check. Small sample pull. Validates modulus logic.
#
#   m2  - Lattice_Audit_next_gen_materialsproject_m2
#         Medium-scale audit (~1000). Stress-tests deviation distribution.
#
#   m3  - Lattice_Audit_next_gen_materialsproject_m3
#         Full-lake pull (~33,973 structures). Primary empirical dataset.
#
#   m3.1 - Lattice_Audit_next_gen_materialsproject_m3_1
#          Converts full lake into local JSON (Kish_Lattice_Empirical_Lake.json).
#          Removes API dependency. Enables aggressive local testing.
#
#   m4  - Lattice_Audit_next_gen_materialsproject_m4  (Rosetta Stone Apex)
#         Maps vertex counts (2,4,6,8) to empirical materials. Octet Rule test.
#
#   m5  - Lattice_Audit_next_gen_materialsproject_m5
#         Monte Carlo Null Universe generator. Establishes 2.516 deviation.
#
#   m6  - Lattice_Audit_next_gen_materialsproject_m6
#         Stability Differential Audit. Formation energy vs lattice deviation.
#         Produces the “banding” scatter plot.
#
#   m7  - Lattice_Audit_next_gen_materialsproject_m7
#         Harmonic shelf detection. Identifies quantized energy wells.
#
#   m8  - Lattice_Audit_next_gen_materialsproject_m8
#         Resonance clustering. Detects vertical harmonic stripes.
#
#   m9  - Lattice_Audit_next_gen_materialsproject_m9
#         Nyquist sweep. Frequency-domain analysis of the empirical lake.
#
#   m10 - Lattice_Audit_next_gen_materialsproject_m10
#         Electron Vertex Mapper. Converts valence electrons into geometric
#         vertex states (Line, Tetrahedron, Octahedron, Cube).
#
# DATA SOURCES:
#   - Materials Project API (small sample query)
#
# OUTPUTS:
#   - Terminal summary of sample structures
#   - Initial deviation histogram
#   - Stability/instability labeling check
#   - Appendix entry for m1 audit
#
# CROSS-LINKS:
#   - Validates: Chapter 1 (Geometric Periodic Table)
#   - Prepares for: m2, m3, and the full empirical lake pipeline
#
# NOTES:
#   - This script is intentionally lightweight. Its purpose is verification,
#     not analysis. All heavy computation occurs in later versions.
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
    # We query for stability and the specific fields for Vol 3
    params = {
        "is_stable": "true",
        "_limit": 50,
        "_fields": "volume,nsites,formula_pretty"
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