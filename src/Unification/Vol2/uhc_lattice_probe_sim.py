# ==============================================================================
# SOVEREIGN COPYRIGHT (C) 2026 KISH LATTICE 16PI INITIATIVES LLC
# SCRIPT: uhc_lattice_probe_sim.py
# TARGET: Ultra-High-Energy Cosmic Rays as Lattice Probes (OMG / Amaterasu Class)
# ==============================================================================

import numpy as np

def propagate_empty_void(E0, D, n_steps=1000):
    """
    Standard-model style toy propagation:
    - E loses energy via a simple exponential attenuation (GZK-like).
    - No geometric drag term, only distance-dependent loss.
    """
    x = np.linspace(0.0, D, n_steps)
    # Toy attenuation length (in arbitrary units)
    L_att = 1.0
    E = E0 * np.exp(-x / L_att)
    return x, E

def propagate_lattice_void(E0, D, n_steps=1000, kish_stiffness=16.0/np.pi):
    """
    Kish Lattice propagation:
    - Same baseline attenuation as empty_void
    - PLUS a geometric drag term proportional to lattice stiffness
      and an effective cross-section (here absorbed into a coefficient).
    """
    x = np.linspace(0.0, D, n_steps)
    L_att = 1.0
    # Base exponential loss
    E = E0 * np.exp(-x / L_att)

    # Geometric drag term: dE/dx ~ -k * kish_stiffness * sqrt(E)
    # Integrated numerically as a small correction per step.
    k_drag = 0.02  # tunable coefficient for “how stiff” the path is
    dx = D / (n_steps - 1)

    for i in range(1, n_steps):
        dE_drag = -k_drag * kish_stiffness * np.sqrt(max(E[i-1], 0.0)) * dx
        E[i] = max(E[i] + dE_drag, 0.0)

    return x, E

def run_uhc_lattice_probe_audit():
    print("[*] INITIALIZING UHECR LATTICE PROBE AUDIT")

    # 1. Define a representative source energy (OMG / Amaterasu scale)
    E0_eev = 300.0  # 3e20 eV ~ 300 EeV (Oh-My-God scale)
    D_void = 1.0    # arbitrary distance unit (e.g., normalized to GZK scale)

    # 2. Propagate in both models
    x_empty, E_empty = propagate_empty_void(E0_eev, D_void)
    x_lattice, E_lattice = propagate_lattice_void(E0_eev, D_void)

    # 3. Extract “arrival energies” at Earth (end of path)
    E_arr_empty = E_empty[-1]
    E_arr_lattice = E_lattice[-1]

    print("\n=== UHECR ARRIVAL ENERGY COMPARISON ===")
    print(f"Initial Energy (Source):      {E0_eev:8.2f} EeV")
    print(f"Arrival (Empty Void Model):   {E_arr_empty:8.2f} EeV")
    print(f"Arrival (16/pi Lattice Model):{E_arr_lattice:8.2f} EeV")
    print("========================================")

    # 4. Simple diagnostic: can either model reach Amaterasu/OMG energies?
    threshold_omg = 240.0  # EeV (Amaterasu / OMG scale)
    print("\n=== THRESHOLD CHECK (OMG / AMATERASU SCALE) ===")
    print(f"Threshold: {threshold_omg:.1f} EeV")
    print(f"Empty Void Model:   {'PASS' if E_arr_empty >= threshold_omg else 'FAIL'}")
    print(f"16/pi Lattice Model:{'PASS' if E_arr_lattice >= threshold_omg else 'FAIL'}")
    print("================================================")

if __name__ == '__main__':
    run_uhc_lattice_probe_audit()
