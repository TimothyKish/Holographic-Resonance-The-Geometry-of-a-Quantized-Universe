# vol5/S-Series/NS6_5_Unification/scripts/ratio_audit.py
import math

def run_ratio_audit():
    lattice = 16.0 / math.pi
    peak = 9.17
    
    ratio = peak / lattice
    
    print("===============================================================")
    print(" 🛡️ NS6_7: THE HARMONIC RATIO AUDIT")
    print("===============================================================")
    print(f"[+] Primary Lattice: {lattice:.5f}")
    print(f"[+] Observed Peak:   {peak:.5f}")
    print(f"[+] Ratio (Peak/L):  {ratio:.5f}")
    print("-" * 63)
    
    # Fundamental Geometric Ratios to check against:
    check_ratios = {
        "sqrt(2) [Diagonal]": math.sqrt(2),
        "sqrt(3) [Tetrahedral]": math.sqrt(3),
        "phi [Golden]": (1 + 5**0.5) / 2,
        "pi/2 [Orthogonal]": math.pi / 2,
        "9/5 [Thermal Shift]": 1.8
    }
    
    for name, val in check_ratios.items():
        diff = abs((ratio / val) - 1.0) * 100
        print(f"Comparison to {name.ljust(22)}: {diff:.2f}% Variance")

if __name__ == "__main__":
    run_ratio_audit()