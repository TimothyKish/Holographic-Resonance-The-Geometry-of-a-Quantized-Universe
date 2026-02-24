# ==============================================================================
# SOVEREIGN COPYRIGHT (C) 2026 KISH LATTICE 16PI INITIATIVES LLC
# SCRIPT: uhc_lattice_gradient_v2_corridor_deep.py
# TARGET: UHECR Lattice Probe – Stiffness Gradient (v2: Deeper Corridor)
#
# VERSION NOTES:
#   v1 (uhc_lattice_gradient_sim.py):
#       - Introduced a spatial stiffness gradient + corridor.
#       - Result: Empty, Uniform Lattice, and Corridor all arrived at ~110.36 EeV.
#       - Conclusion: The initial corridor profile did not produce any advantage.
#
#   v2 (this script):
#       - Corridor is made NARROWER and DEEPER (lower effective drag).
#       - Global drag coefficient is slightly reduced to expose corridor contrast.
#       - All changes are documented below; no hidden parameters.
# ==============================================================================

import numpy as np

# -----------------------------
# GLOBAL PARAMETERS (DOCUMENTED)
# -----------------------------
E0_EEV          = 300.0       # Source energy (EeV), OMG / Amaterasu scale
D_VOID          = 1.0         # Normalized path length
N_STEPS         = 2000        # Integration resolution

L_ATTENUATION   = 1.0         # Baseline exponential attenuation length (toy GZK)
KISH_STIFFNESS  = 16.0 / np.pi

# Drag parameters:
K_DRAG_UNIFORM  = 0.015       # Slightly reduced from 0.02 (v1) for clarity
K_DRAG_CORRIDOR = 0.015       # Same base coefficient; corridor modifies via profile

# Corridor geometry:
CORRIDOR_CENTER = 0.5         # Center of corridor (normalized position)
CORRIDOR_WIDTH  = 0.10        # Narrower than v1 (0.20) – more focused channel
DRAG_MIN        = 0.05        # Deeper corridor: minimum drag multiplier (v1 used 0.2)
DRAG_MAX        = 1.00        # Full drag outside corridor


def propagate_empty_void(E0, D, n_steps=N_STEPS):
    """
    Standard-model style toy propagation:
    - Pure exponential attenuation with distance.
    - No geometric drag term.
    """
    x = np.linspace(0.0, D, n_steps)
    E = E0 * np.exp(-x / L_ATTENUATION)
    return x, E


def propagate_uniform_lattice(E0, D, n_steps=N_STEPS, kish_stiffness=KISH_STIFFNESS):
    """
    Kish Lattice propagation with UNIFORM stiffness:
    - Baseline exponential attenuation.
    - PLUS geometric drag term proportional to sqrt(E) and lattice stiffness.
    """
    x = np.linspace(0.0, D, n_steps)
    E = E0 * np.exp(-x / L_ATTENUATION)

    dx = D / (n_steps - 1)

    for i in range(1, n_steps):
        dE_drag = -K_DRAG_UNIFORM * kish_stiffness * np.sqrt(max(E[i-1], 0.0)) * dx
        E[i] = max(E[i] + dE_drag, 0.0)

    return x, E


def lattice_stiffness_profile_v2(x, D, kish_stiffness=KISH_STIFFNESS):
    """
    v2 stiffness profile:
    - Same conceptual structure as v1 (Gaussian corridor),
      but with:
        * narrower width (CORRIDOR_WIDTH = 0.10),
        * deeper drag reduction (DRAG_MIN = 0.05).
    - This models a more sharply defined, low-drag lattice corridor.
    """
    u = x / D  # normalize to [0, 1]

    sigma = CORRIDOR_WIDTH / 2.0
    corridor_factor = np.exp(-0.5 * ((u - CORRIDOR_CENTER) / sigma) ** 2)

    # Map corridor_factor (0..1) to drag multiplier:
    #   at corridor center: drag_multiplier ~ DRAG_MIN
    #   far from corridor: drag_multiplier ~ DRAG_MAX
    drag_multiplier = DRAG_MIN + (DRAG_MAX - DRAG_MIN) * (1.0 - corridor_factor)

    return kish_stiffness * drag_multiplier


def propagate_lattice_with_corridor_v2(E0, D, n_steps=N_STEPS, kish_stiffness=KISH_STIFFNESS):
    """
    Kish Lattice propagation with v2 stiffness corridor:
    - Baseline exponential attenuation.
    - PLUS position-dependent geometric drag term using v2 profile.
    """
    x = np.linspace(0.0, D, n_steps)
    E = E0 * np.exp(-x / L_ATTENUATION)

    dx = D / (n_steps - 1)
    stiffness_profile = lattice_stiffness_profile_v2(x, D, kish_stiffness=kish_stiffness)

    for i in range(1, n_steps):
        local_stiffness = stiffness_profile[i-1]
        dE_drag = -K_DRAG_CORRIDOR * local_stiffness * np.sqrt(max(E[i-1], 0.0)) * dx
        E[i] = max(E[i] + dE_drag, 0.0)

    return x, E, stiffness_profile


def run_uhc_lattice_gradient_v2_audit():
    print("[*] INITIALIZING UHECR LATTICE GRADIENT AUDIT (v2: DEEP CORRIDOR)")

    # 1. Propagate in all three models
    x_empty,   E_empty   = propagate_empty_void(E0_EEV, D_VOID)
    x_uniform, E_uniform = propagate_uniform_lattice(E0_EEV, D_VOID)
    x_corr,    E_corr, stiffness_profile = propagate_lattice_with_corridor_v2(E0_EEV, D_VOID)

    # 2. Extract arrival energies
    E_arr_empty   = E_empty[-1]
    E_arr_uniform = E_uniform[-1]
    E_arr_corr    = E_corr[-1]

    print("\n=== UHECR ARRIVAL ENERGY COMPARISON (GRADIENT MODEL v2) ===")
    print(f"Initial Energy (Source):                {E0_EEV:8.2f} EeV")
    print(f"Arrival (Empty Void Model):             {E_arr_empty:8.2f} EeV")
    print(f"Arrival (Uniform 16/pi Lattice):        {E_arr_uniform:8.2f} EeV")
    print(f"Arrival (16/pi Lattice + Deep Corridor):{E_arr_corr:8.2f} EeV")
    print("============================================================")

    # 3. Threshold check (OMG / Amaterasu scale)
    threshold_omg = 240.0  # EeV
    print("\n=== THRESHOLD CHECK (OMG / AMATERASU SCALE) ===")
    print(f"Threshold: {threshold_omg:.1f} EeV")
    print(f"Empty Void Model:                 {'PASS' if E_arr_empty   >= threshold_omg else 'FAIL'}")
    print(f"Uniform 16/pi Lattice:            {'PASS' if E_arr_uniform >= threshold_omg else 'FAIL'}")
    print(f"16/pi Lattice + Deep Corridor:    {'PASS' if E_arr_corr    >= threshold_omg else 'FAIL'}")
    print("================================================")

    # 4. Stiffness diagnostics
    print("\n=== STIFFNESS PROFILE DIAGNOSTIC (v2) ===")
    print(f"Min effective stiffness: {stiffness_profile.min():.4f}")
    print(f"Max effective stiffness: {stiffness_profile.max():.4f}")
    print("==========================================")


if __name__ == '__main__':
    run_uhc_lattice_gradient_v2_audit()