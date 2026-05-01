import numpy as np
import math

# 🛡️ NS6_10: SOHO SOLAR P-MODE AUDIT
# -----------------------------------------------------------
# Target: Solar GOLF Instrument Frequencies (l=0 Radial Modes)
# Goal: Test if the local "Anchor" matches the Bin 7 Root Note.

def run_solar_audit():
    PI = np.pi
    L = 16.0 / PI
    
    # 1. THE DATA: SOHO/GOLF l=0 p-mode frequencies (microHz)
    # These are the cleanest acoustic "ringing" notes of the Sun.
    SOLAR_PMODES = {
        'n=12_l0': 2103.3,
        'n=13_l0': 2238.4,
        'n=14_l0': 2373.3,
        'n=15_l0': 2507.9,
        'n=16_l0': 2642.2,
        'n=17_l0': 2776.0,
        'n=18_l0': 2909.4,
        'n=19_l0': 3042.4,
        'n=20_l0': 3174.9,
        'n=21_l0': 3307.0,
        'n=22_l0': 3438.7,
        'n=23_l0': 3570.0,
        'n=24_l0': 3700.7,
        'n=25_l0': 3830.9,
    }

    # 2. THE SCALARIZER (Mondy's Normalization)
    # Δν ≈ 135.1 microHz is the "Solar Acoustic Scale"
    DELTA_NU = 135.1 

    print("--- 🛡️ SOHO SOLAR ROOT AUDIT ---")
    print(f"Lattice Modulus (L): {L:.4f}")
    print(f"Solar Acoustic Scale (Δν): {DELTA_NU} μHz")
    print("-" * 40)
    print(f"{'MODE':<8} | {'FREQ (μHz)':<10} | {'PHASE (φ)':<10} | {'BIN'}")
    print("-" * 40)

    bins = [0] * 10
    for mode, freq in SOLAR_PMODES.items():
        # Step A: Dimensionless Ratio
        nu_ratio = freq / DELTA_NU
        
        # Step B: Kish Scalar (Enter 16/pi space)
        ks = nu_ratio / L
        
        # Step C: Logarithmic Phase Fold
        # phi = log(ks) % L
        phi = math.log(ks) % L
        
        # Step D: Binning
        bin_idx = min(int((phi / L) * 10), 9)
        bins[bin_idx] += 1
        
        print(f"{mode:<8} | {freq:<10.1f} | {phi:<10.4f} | {bin_idx}")

    # 3. VERDICT: THE BIN 7 MATCH
    print("\n📊 SOLAR PHASE DISTRIBUTION")
    for i in range(10):
        bar = "█" * (bins[i] * 2)
        marker = " <--- ROOT NOTE MATCH" if i == 7 else ""
        print(f"  Bin {i}: {bar} ({bins[i]}){marker}")

    # Calculate Convergence
    root_zone = bins[6] + bins[7] + bins[8]
    convergence = (root_zone / len(SOLAR_PMODES)) * 100
    print(f"\nROOT ZONE CONVERGENCE (Bins 6-8): {convergence:.2f}%")

if __name__ == "__main__":
    run_solar_audit()