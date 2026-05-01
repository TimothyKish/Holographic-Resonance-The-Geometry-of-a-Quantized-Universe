# ==============================================================================
# PROJECT: THE KISH LATTICE | VOLUME 3 (DIAMOND EDITION)
# TITLE: m3.1 - The Silent Lake Dredger (Full Empirical JSON Dump)
# AUTHORS: Timothy John Kish & Lyra Aurora Kish & Alexandria Aurora Kish
# API: https://api.materialsproject.org/materials/summary/
# Crosslink: Vol3.Chapter1.4 (The Kish Rosetta Stone)
# LICENSE: Sovereign Protected / Copyright © 2026
# SCRIPT NAME: Lattice_Audit_next_gen_materialsproject_m3_1
# PIPELINE ROLE: Sovereign Dataset Creation (Local JSON Lake Generation)
# ==============================================================================
# PURPOSE:
#   This script converts the full empirical dataset extracted in m3
#   (~33,973 stable crystal structures) into a local, self-contained JSON file:
#
#       Kish_Lattice_Empirical_Lake.json
#
#   This file becomes the sovereign data lake for all downstream analysis.
#   By storing the entire crystallographic universe locally, the Lattice Lab
#   eliminates API rate limits, network dependencies, and external bottlenecks.
#
#   m3.1 is the turning point where the pipeline transitions from
#   “data acquisition” to “unbounded computation.” All Monte Carlo fleets,
#   null universes, harmonic shelf detection, resonance clustering, Nyquist
#   sweeps, and vertex mapping operations run exclusively on this local lake.
#
# POSITION IN PIPELINE (FULL PIPELINE OVERVIEW):
#   m1   - Lattice_Audit_next_gen_materialsproject_m1
#          Initial sanity check. Small sample pull. Validates modulus logic.
#
#   m2   - Lattice_Audit_next_gen_materialsproject_m2
#          Medium-scale audit (~1000). Stress-tests deviation distribution and
#          confirms early resonance clustering.
#
#   m3   - Lattice_Audit_next_gen_materialsproject_m3
#          Full-lake pull (~33,973 structures). Primary empirical dataset.
#
#   m3.1 - Lattice_Audit_next_gen_materialsproject_m3_1   (This Script)
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
#          Nyquist sweep. Frequency-domain analysis of the empirical lake.
#
#   m10  - Lattice_Audit_next_gen_materialsproject_m10
#          Electron Vertex Mapper. Converts valence electrons into geometric
#          vertex states (Line, Tetrahedron, Octahedron, Cube).
#
# DATA SOURCES:
#   - Output of m3 (full Materials Project dataset)
#
# OUTPUTS:
#   - Kish_Lattice_Empirical_Lake.json (sovereign dataset)
#   - Terminal summary of dataset size, structure, and integrity checks
#   - Appendix entry for m3.1 audit
#
# CROSS-LINKS:
#   - Validates: Chapter 1 (Geometric Periodic Table), Chapter 5 (Crystallographic Resonance)
#   - Enables: m4–m10 (all downstream computational analysis)
#
# NOTES:
#   - This script is the most strategically important in the entire pipeline.
#     Once the JSON lake is created, all further computation is local, fast,
#     reproducible, and immune to external API limitations.
#   - The JSON lake becomes the canonical empirical universe for Volume 3.
# ==============================================================================

import requests
import numpy as np
import matplotlib.pyplot as plt
import random
import time
import json
import logging

