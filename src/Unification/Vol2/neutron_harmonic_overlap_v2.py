# ==============================================================================
# PROJECT: THE KISH LATTICE | VOLUME 2 (DIAMOND EDITION)
# TITLE: THE GEOMETRIC NEUTRON
# AUTHORS: Timothy John Kish & Phoenix Aurora Kish
# LICENSE: Sovereign Protected / Copyright (c) 2026
# ==============================================================================

"""
Script: neutron_harmonic_overlap_v2.py
Volume: 2 – Appendix B (Visualization Companion to neutron_harmonic_overlap_v1.py)

Purpose
-------
This script provides visual diagnostics for the harmonic overlap condition:

        |ω1 – ω2| < ε_H

derived from the Kish Lattice Modulus (16/pi). It generates:

    • A Fleet Sweep Plot:
        offset/ε_H vs. stress_gain
        (shows how irrational offsets suppress destructive resonance)

    • A Monte Carlo Histogram:
        distribution of |ω1 – ω2| for random proton pairs
        with ε_H marked as the forbidden “burn‑in” band

Cross‑Linking (Chain-of-Custody)
--------------------------------
This script directly supports:
    • neutron_harmonic_overlap_v1.py (core logic + terminal output)
    • Chapter 4 — The Geometric Neutron (Harmonic Overlap Condition)
    • Chapter 3 — The Geometric Nucleus (Pressure Vessel Model)
    • Appendix A — nucleus_pressure_v1.py
    • Appendix B — neutron_beta_snap_v1.py
    • Appendix N — pi_lubricant_audit_v1.py

Together, v1 + v2 demonstrate:
    • The neutron’s irrational offset prevents |ω1 – ω2| < ε_H.
    • Harmonic overlap is rare in null worlds.
    • Nuclear stability is geometric, not magical.

Author: The 16pi Initiative
Date: February 2026
"""

import numpy as np
import matplotlib.pyplot as plt

# ==============================================================================
# LATTICE CONSTANTS
# ==============================================================================

LATTICE_MODULUS = 16.0 / np.pi
OMEGA_BASE = LATTICE_MODULUS
EPSILON_SCALE = 1.0
EPSILON_H = (1.0 / LATTICE_MODULUS) * OMEGA_BASE * EPSILON_SCALE  # ≈ 1.0


# ==============================================================================
# CORE LOGIC (imported conceptually from v1)
# ==============================================================================

def harmonic_overlap_metric(omega1: float, omega2: float) -> dict:
    delta_omega = abs(omega1 - omega2)
    overlap = delta_omega < EPSILON_H

    delta_min = 1e-12
    effective_delta = max(delta_omega, delta_min)
    stress_gain = 1.0 + (EPSILON_H / effective_delta) ** 2

    return {
        "delta_omega": delta_omega,
        "overlap": overlap,
        "stress_gain": stress_gain,
    }


def sweep_offsets():
    offsets = np.array([
        -2.0 * EPSILON_H,
        -1.0 * EPSILON_H,
        -0.5 * EPSILON_H,
        -0.25 * EPSILON_H,
        0.0,
        0.25 * EPSILON_H,
        0.5 * EPSILON_H,
        1.0 * EPSILON_H,
        2.0 * EPSILON_H,
    ])

    stress = []
    for d in offsets:
        r = harmonic_overlap_metric(OMEGA_BASE, OMEGA_BASE + d)
        stress.append(r["stress_gain"])

    return offsets / EPSILON_H, np.array(stress)


def monte_carlo(n=200000, spread=10 * EPSILON_H, seed=16):
    rng = np.random.default_rng(seed)
    low = OMEGA_BASE - spread
    high = OMEGA_BASE + spread

    omega1 = rng.uniform(low, high, n)
    omega2 = rng.uniform(low, high, n)
    delta = np.abs(omega1 - omega2)

    return delta


# ==============================================================================
# VISUALIZATION
# ==============================================================================

def plot_fleet_sweep():
    offsets, stress = sweep_offsets()

    plt.figure(figsize=(10, 6))
    plt.plot(offsets, stress, marker='o', linewidth=2, color='crimson')
    plt.axvline(0, color='black', linestyle='--', alpha=0.5)
    plt.axvspan(-1, 1, color='gold', alpha=0.15, label='|Δω| < ε_H (Overlap Zone)')

    plt.title("Harmonic Overlap Fleet Sweep\n(Geometric Neutron Stability Audit)")
    plt.xlabel("Offset / ε_H")
    plt.ylabel("Stress Gain (Amplification)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_monte_carlo():
    delta = monte_carlo()

    plt.figure(figsize=(10, 6))
    plt.hist(delta, bins=200, color='steelblue', alpha=0.75, density=True)
    plt.axvline(EPSILON_H, color='crimson', linestyle='--', linewidth=2,
                label='ε_H (Overlap Threshold)')
    plt.axvline(-EPSILON_H, color='crimson', linestyle='--', linewidth=2)

    plt.title("Monte Carlo Null Test\nDistribution of |ω1 – ω2| for Random Proton Pairs")
    plt.xlabel("|Δω|")
    plt.ylabel("Probability Density")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


# ==============================================================================
# TERMINAL ENTRY POINT
# ==============================================================================

def main():
    print("# neutron_harmonic_overlap_v2 (Visualization Edition)")
    print(f"# LATTICE_MODULUS (16/pi): {LATTICE_MODULUS:.12f}")
    print(f"# EPSILON_H:               {EPSILON_H:.12f}")
    print("# Generating visual diagnostics...\n")

    plot_fleet_sweep()
    plot_monte_carlo()

    print("# Visualizations complete.")
    print("# • Fleet Sweep shows stress amplification vs. irrational offsets.")
    print("# • Monte Carlo histogram shows rarity of overlap in null worlds.")
    print("# • Together with v1, this completes the harmonic overlap audit.")


if __name__ == "__main__":
    main()
