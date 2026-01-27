# ==============================================================================
# PROJECT: THE 16PI INITIATIVE | REAL DATA INTERFACE (STATISTICAL ENGINE)
# SCRIPT: kish_lattice_wav_scanner.py
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
# This instrument ingests .wav audio data (LIGO Glitches) and performs a 
# "Null Hypothesis Test." It compares the geometric alignment of the real signal
# against 100 randomized "shuffled" versions of itself to determine the 
# Statistical Sigma (Z-Score) of the event.
# ==============================================================================

import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import os

# --- THE GEOMETRIC KERNEL ---
def get_lattice_ticks(sample_rate, data_length):
    """Generates the 16/pi Time Grid with Agency Offset."""
    k_geo = 16 / np.pi
    delta_agency = 1.42e-7 # The WMAP Life Friction Coefficient
    
    # The Resonant Prime Nodes
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73]
    
    ticks = []
    for p in primes:
        # Calculate geometric beat time (ms scaled)
        beat_time = (p * (k_geo + delta_agency)) / 1000 
        tick_index = int(beat_time * sample_rate)
        if tick_index < data_length:
            ticks.append(tick_index)
    return ticks

def compute_score(data, sample_rate, threshold=0.5):
    """Calculates the Alignment Score for a single data array."""
    ticks = get_lattice_ticks(sample_rate, len(data))
    if not ticks:
        return 0.0, []

    hits = 0
    hit_indices = []
    window = 50 # Tolerance window (samples)

    for tick in ticks:
        start = max(0, tick - window)
        end = min(len(data), tick + window)
        local_segment = np.abs(data[start:end])
        
        if len(local_segment) > 0 and np.max(local_segment) > threshold:
            hits += 1
            hit_indices.append(tick)
            
    return (hits / len(ticks)) * 100, hit_indices

# --- THE STATISTICAL ENGINE ---
def analyze_lattice_alignment(wav_path, threshold=0.5, null_trials=100):
    print(f"\nLOADING ASSET: {wav_path}")
    
    try:
        sample_rate, data = wav.read(wav_path)
    except FileNotFoundError:
        print(f"  [!] ERROR: File '{wav_path}' not found.")
        return

    # Normalize Data
    if len(data.shape) > 1: data = data[:, 0]
    data = data / np.max(np.abs(data)) # Normalize -1 to 1

    # 1. MEASURE REALITY
    real_score, hit_indices = compute_score(data, sample_rate, threshold)
    print(f"  > Real Alignment Score: {real_score:.2f}%")

    # 2. THE NULL TEST (Scanning the Static)
    print(f"  > Running {null_trials} Null Comparisons (Shuffling)...")
    null_scores = []
    for _ in range(null_trials):
        shuffled_data = np.random.permutation(data)
        score, _ = compute_score(shuffled_data, sample_rate, threshold)
        null_scores.append(score)
    
    null_mean = np.mean(null_scores)
    null_std = np.std(null_scores)
    
    # 3. THE SIGMA (Z-Score)
    if null_std > 0:
        sigma = (real_score - null_mean) / null_std
    else:
        sigma = 0.0

    print(f"  > Null Mean: {null_mean:.2f}% (Std: {null_std:.2f})")
    print(f"  > STATISTICAL SIGMA: {sigma:.2f}σ")

    # 4. THE VERDICT
    if sigma > 5.0:
        print("  >>> VERDICT: DISCOVERY (5-Sigma). The Signal is Geometric.")
    elif sigma > 3.0:
        print("  >>> VERDICT: PROOF (3-Sigma). Strong Evidence of Lattice.")
    elif sigma > 1.0:
        print("  >>> VERDICT: HINT (1-Sigma). Interesting, but not conclusive.")
    else:
        print("  >>> VERDICT: NOISE. Indistinguishable from static.")

    # 5. VISUAL PROOF (Only plot the Real Data)
    ticks = get_lattice_ticks(sample_rate, len(data))
    plt.figure(figsize=(12, 5))
    plt.plot(data, color='gray', alpha=0.5, label='Real LIGO Strain')
    for tick in ticks:
        plt.axvline(x=tick, color='cyan', alpha=0.3, linestyle='--', linewidth=1)
    if hit_indices:
        plt.plot(hit_indices, [data[i] for i in hit_indices], 'ro', label='Lattice Intersections')
    
    plt.title(f"File: {wav_path} | Score: {real_score:.1f}% | Significance: {sigma:.1f}σ")
    plt.legend(loc='upper right')
    plt.show()

# --- DRIVER ---
if __name__ == "__main__":
    # LIST YOUR FILES HERE (Put them in the src folder)
    test_files = [
        "blip.wav",
        "whistle.wav",
        "koi_glitch.wav"
    ]
    
    print("========================================")
    print("   THE KISH LATTICE SCANNNER (v2.0)   ")
    print("   Statistical Null-Test Engine       ")
    print("========================================")

    for f in test_files:
        if os.path.exists(f):
            analyze_lattice_alignment(f, threshold=0.4, null_trials=100)
        else:
            print(f"\n[!] Skipping {f} (Not found in src folder)")
            
    print("\n[INFO] To test real data, download .wav files from gw-openscience.org")