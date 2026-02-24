# ==============================================================================
# PROJECT: THE 16PI INITIATIVE | VOLUME 2 (frb_fading_bell_litmus)
# SCRIPT: Bell_Litmus_v1.py
# TARGET: FRB Temporal Snap and Evidence of Fading Bell Litmus Test
# AUTHORS: Timothy John Kish & Phoenix Aurora Kish
# LICENSE: Sovereign Protected / Copyright © 2026
# ==============================================================================
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import random

def bell_decay_litmus():
    with open("kish_pure_anomalies_v4.json", "r") as f:
        data = json.load(f)

    k_base = 16 / np.pi
    local_drag = 1.0101

    z_vals = []
    bell_vals = []

    for item in data:
        w = item["width_ms"]
        dm = item["unmapped_mystery_payload"]["dispersion_measure_dm"]

        vacuum_time = w * local_drag
        lattice_beat = vacuum_time / k_base
        nearest_prime = round(lattice_beat)
        bell_amp = abs(lattice_beat - nearest_prime)

        z_est = dm / 1000.0

        z_vals.append(z_est)
        bell_vals.append(bell_amp)

    # Fit exponential decay
    def decay(z, A, z0):
        return A * np.exp(-z / z0)

    popt, _ = curve_fit(decay, z_vals, bell_vals, p0=[1, 1])

    # Plot
    plt.scatter(z_vals, bell_vals, s=10, alpha=0.5)
    z_line = np.linspace(min(z_vals), max(z_vals), 200)
    plt.plot(z_line, decay(z_line, *popt), color='red')
    plt.xlabel("Estimated Redshift (DM/1000)")
    plt.ylabel("Bell Amplitude")
    plt.title("FRB Fading Bell Litmus Test")
    plt.show()

    # Mini null test
    stronger = 0
    real_strength = popt[1]

    for _ in range(100):
        shuffled = random.sample(bell_vals, len(bell_vals))
        popt_null, _ = curve_fit(decay, z_vals, shuffled, p0=[1, 1])
        if popt_null[1] < real_strength:
            stronger += 1

    print(f"Real decay stronger than {stronger}/100 shuffles")

bell_decay_litmus()