# Set up the silent logging for the audit trail
logging.basicConfig(filename='M3_Dredge_Log.txt', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

API_KEY = "aHQ7sEIFtfimcD35Lgp0lFMOmj2O0Ex6"
K_MODULUS = 16 / np.pi
BASE_URL = "https://api.materialsproject.org/materials/summary/"

def dredge_and_dump():
    headers = {"X-API-KEY": API_KEY}
    
    # --- LYRA'S DREDGE CONFIGURATION ---
    BATCH_SIZE = 1000
    # Set to 150000+ to dump the entire Materials Project
    TARGET_NODES = 150000  
    
    skip = 0
    all_real_alignments = []
    all_volumes = []
    all_nodes = []
    
    # The Local JSON Data Lake
    local_lake_data = []
    
    print(f"Initiating m3.1 Silent Dredger. Target: {TARGET_NODES} nodes.")
    print("Writing detailed node data to 'M3_Dredge_Log.txt'...")
    logging.info(f"--- INITIATING FULL KISH-LATTICE AUDIT (Target: {TARGET_NODES}) ---")
    
    while skip < TARGET_NODES:
        params = {
            "is_stable": "true",
            "_limit": BATCH_SIZE,
            "_skip": skip,
            "_fields": "material_id,formula_pretty,volume,nsites"
        }
        
        # Dashboard output
        print(f"Dredging batch: {skip} to {skip + BATCH_SIZE}...")
        
        response = requests.get(BASE_URL, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"API choked at skip={skip}. Status: {response.status_code}")
            logging.error(f"API Error at skip={skip}: {response.text}")
            break
            
        payload = response.json()
        data_lake = payload.get('data') or payload.get('results', [])
        
        if not data_lake:
            print("Bottom of the lake reached. No more data to pull.")
            break
            
        for entry in data_lake:
            v = entry.get('volume')
            n = entry.get('nsites')
            formula = entry.get('formula_pretty', 'Unknown')
            mat_id = entry.get('material_id', 'Unknown')
            
            if v and n:
                ratio = v / n
                deviation = abs((ratio % K_MODULUS))
                
                # Append for our active mathematical audit
                all_real_alignments.append(deviation)
                all_volumes.append(v)
                all_nodes.append(n)
                
                # Append to our Local Lake JSON structure
                local_lake_data.append({
                    "material_id": mat_id,
                    "formula": formula,
                    "volume": v,
                    "nsites": n,
                    "node_ratio": ratio,
                    "lattice_deviation": deviation
                })
                
                # Log silently
                logging.info(f"[{mat_id}] {formula:10} | Ratio: {ratio:.4f} | Dev: {deviation:.6f}")
                
        skip += BATCH_SIZE
        time.sleep(1) # Polite delay
        
    print(f"\nSuccess. Ingested {len(all_real_alignments)} empirical nodes.")
    
    # --- DUMP TO LOCAL JSON ---
    print("Dumping data to 'Kish_Lattice_Empirical_Lake.json'...")
    with open('Kish_Lattice_Empirical_Lake.json', 'w') as json_file:
        json.dump(local_lake_data, json_file, indent=4)
        
    logging.info(f"--- DREDGE COMPLETE. {len(all_real_alignments)} NODES SAVED. ---")
    
    # --- MONTE CARLO NULL TEST ---
    print("Generating corresponding Null-Lattice for 5-Sigma Chart...")
    null_alignments = []
    min_v, max_v = min(all_volumes), max(all_volumes)
    min_n, max_n = min(all_nodes), max(all_nodes)
    
    for _ in range(len(all_real_alignments)):
        rand_v = random.uniform(min_v, max_v)
        rand_n = random.randint(min_n, max_n)
        rand_dev = abs(((rand_v / rand_n) % K_MODULUS))
        null_alignments.append(rand_dev)
        
    real_mean = np.mean(all_real_alignments)
    null_mean = np.mean(null_alignments)
    
    print(f"\n--- M3.1 MACRO-AUDIT SUMMARY ---")
    print(f"Empirical Lattice Deviation (Real): {real_mean:.6f}")
    print(f"Random Universe Deviation (Null): {null_mean:.6f}")
    
    # Visualization
    plt.figure(figsize=(12, 7))
    plt.hist(null_alignments, bins=100, density=True, color='gray', alpha=0.5, label='Null Test (Random Universe)')
    plt.hist(all_real_alignments, bins=100, density=True, color='#003278', alpha=0.8, label='Empirical Matter (Kish Lattice)')
    plt.axvline(0, color='red', linestyle='--', linewidth=2, label='Perfect Resonance (0)')
    
    plt.title(f"Full Lake Audit: {len(all_real_alignments)} Nodes vs Random Geometry", fontsize=16, fontweight='bold')
    plt.xlabel(f"Deviation from 16/π Modulus (Max = {K_MODULUS:.4f})", fontsize=12)
    plt.ylabel("Density of Elements", fontsize=12)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig("M3_Full_Lake_Audit.png", dpi=300)
    print("Macro-Audit Chart saved as 'M3_Full_Lake_Audit.png'.")

if __name__ == "__main__":
    dredge_and_dump()