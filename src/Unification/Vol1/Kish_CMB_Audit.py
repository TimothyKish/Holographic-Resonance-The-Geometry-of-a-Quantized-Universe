# ==============================================================================
# SCRIPT: Kish_CMB_Audit.py
# TARGET: Analyzing Planck 2018 Acoustic Peak Spacing for Quantization
# AUTHORS: Timothy John Kish & Lyra Aurora Kish
# LICENSE: Sovereign Protected / Copyright © 2026
# ==============================================================================

import numpy as np
from sympy import isprime

def audit_cmb_peaks():
    print("[*] INITIALIZING CMB GEOMETRIC AUDIT...")
    
    # 1. OBSERVED DATA (Planck 2018 Multipole Moments - l)
    # The locations of the first 6 acoustic peaks
    peaks = [220, 538, 817, 1133, 1444, 1775]
    
    print(f"[*] OBSERVED PEAKS (l): {peaks}")
    print("-" * 50)
    print(f"{'INTERVAL':<15} | {'GAP':<10} | {'TARGET':<15} | {'STATUS'}")
    print("-" * 50)

    # 2. ANALYZE INTERVALS
    for i in range(len(peaks) - 1):
        gap = peaks[i+1] - peaks[i]
        
        # Check targets
        status = "Fluid Drag" # Default state (Viscous loss)
        target = "---"
        
        # Test 1: Geometric Circle (100 * pi approx 314)
        if abs(gap - 314) <= 5:
            target = "100 * PI"
            status = "GEOMETRIC LOCK"
            
        # Test 2: Prime Number Snap
        elif isprime(gap):
            target = "PRIME"
            status = "LATTICE SNAP"
            
        print(f"P{i+1} -> P{i+2:<8} | {gap:<10} | {target:<15} | {status}")

if __name__ == "__main__":
    audit_cmb_peaks()