import json
import random
import math
import os

# 🛡️ NS6_32: THE NULL SCALING DIAGNOSTIC
# -----------------------------------------------------------
def test_scaling():
    L = 16.0 / math.pi
    ANCHOR = 6.6069e10
    floors = [70, 100, 150, 200]
    total_n = 268000
    
    print("📐 INITIATING NULL SCALING TEST...")
    print(f"Testing Chi-Squared response to Vdisp floors: {floors}\n")

    for floor in floors:
        bins = {i: 0 for i in range(10)}
        for _ in range(total_n):
            v = random.uniform(floor, 500.0) # Random above the floor
            m = random.uniform(13.0, 22.0)   # SDSS mag range
            
            lum = 10**((25 - m) / 2.5)
            ks = ((v**4) / lum) / ANCHOR
            phi = math.log(ks) % L
            bin_idx = min(int((phi / L) * 10), 9)
            bins[bin_idx] += 1
            
        expected = total_n / 10.0
        chi2 = sum([((bins[i] - expected)**2) / expected for i in range(10)])
        print(f"Floor > {floor:3} km/s | Chi-Squared (X²): {chi2:8.2f}")

if __name__ == "__main__":
    test_scaling()
    input("\nPress ENTER to close...")