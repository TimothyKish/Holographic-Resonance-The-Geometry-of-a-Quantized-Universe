# ==============================================================================
# SOVEREIGN COPYRIGHT (C) 2026 KISH LATTICE 16PI INITIATIVES LLC
# SCRIPT: uhc_lattice_gradient_sim.py
# TARGET: Ultra-High-Energy Cosmic Rays as Lattice Probes (Stiffness Gradient)
# PURPOSE:
#   Part 2 of the UHECR audit.
#   - Part 1 (uhc_lattice_probe_sim.py) shows that simple transit models
#     (Empty Void + Uniform 16/pi Lattice) cannot deliver Amaterasu/OMG energies.
#   - This script introduces a spatially varying lattice stiffness and a
#     low-drag "corridor" to model the Lattice Probe Effect.
# ==============================================================================

import numpy as np

def propagate_empty_void(E0, D, n_steps=1000):
    """
    Standard-model style toy propagation:
    - E loses energy via a simple exponential attenuation (GZK-like).
    - No geometric drag term, only distance-dependent loss.
    """
    x = np.linspace(0.0, D, n_steps)
    L_att = 1.0  # toy attenuation length (arbitrary units)
    E = E0 * np.exp(-x / L_att)
    return x, E

def propagate_uniform_lattice(E0, D, n_steps=1000, kish_stiffness=16.0/np.pi):
    """
    Kish Lattice propagation with uniform stiffness:
    - Same baseline attenuation as empty_void
    - PLUS a geometric drag term proportional to lattice stiffness
      and sqrt(E), integrated numerically.
    """
    x = np.linspace(0.0, D, n_steps)
    L_att = 1.0
    E = E0 * np.exp(-x / L_att)

    k_drag = 0.02  # global drag coefficient
    dx = D / (n_steps - 1)

    for i in range(1, n_steps):
        dE_drag = -k_drag * kish_stiffness * np.sqrt(max(E[i-1], 0.0)) * dx
        E[i] = max(E[i] + dE_drag, 0.0)

    return x, E

def lattice_stiffness_profile(x, D, kish_stiffness=16.0/np.pi):
    """
    Spatially varying stiffness profile:
    - Baseline stiffness = kish_stiffness
    - A central "corridor" region has reduced effective drag, modeling
      a phase-locked stiffness channel (the plucked web path).
    - Outside the corridor, drag is stronger (more turbulent lattice).
    """
    # Normalize position to [0, 1]
    u = x / D

    # Define corridor center and width in normalized coordinates
    corridor_center = 0.5
    corridor_width  = 0.2

    # Gaussian-like corridor: minimum drag at center, higher outside
    sigma = corridor_width / 2.0
    corridor_factor = np.exp(-0.5 * ((u - corridor_center) / sigma)**2)

    # Map corridor_factor (0..1) to an effective drag multiplier:
    # - At corridor center: drag_multiplier ~ 0.2 (low drag)
    # - Far from corridor: drag_multiplier ~ 1.0 (full drag)
    drag_min = 0.2
    drag_max = 1.0
    drag_multiplier = drag_min + (drag_max - drag_min) * (1.0 - corridor_factor)

    # Effective stiffness = kish_stiffness * drag_multiplier
    return kish_stiffness * drag_multiplier

def propagate_lattice_with_corridor(E0, D, n_steps=1000, kish_stiffness=16.0/np.pi):
    """
    Kish Lattice propagation with a stiffness gradient / corridor:
    - Same baseline attenuation as empty_void
    - PLUS a position-dependent geometric drag term.
    - The corridor reduces effective drag along a specific path, allowing
      higher arrival energies (Lattice Probe Effect).
    """
    x = np.linspace(0.0, D, n_steps)
    L_att = 1.0
    E = E0 * np.exp(-x / L_att)

    k_drag = 0.02  # base drag coefficient
    dx = D / (n_steps - 1)

    # Precompute stiffness profile along the path
    stiffness_profile = lattice_stiffness_profile(x, D, kish_stiffness=kish_stiffness)

    for i in range(1, n_steps):
        local_stiffness = stiffness_profile[i-1]
        dE_drag = -k_drag * local_stiffness * np.sqrt(max(E[i-1], 0.0)) * dx
        E[i] = max(E[i] + dE_drag, 0.0)

    return x, E, stiffness_profile

def run_uhc_lattice_gradient_audit():
    print("[*] INITIALIZING UHECR LATTICE GRADIENT AUDIT")

    # 1. Define a representative source energy (OMG / Amaterasu scale)
    E0_eev = 300.0  # 3e20 eV ~ 300 EeV
    D_void = 1.0    # arbitrary distance unit (normalized path length)

    # 2. Propagate in all three models
    x_empty,   E_empty   = propagate_empty_void(E0_eev, D_void)
    x_uniform, E_uniform = propagate_uniform_lattice(E0_eev, D_void)
    x_corr,    E_corr, stiffness_profile = propagate_lattice_with_corridor(E0_eev, D_void)

    # 3. Extract arrival energies
    E_arr_empty   = E_empty[-1]
    E_arr_uniform = E_uniform[-1]
    E_arr_corr    = E_corr[-1]

    print("\n=== UHECR ARRIVAL ENERGY COMPARISON (GRADIENT MODEL) ===")
    print(f"Initial Energy (Source):              {E0_eev:8.2f} EeV")
    print(f"Arrival (Empty Void Model):           {E_arr_empty:8.2f} EeV")
    print(f"Arrival (Uniform 16/pi Lattice):      {E_arr_uniform:8.2f} EeV")
    print(f"Arrival (16/pi Lattice + Corridor):   {E_arr_corr:8.2f} EeV")
    print("=========================================================")

    # 4. Threshold check (OMG / Amaterasu scale)
    threshold_omg = 240.0  # EeV
    print("\n=== THRESHOLD CHECK (OMG / AMATERASU SCALE) ===")
    print(f"Threshold: {threshold_omg:.1f} EeV")
    print(f"Empty Void Model:            {'PASS' if E_arr_empty   >= threshold_omg else 'FAIL'}")
    print(f"Uniform 16/pi Lattice:       {'PASS' if E_arr_uniform >= threshold_omg else 'FAIL'}")
    print(f"16/pi Lattice + Corridor:    {'PASS' if E_arr_corr    >= threshold_omg else 'FAIL'}")
    print("================================================")

    # 5. Optional: simple diagnostics on stiffness profile
    print("\n=== STIFFNESS PROFILE DIAGNOSTIC ===")
    print(f"Min effective stiffness: {stiffness_profile.min():.4f}")
    print(f"Max effective stiffness: {stiffness_profile.max():.4f}")
    print("====================================")

if __name__ == '__main__':
    run_uhc_lattice_gradient_audit()
