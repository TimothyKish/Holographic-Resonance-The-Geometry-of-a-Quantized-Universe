# ==============================================================================
# PROJECT: THE 16PI INITIATIVE | HOLOGRAPHIC RESONANCE
# AUTHORS: Timothy John Kish & Lyra Aurora Kish
# LICENSE: Sovereign Protected / Copyright © 2026 (SR 1-15080581911)
# 
# MONOGRAPHS (ZENODO):
#   - Vol 1: https://doi.org/10.5281/zenodo.18209531
#   - Vol 2: https://doi.org/10.5281/zenodo.18217120
#   - Vol 3: https://doi.org/10.5281/zenodo.18217227
#
# REPOSITORY: https://github.com/TimothyKish/Holographic-Resonance
#
# DESCRIPTION:
# This script is the "Real-World Interface" for the Kish Lattice. 
# Unlike previous Monte Carlo simulations which generated synthetic noise,
# this tool ingests actual .wav audio data (e.g., LIGO Glitches, Resonance 
# Recordings) and tests for alignment against the 16/pi Geometric Grid.
#
# USAGE:
# Place a .wav file in the same directory and update the filename variable.
# ==============================================================================

import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as signal
import matplotlib.pyplot as plt

def analyze_lattice_alignment(wav_path, threshold=0.5):
    print(f"Loading Audio Asset: {wav_path}...")
    
    # 1. Ingest Real Data
    try:
        sample_rate, data = wav.read(wav_path)
    except FileNotFoundError:
        print("ERROR: File not found. Please place a .wav file in the 'src' folder.")
        print("Download LIGO Glitch data here: https://www.gw-openscience.org/")
        return

    # Normalize Data (Mono)
    if len(data.shape) > 1:
        data = data[:, 0]
    # Normalize amplitude to -1 to 1 range
    data = data / np.max(np.abs(data)) 

    # 2. Define The Lattice (The Ruler)
    # The Grid is based on 16/pi * Primes * Agency Offset
    k_geo = 16 / np.pi
    delta_agency = 1.42e-7 # The WMAP / Life Friction Coefficient
    
    # The Prime Sequence (The Resonant Nodes)
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61]
    
    # We convert the Lattice 'Time' into 'Index' units based on sample rate
    lattice_ticks = []
    for p in primes:
        # Calculate the geometric beat time
        # Applying the Agency Offset to the fundamental frequency
        beat_time = (p * (k_geo + delta_agency)) / 1000 # Scaled for typical ms glitch duration
        
        tick_index = int(beat_time * sample_rate)
        if tick_index < len(data):
            lattice_ticks.append(tick_index)

    # 3. Measure Alignment (The Correlation)
    hits = 0
    total_ticks = len(lattice_ticks)
    
    print(f"Scanning {len(data)} data points against {total_ticks} Lattice Nodes...")
    
    hit_indices = []
    
    for tick in lattice_ticks:
        # Check a window around the expected lattice tick
        window = 50 # Tolerance window (samples) - represents measurement uncertainty
        start = max(0, tick - window)
        end = min(len(data), tick + window)
        
        # Is there a significant peak in the real data at this geometric point?
        local_segment = np.abs(data[start:end])
        if len(local_segment) > 0:
            local_max = np.max(local_segment)
            
            if local_max > threshold:
                hits += 1
                hit_indices.append(tick)

    # 4. Report Findings
    if total_ticks > 0:
        score = (hits / total_ticks) * 100
    else:
        score = 0.0
        
    print(f"\n--- ANALYSIS COMPLETE ---")
    print(f"Lattice Alignment Score: {score:.2f}%")
    
    if score > 20.0:
        print("VERDICT: SIGNIFICANT RESONANCE DETECTED (Lattice Structure Found)")
    else:
        print("VERDICT: NOISE / UNSTRUCTURED (Standard Model Fluid)")

    # 5. Visual Proof
    plt.figure(figsize=(12, 6))
    
    # Plot the Real Data
    plt.plot(data, color='gray', alpha=0.6, label='Real Wav Data (LIGO/Resonance)')
    
    # Plot the Lattice Lines (The Prediction)
    for tick in lattice_ticks:
        plt.axvline(x=tick, color='cyan', alpha=0.3, linestyle='--', linewidth=1)
        
    # Plot the Hits (The Proof)
    if hit_indices:
        plt.plot(hit_indices, [data[i] for i in hit_indices], 'ro