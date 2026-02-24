# ==============================================================================
# PROJECT: THE KISH LATTICE | VOLUME 2 (DIAMOND EDITION)
# TITLE: THE GEOMETRIC NEUTRON — NULL GEOMETRY FLEET
# AUTHORS: Timothy John Kish & Phoenix Aurora Kish
# LICENSE: Sovereign Protected / Copyright © 2026
# ==============================================================================

"""
Script: bond_angle_null_test_v2.py
Volume: 2 – Appendix C (Visualization Companion to bond_angle_null_test_v1.py)

Purpose
-------
Visualization suite for the null bond‑angle audit:

    • Plot 1: Bond angle vs. drag_factor
              (stability basin around the tetrahedral angle)

    • Plot 2: Categorical bar chart
              (stable vs. unstable vs. null geometry)

Both plots are saved as PNG files in the script directory for Appendix integration.

Cross‑Linking (Chain-of-Custody)
--------------------------------
This script directly supports:
    • bond_angle_null_test_v1.py      (core logic + terminal output)
    • h2o_bond_angle_audit_v1.py      (H2O derivation)
    • Chapter 6 — The Geometric Bond
    • Chapter 4 — The Geometric Neutron
    • Appendix N — pi_lubricant_audit_v1.py

Together, v1 + v2 demonstrate:
    • Real bond angles occupy a low‑drag basin.
    • Fake/null angles produce high drag or collapse.
    • Chemistry is a geometric consequence of the 16/pi lattice.

Author: The 16pi Initiative
Date: February 2026
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# ==============================================================================
# LATTICE CONSTANTS (must match v1)
# ==============================================================================

LATTICE_MODULUS = 16.0 / np.pi
IDEAL_ANGLE = 109.4712206  # degrees
ANGLE_TOLERANCE = 4.0      # degrees


# ==============================================================================
# CORE METRIC (mirrors v1)
# ==============================================================================

def bond_angle_stability(angle_deg: float) -> dict:
    delta = abs(angle_deg - IDEAL_ANGLE)
    drag_factor = 1.0 + (delta / ANGLE_TOLERANCE) ** 2
    stable = delta <= ANGLE_TOLERANCE
    null_geometry = angle_deg < 60 or angle_deg > 180

    return {
        "angle": angle_deg,
        "delta": delta,
        "drag_factor": drag_factor,
        "stable": stable,
        "null_geometry": null_geometry,
    }


def sweep_angles_dense():
    angles = np.linspace(0, 210, 1000)
    drag = []
    null_mask = []

    for a in angles:
        r = bond_angle_stability(a)
        drag.append(r["drag_factor"])
        null_mask.append(r["null_geometry"])

    return angles, np.array(drag), np.array(null_mask)


def sweep_angles_discrete():
    test_angles = [
        104.5,   # H2O
        109.47,  # Ideal tetrahedral
        120.0,   # Trigonal planar
        90.0,    # Square planar
        60.0,    # Edge of viability
        45.0,    # Null
        30.0,    # Null
        10.0,    # Null
        200.0,   # Impossible
    ]

    return [bond_angle_stability(a) for a in test_angles]


# ==============================================================================
# VISUALIZATION (with PNG export)
# ==============================================================================

def plot_drag_landscape(save_path="bond_angle_drag_landscape.png"):
    angles, drag, null_mask = sweep_angles_dense()

    plt.figure(figsize=(10, 6))
    plt.plot(angles, drag, color="steelblue", linewidth=2, label="Drag factor")

    plt.axvspan(0, 60, color="lightcoral", alpha=0.2, label="Null geometry")
    plt.axvspan(180, 210, color="lightcoral", alpha=0.2)

    plt.axvline(IDEAL_ANGLE, color="green", linestyle="--", linewidth=2,
                label="Ideal tetrahedral angle")
    plt.axvspan(IDEAL_ANGLE - ANGLE_TOLERANCE,
                IDEAL_ANGLE + ANGLE_TOLERANCE,
                color="gold", alpha=0.2, label="Stability basin")

    plt.title("Null Bond‑Angle Audit\nDrag Landscape in the 16/pi Lattice")
    plt.xlabel("Bond angle (degrees)")
    plt.ylabel("Drag factor (relative)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(save_path, dpi=300)
    plt.close()


def plot_categorical_bars(save_path="bond_angle_categorical_bars.png"):
    results = sweep_angles_discrete()

    labels = [f"{r['angle']:.1f}°" for r in results]
    drag = [r["drag_factor"] for r in results]

    colors = []
    for r in results:
        if r["null_geometry"]:
            colors.append("firebrick")
        elif r["stable"]:
            colors.append("seagreen")
        else:
            colors.append("darkorange")

    plt.figure(figsize=(10, 6))
    x = np.arange(len(labels))
    plt.bar(x, drag, color=colors)
    plt.xticks(x, labels, rotation=45, ha="right")

    plt.title("Representative Bond Angles\nStable vs. Unstable vs. Null Geometry")
    plt.ylabel("Drag factor (relative)")
    plt.grid(True, axis="y", alpha=0.3)

    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color="seagreen"),
        plt.Rectangle((0, 0), 1, 1, color="darkorange"),
        plt.Rectangle((0, 0), 1, 1, color="firebrick"),
    ]
    plt.legend(legend_handles,
               ["Stable (low drag)", "Unstable (high drag)", "Null geometry"],
               loc="upper left")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()


# ==============================================================================
# TERMINAL ENTRY POINT
# ==============================================================================

def main():
    print("# bond_angle_null_test_v2 (Visualization Edition)")
    print(f"# LATTICE_MODULUS (16/pi): {LATTICE_MODULUS:.12f}")
    print(f"# IDEAL_ANGLE:             {IDEAL_ANGLE:.6f}°")
    print(f"# ANGLE_TOLERANCE:         ±{ANGLE_TOLERANCE:.2f}°")
    print("# Saving visual diagnostics...\n")

    plot_drag_landscape()
    plot_categorical_bars()

    print("# PNG files saved:")
    print("#  • bond_angle_drag_landscape.png")
    print("#  • bond_angle_categorical_bars.png")
    print("# Visualization suite complete.")


if __name__ == "__main__":
    main()
