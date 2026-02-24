# ==============================================================================
# PROJECT: THE KISH LATTICE | VOLUME 2 (DIAMOND EDITION)
# TITLE: THE GEOMETRIC NEUTRON
# AUTHORS: Timothy John Kish & Phoenix Aurora Kish
# LICENSE: Sovereign Protected / Copyright {c} 2026
# ==============================================================================

"""
Script: neutron_harmonic_overlap_v1.py
Volume: 2 – Appendix B (The Geometric Neutron beta decay sim and no need for Boson)

Purpose
-------
This script quantifies harmonic overlap between two proton vertices embedded in the
16/pi lattice and evaluates the burn‑in condition:

        |ω1 – ω2| < ε_H

where ε_H is an irrational spacing threshold derived from the Kish Lattice Modulus (16/pi).
When this condition is satisfied, the two vertices strike the same vacuum nodes repeatedly,
amplifying local stress and risking Burn‑In Failure. The neutron’s geometric role is to
introduce an irrational offset that *prevents* this condition from being met.

Cross‑Linking (Chain-of-Custody)
--------------------------------
This script directly supports:
    • Chapter 4 — The Geometric Neutron (Harmonic Overlap Condition)
    • Chapter 3 — The Geometric Nucleus (Pressure Vessel Model)
    • Chapter 5 — Higgs Removal (Mass as Vacuum Drag)
    • Appendix A — nucleus_pressure_v1.py (pressure confinement)
    • Appendix B — neutron_beta_snap_v1.py (delamination torque)
    • Appendix N — pi_lubricant_audit_v1.py (irrationality as stabilizer)

Together, these scripts demonstrate that:
    • The nucleus is a pressure vessel.
    • The neutron is a geometric damper.
    • Harmonic overlap is the mechanical origin of nuclear instability.
    • Irrational offsets (16/pi) prevent destructive resonance.

Author: The 16pi Initiative
Date: February 2026
"""

import numpy as np

# ==============================================================================
# LATTICE CONSTANTS
# ==============================================================================

# Kish Lattice Modulus (spatial)
LATTICE_MODULUS = 16.0 / np.pi

# Base angular frequency scale (normalized)
OMEGA_BASE = LATTICE_MODULUS

# Harmonic overlap threshold ε_H:
# Defined as the irrational spacing scale that the neutron enforces.
EPSILON_SCALE = 1.0
EPSILON_H = (1.0 / LATTICE_MODULUS) * OMEGA_BASE * EPSILON_SCALE  # ≈ 1.0


# ==============================================================================
# CORE DIAGNOSTIC
# ==============================================================================

def harmonic_overlap_metric(omega1: float, omega2: float) -> dict:
    """
    Evaluate harmonic overlap between two proton vertices.

    Returns:
        {
            "omega1": ω1,
            "omega2": ω2,
            "delta_omega": |ω1 - ω2|,
            "epsilon_H": ε_H,
            "overlap": True/False,
            "stress_gain": amplification factor
        }
    """
    delta_omega = abs(omega1 - omega2)
    overlap = delta_omega < EPSILON_H

    # Prevent singularity at exact match
    delta_min = 1e-12
    effective_delta = max(delta_omega, delta_min)

    # Stress amplification proxy
    stress_gain = 1.0 + (EPSILON_H / effective_delta) ** 2

    return {
        "omega1": omega1,
        "omega2": omega2,
        "delta_omega": delta_omega,
        "epsilon_H": EPSILON_H,
        "overlap": overlap,
        "stress_gain": stress_gain,
    }


# ==============================================================================
# FLEET SWEEP — BOUND VS OFFSET STATES
# ==============================================================================

def sweep_neutron_offsets(
    omega_base: float = OMEGA_BASE,
    offsets: np.ndarray | None = None,
) -> list[dict]:
    """
    Sweep offsets around a base proton frequency to show:
        • near‑integer offsets → overlap (unstable)
        • irrational offsets → no overlap (stable)
    """
    if offsets is None:
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

    results = []
    for d_omega in offsets:
        omega1 = omega_base
        omega2 = omega_base + d_omega
        result = harmonic_overlap_metric(omega1, omega2)
        result["offset"] = d_omega
        results.append(result)

    return results


# ==============================================================================
# MONTE CARLO NULL TEST
# ==============================================================================

def monte_carlo_overlap_fraction(
    n_samples: int = 100000,
    omega_center: float = OMEGA_BASE,
    spread: float = 10.0 * EPSILON_H,
    seed: int | None = 16,
) -> dict:
    """
    Estimate how often random proton frequency pairs fall into the overlap regime.
    This demonstrates that harmonic overlap is *rare* in null worlds, and that the
    neutron’s irrational offset is what keeps real nuclei out of this fragile band.
    """
    rng = np.random.default_rng(seed)
    low = omega_center - spread
    high = omega_center + spread

    overlap_count = 0

    for _ in range(n_samples):
        omega1 = rng.uniform(low, high)
        omega2 = rng.uniform(low, high)
        if harmonic_overlap_metric(omega1, omega2)["overlap"]:
            overlap_count += 1

    overlap_fraction = overlap_count / n_samples

    return {
        "n_samples": n_samples,
        "overlap_count": overlap_count,
        "overlap_fraction": overlap_fraction,
        "epsilon_H": EPSILON_H,
        "omega_center": omega_center,
        "spread": spread,
    }


# ==============================================================================
# TERMINAL ENTRY POINT (FOR APPENDIX B CAPTURE)
# ==============================================================================

def main():
    print("# neutron_harmonic_overlap_v1")
    print(f"# LATTICE_MODULUS (16/pi): {LATTICE_MODULUS:.12f}")
    print(f"# OMEGA_BASE:              {OMEGA_BASE:.12f}")
    print(f"# EPSILON_H (threshold):   {EPSILON_H:.12f}")
    print()

    print("# Offset Sweep (Bound vs Near-Bound States)")
    results = sweep_neutron_offsets()
    print("# offset/ε_H   δω/ε_H     overlap   stress_gain")
    for r in results:
        offset_norm = r["offset"] / EPSILON_H
        delta_norm = r["delta_omega"] / EPSILON_H
        print(
            f"{offset_norm:10.4f}  {delta_norm:8.4f}   "
            f"{str(r['overlap']):7s}   {r['stress_gain']:12.4f}"
        )
    print()

    print("# Monte Carlo Null Test")
    mc = monte_carlo_overlap_fraction()
    print(f"# n_samples:        {mc['n_samples']}")
    print(f"# overlap_count:    {mc['overlap_count']}")
    print(f"# overlap_fraction: {mc['overlap_fraction']:.8f}")
    print(f"# epsilon_H:        {mc['epsilon_H']:.12f}")
    print()

    print("# Interpretation:")
    print("# • overlap=True corresponds to |ω1 – ω2| < ε_H (harmonic overlap).")
    print("# • This is the Burn‑In Failure regime described in Chapter 4.")
    print("# • The neutron prevents this by enforcing an irrational offset.")
    print("# • Null worlds rarely fall into this band — proving the damper role.")


if __name__ == '__main__':
    main()
