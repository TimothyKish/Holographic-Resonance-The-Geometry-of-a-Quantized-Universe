# -----------------------------------------------------------------------------
# HOLOGRAPHIC RESONANCE THEORY - GALACTIC ROTATION VALIDATION
# Author: Timothy John Kish
# Repository: https://github.com/TimothyKish/Holographic-Resonance-The-Geometry-of-a-Quantized-Universe
# License: MIT License
#
# DESCRIPTION:
# This script compares Standard Newtonian Dynamics against the Kish Vacuum Viscosity
# model for Galaxy NGC 6503. It demonstrates that the flat rotation curve can be
# derived from the geometric stiffness of the vacuum (16/pi) without Dark Matter.
#
# CITATIONS (Zenodo):
# Vol 1 (Geometry): https://doi.org/10.5281/zenodo.18209531
# Vol 2 (Dynamics): https://doi.org/10.5281/zenodo.18217120
# Vol 3 (Matter):   https://doi.org/10.5281/zenodo.18217227
# -----------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt

# --- 1. DEFINE CONSTANTS ---
G = 6.674e-11          # Gravitational Constant (m^3 kg^-1 s^-2)
c = 2.9979e8           # Speed of Light (m/s)
H0 = 2.2e-18           # Hubble Constant (approx 67 km/s/Mpc in s^-1)
k_geo = 16 / np.pi     # The Kish Geometric Constant (approx 5.09)

# --- 2. CALCULATE KISH ACCELERATION (Vacuum Viscosity Threshold) ---
# Formula: a_kish = (c * H0) / k_geo
# This represents the minimum acceleration the vacuum lattice can support before
# viscosity (drag) dominates.
a_kish = (c * H0) / k_geo

print(f"--- KISH LATTICE PARAMETERS ---")
print(f"Geometric Constant (k_geo):      {k_geo:.4f}")
print(f"Vacuum Viscosity Limit (a_kish): {a_kish:.3e} m/s^2")
print(f"Milgrom's Constant (Observed):   1.200e-10 m/s^2")
print(f"Match Accuracy:                  {100 * (1 - abs(a_kish - 1.2e-10)/1.2e-10):.2f}%")
print("-" * 40)

# --- 3. GALAXY PARAMETERS (NGC 6503) ---
# Approximate Baryonic Mass (Stars + Gas) based on luminosity
mass_galaxy_solar = 4.8e9  # Solar masses
mass_galaxy_kg = mass_galaxy_solar * 1.989e30

# Radial range (0.1 to 20 kpc)
# 1 kpc = 3.086e19 meters
radii_kpc = np.linspace(0.1, 20, 100)
radii_m = radii_kpc * 3.086e19

# --- 4. COMPUTE VELOCITY CURVES ---

# A. Newtonian Velocity (Standard Physics - No Dark Matter)
# v = sqrt(GM/r)
# This curve drops off as 1/sqrt(r), failing to match observation.
v_newton = np.sqrt((G * mass_galaxy_kg) / radii_m)

# B. Kish Viscosity Velocity (Holographic Resonance Theory)
# The "Vacuum Grip" takes over when acceleration drops below a_kish.
# Interpolation Function: a_eff = sqrt(a_N^2 + a_N * a_kish)
# Velocity: v = sqrt(r * a_eff)

a_newton_array = (G * mass_galaxy_kg) / (radii_m**2)
a_eff = np.sqrt(a_newton_array**2 + a_newton_array * a_kish)
v_kish = np.sqrt(radii_m * a_eff)

# Convert to km/s for plotting
v_newton_km = v_newton / 1000
v_kish_km = v_kish / 1000

# --- 5. PLOTTING ---
plt.figure(figsize=(10, 6))

# Plot Standard Newton
plt.plot(radii_kpc, v_newton_km, linestyle='--', color='gray', alpha=0.7, label='Standard Newtonian (Mass only)')

# Plot Kish Model
plt.plot(radii_kpc, v_kish_km, linewidth=3, color='blue', label='Kish Vacuum Viscosity (Predicted)')

# Add "Observed" flat line approximation for NGC 6503 (approx 120 km/s)
plt.axhline(y=120, color='red', linestyle=':', alpha=0.6, label='Observed Data (Approx)')

plt.title(f"Galactic Rotation Curve: NGC 6503\nStandard Model vs. Kish Lattice (No Dark Matter)")
plt.xlabel("Distance from Center (kpc)")
plt.ylabel("Orbital Velocity (km/s)")
plt.legend()
plt.grid(True, alpha=0.3)

# Annotation explaining the mechanism
plt.text(10, 50, f"Vacuum Grip (a_kish) = {a_kish:.2e}\nDerived from 16/pi", fontsize=10,
         bbox=dict(facecolor='white', alpha=0.8, edgecolor='blue'))

plt.tight_layout()
plt.show()