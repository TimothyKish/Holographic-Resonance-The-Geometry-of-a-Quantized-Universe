import numpy as np
from scipy.stats import chisquare
import math

def run_correct_ghost_audit():
    print("🛡️  CORRECT GHOST AUDIT — BOTH VARIABLES VARYING (REFEREE PROTOCOL)")
    
    L_target = 16.0 / math.pi
    ANCHOR = 6.6069e10
    N = 500000 
    
    # 1. GENERATE BOTH VARIABLES (MATCHING SDSS DISTRIBUTIONS)
    # Velocity dispersion: lognormal, mean ~180-200 km/s
    velDisp = np.random.lognormal(mean=5.2, sigma=0.35, size=N)
    
    # Magnitude: Normal distribution r-band ~17.0
    mag = np.random.normal(17.0, 1.5, size=N)
    mag = np.clip(mag, 13.0, 22.0) 
    
    # 2. APPLY THE FULL FABER-JACKSON TRANSFORM
    lum = 10**((25 - mag) / 2.5)
    val = (velDisp**4 / lum) / ANCHOR
    
    # 3. THE LOG-MODULO TEST (THE REAL AUDIT)
    phi = np.log(val) % L_target
    observed, _ = np.histogram(phi, bins=10, range=(0, L_target))
    expected = np.full(10, N / 10.0)
    chi2, p = chisquare(f_obs=observed, f_exp=expected)
    
    print("\n" + "="*50)
    print(f"📊 CORRECTED GHOST OUTPUT (VARYING MAG)")
    print("="*50)
    print(f"N = {N:,}")
    print(f"Chi-squared (χ²) = {chi2:.4f}")
    print(f"P-Value          = {p:.4e}")
    print("-" * 50)
    
    # 4. L-SWEEP ON CORRECT GHOST
    print("\nL-sweep on Corrected Ghost:")
    print(f"{'L':<8} {'Chi2':>10} {'Peak %':>10}")
    print("-"*35)
    
    for L_test in [4.0, 4.5, 5.093, 5.5, 6.0, 6.5]:
        phi_t = np.log(val) % L_test
        obs_t, _ = np.histogram(phi_t, bins=10, range=(0, L_test))
        peak_pct = (np.max(obs_t) / N) * 100
        c2, _ = chisquare(f_obs=obs_t, f_exp=np.full(10, N/10.0))
        marker = " ← TARGET" if abs(L_test - 5.093) < 0.01 else ""
        print(f"{L_test:<8.3f} {c2:>10.2f} {peak_pct:>9.2f}%{marker}")

    print("\n" + "="*50)
    print("VERDICT:")
    if chi2 < 100:
        print(f"✅ STATUS: METHODOLOGY SOUND (χ²={chi2:.2f})")
        print("   The artifact was caused by the fixed-magnitude flaw.")
        print("   Real SDSS peaks are almost certainly PHYSICAL.")
    elif chi2 > 1000:
        print(f"🚨 STATUS: ARTIFACT CONFIRMED (χ²={chi2:.2f})")
        print("   Even with varying magnitude, the math creates a ghost.")
    else:
        print(f"⚠️  STATUS: AMBIGUOUS (χ²={chi2:.2f})")
    print("="*50)

if __name__ == "__main__":
    run_correct_ghost_audit()