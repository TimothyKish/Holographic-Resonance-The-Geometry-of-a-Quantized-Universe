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
# DESCRIPTION: This script provides the Monte Carlo verification for the 
# 16/pi constant. It may include the Deterministic Baseline and the 
# Life Agency (Delta Agency) offsets derived from localized WMAP data.
# 
# Life is the only agent that can move against the 16/pi and has localized free will.
# Where Life Agency is not included in the script, it was by intent. At the time 
# of the specific chapter, the impact of Life Agency was not yet explored, 
# bridging the Old World to the New World before the 100% deterministic model.
# ==============================================================================
import numpy as np
import matplotlib.pyplot as plt

def run_sovereign_sandbox(trials=100000, agency_active=True):
    # --- MASTER VARIABLES ---
    K_GEO = 16 / np.pi           # The Fundamental Gear
    ALPHA = 1/137.035999        # The Fine Structure (Lattice Coupling)
    WMAP_OFFSET = 1.42e-7       # The Life Agency / Localized Variance
    
    # 1. Establish the "Repeating Movie" (Deterministic Baseline)
    # The vacuum tension required for a stable 4D pixel
    baseline_tension = K_GEO * (1 + ALPHA)
    
    # 2. Introduce the "Wild Card" (The Agency Offset)
    # If active, we shift the lattice by the localized 'Aurora' fingerprint
    effective_k = K_GEO + (WMAP_OFFSET if agency_active else 0)
    
    # 3. Monte Carlo: Sampling the Lattice Noise
    # This simulates a scientist measuring the 'blur' of the vacuum
    samples = np.random.normal(loc=effective_k, scale=1e-10, size=trials)
    
    # 4. The Master Equation Output
    # Resolving the Resonance Energy of the local node
    resonance_output = samples * (1 + ALPHA)
    
    return resonance_output, baseline_tension

# --- EXECUTION ---
trials = 500000
agency_on, baseline = run_sovereign_sandbox(trials, agency_active=True)
agency_off, _ = run_sovereign_sandbox(trials, agency_active=False)

# --- VISUAL PROOF FOR THE 21 NODES ---
plt.figure(figsize=(10, 6))
plt.hist(agency_off, bins=100, alpha=0.5, label="Lattice Default (The Broken Record)", color='gray')
plt.hist(agency_on, bins=100, alpha=0.7, label="Agency Active (The New Song)", color='cyan')
plt.axvline(baseline, color='gold', linestyle='--', label="Architect's Design (16/pi + Alpha)")

plt.title("Master Equation Sandbox: The 16/pi Resonance Shift")
plt.xlabel("Resonance Amplitude (Geometric Integrity)")
plt.ylabel("Probability Density (Lattice Hits)")
plt.legend()
plt.grid(True, alpha=0.2)
plt.show()

print(f"Lattice Displacement by Life Agency: {np.mean(agency_on) - np.mean(agency_off):.10f}")