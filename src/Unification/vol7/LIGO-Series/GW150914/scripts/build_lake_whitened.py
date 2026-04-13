# ==============================================================================
# SCRIPT: build_lake_whitened.py
# SERIES: LIGO-Series / GW150914
# PURPOSE: Whitened strain PSD analysis of GW150914 for ghost note frequencies
#          5.093 Hz (k_geo = 16/π) and 16.0 Hz (k_geo × π = 16)
#
# LAKE NAMING CONVENTION:
#   gw150914_ghost_notes_raw.json      — RAW strain (null baseline, already built)
#   gw150914_ghost_notes_whitened.json — WHITENED strain (this script)
#
# WHY WHITENED:
#   Raw LIGO strain below ~10 Hz is buried under a steeply rising seismic
#   noise wall. The 5.093 Hz frequency sits in a trough of that wall and
#   appears depressed in raw PSD regardless of any astrophysical content.
#
#   Whitening divides the strain by its noise amplitude spectral density,
#   flattening the noise floor so that coherent signals stand out above it.
#   This is the standard LIGO processing and is the data layer where
#   sub-threshold features — ghost notes — would be visible.
#
#   This is the layer Lyra Aurora Kish was analyzing on January 8, 2026
#   when she observed anomalous features at 5.13 Hz and 16.12 Hz in
#   the GW150914 ringdown data.
#
# PROTOCOL:
#   1. Download raw strain (same as raw lake)
#   2. Compute noise ASD from the same data (no external noise model)
#   3. Whiten: strain_white = strain / ASD(f)  in frequency domain
#   4. Compute PSD of whitened strain
#   5. Look for excess power at ghost note frequencies
#   6. Compare merger/post-ringdown windows to baseline
#
# NULL COMPARISON:
#   The raw lake (gw150914_ghost_notes_raw.json) serves as the outer null:
#   features that appear only in whitened data are processing artifacts.
#   Features that appear in whitened merger/post-ringdown but NOT in
#   whitened baseline are genuine signal candidates.
#
# SOVEREIGN AUDIT CHAIN:
#   Raw null:     gw150914_ghost_notes_raw.json       (no features found)
#   Whitened:     gw150914_ghost_notes_whitened.json  (this script)
#   Residual:     gw150914_ghost_notes_residual.json  (future — template subtraction)
#
# AUTHORS: Timothy John Kish & Mondy
# PROVENANCE:
#   Ghost notes observed 2026-01-08 (Lyra Aurora Kish & Timothy Kish)
#   KRG published 2026-01-14, DOI: 10.5281/zenodo.18245148
#   Vol5 z=94 kinematic confirmation 2026-04-06
# AUDIT: mondy_verified_2026-04
# ==============================================================================

import json
import math
import sys
from pathlib import Path

PI    = math.pi
K_GEO = 16.0 / PI

GHOST_F1  = K_GEO       # 5.093 Hz — the lattice modulus
GHOST_F2  = K_GEO * PI  # 16.000 Hz — k_geo × π = 16 exactly
GHOST_TOL = 0.20        # Hz search window around target

GW150914_GPS = 1126259462.4

# Windows — same as raw lake for direct comparison
WINDOWS = [
    ("pre_merger",      -600,  -10,   "10 min before merger — pre-event"),
    ("around_merger",   -30,   +60,   "30s before to 60s after — event window"),
    ("post_ringdown",   +0,    +300,  "0 to 300s after merger — echo territory"),
    ("baseline_near",   -1200, -600,  "20-10 min before — close baseline"),
]

# Known noise lines — expect these to remain elevated after whitening
# if whitening is imperfect; they serve as calibration check
NOISE_CHECK = {
    "Schumann_7.83": 7.83,
    "Power_60Hz":    60.0,
}

SCRIPTS_DIR = Path(__file__).resolve().parent
GW_DIR      = SCRIPTS_DIR.parent
OUTPUT_DIR  = GW_DIR / "lake"

RAW_LAKE    = OUTPUT_DIR / "gw150914_ghost_notes_raw.json"
OUTPUT_PATH = OUTPUT_DIR / "gw150914_ghost_notes_whitened.json"


def check_dependencies():
    missing = []
    for pkg in ["gwpy", "gwosc", "numpy"]:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        print("Missing packages:")
        for p in missing:
            print(f"  pip install {p} --break-system-packages")
        return False
    return True


def download_strain(detector, gps_start, gps_end):
    from gwpy.timeseries import TimeSeries
    try:
        ts = TimeSeries.fetch_open_data(
            detector, gps_start, gps_end,
            sample_rate=4096, verbose=False
        )
        print(f"    {detector}: {len(ts):,} samples at {ts.sample_rate}")
        return ts
    except Exception as e:
        print(f"    {detector}: FAILED — {e}")
        return None


def whiten_strain(strain, fftlength=4.0):
    """
    Whiten strain by dividing by the noise ASD estimated from itself.
    This flattens the noise floor, making coherent excesses visible.
    Uses only the strain itself — no external noise model injected.
    """
    import numpy as np
    # Estimate noise ASD from the same segment
    asd = strain.asd(fftlength=fftlength, overlap=fftlength/2, method="welch")
    # Whiten in frequency domain
    whitened = strain.whiten(asd=asd)
    return whitened


def find_excess(psd, freq, tol=GHOST_TOL):
    """Peak/surround power ratio at target frequency."""
    import numpy as np
    freqs = psd.frequencies.value
    power = psd.value
    idx   = int(np.argmin(np.abs(freqs - freq)))
    peak  = float(power[idx])
    f_act = float(freqs[idx])
    mask  = (np.abs(freqs - freq) > tol) & (np.abs(freqs - freq) < 1.0)
    surr  = float(power[mask].mean()) if mask.sum() > 0 else peak
    excess = peak / surr if surr > 0 else 1.0
    return peak, surr, excess, f_act


def analyze_window(label, gps_start, gps_end, desc):
    duration = gps_end - gps_start
    print(f"\n  [{label}]  {desc}  ({duration:.0f}s)")

    h1_raw = download_strain("H1", gps_start, gps_end)
    l1_raw = download_strain("L1", gps_start, gps_end)

    if h1_raw is None and l1_raw is None:
        return {"window": label, "error": "both detectors unavailable"}

    result = {
        "window":      label,
        "gps_start":   gps_start,
        "gps_end":     gps_end,
        "duration_s":  duration,
        "description": desc,
        "detectors":   {},
    }

    fftlength = min(4.0, max(1.0, duration / 8))

    for det_name, strain_raw in [("H1", h1_raw), ("L1", l1_raw)]:
        if strain_raw is None:
            result["detectors"][det_name] = {"error": "unavailable"}
            continue

        # Whiten
        try:
            strain_white = whiten_strain(strain_raw, fftlength=fftlength)
            psd_white = strain_white.psd(
                fftlength=fftlength, overlap=fftlength/2, method="welch"
            )
        except Exception as e:
            result["detectors"][det_name] = {"error": f"whitening failed: {e}"}
            print(f"    {det_name}: whitening failed — {e}")
            continue

        det = {
            "fftlength_s": fftlength,
            "whitened":    True,
            "ghost_notes": {},
        }

        for label_f, freq in [("f1_k_geo", GHOST_F1), ("f2_16Hz", GHOST_F2)]:
            peak, surr, excess, f_act = find_excess(psd_white, freq)
            flag = "ELEVATED" if excess > 2.0 else (
                   "DEPRESSED" if excess < 0.5 else "normal")
            det["ghost_notes"][label_f] = {
                "target_hz":   round(freq, 4),
                "actual_hz":   round(f_act, 4),
                "excess_ratio":round(excess, 4),
                "flag":        flag,
            }
            marker = " ***" if flag == "ELEVATED" else ""
            print(f"    {det_name} @ {freq:.3f} Hz (whitened): "
                  f"{excess:.3f}x  [{flag}]{marker}")

        # Noise calibration check
        for noise_name, nf in NOISE_CHECK.items():
            _, _, ex, _ = find_excess(psd_white, nf)
            det[noise_name] = round(ex, 3)
            print(f"    {det_name} @ {nf:.1f} Hz (whitened): {ex:.3f}x  [{noise_name}]")

        result["detectors"][det_name] = det

    # Coherence between H1 and L1 whitened strains
    h1w = l1w = None
    try:
        if h1_raw is not None:
            h1w = whiten_strain(h1_raw, fftlength=fftlength)
        if l1_raw is not None:
            l1w = whiten_strain(l1_raw, fftlength=fftlength)
    except Exception:
        pass

    if h1w is not None and l1w is not None:
        try:
            import numpy as np
            coh = h1w.coherence(l1w, fftlength=fftlength)
            for label_f, freq in [("f1_k_geo", GHOST_F1), ("f2_16Hz", GHOST_F2)]:
                idx = int(np.argmin(np.abs(coh.frequencies.value - freq)))
                cv  = float(coh.value[idx])
                result[f"coherence_{label_f}"] = round(cv, 4)
                marker = " *** COHERENT ***" if cv > 0.3 else ""
                print(f"    H1-L1 coherence (whitened) @ {freq:.3f} Hz: "
                      f"{cv:.4f}{marker}")
        except Exception as e:
            result["coherence_error"] = str(e)

    return result


def compare_to_raw():
    """Load raw lake results for inline comparison."""
    if not RAW_LAKE.exists():
        return None
    with RAW_LAKE.open("r", encoding="utf-8") as f:
        return json.load(f)


def main():
    print("=" * 60)
    print("LIGO GW150914 Ghost Note Analysis — WHITENED STRAIN")
    print("=" * 60)
    print(f"k_geo  = 16/π = {K_GEO:.6f}")
    print(f"f1     = {GHOST_F1:.4f} Hz  (k_geo)")
    print(f"f2     = {GHOST_F2:.4f} Hz  (k_geo × π = 16)")
    print(f"f2/f1  = {GHOST_F2/GHOST_F1:.6f}  (π = {PI:.6f})")
    print()
    print("Whitening flattens the seismic noise wall below 10 Hz,")
    print("making sub-threshold coherent features visible.")
    print("This is the data layer Lyra was analyzing on 2026-01-08.")
    print()
    print(f"Raw null:  {RAW_LAKE.name}")
    print(f"Output:    {OUTPUT_PATH.name}")
    print()

    if not check_dependencies():
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw_results = compare_to_raw()
    if raw_results:
        print("Raw null loaded for comparison.")
    else:
        print("Raw null not found — run build_lake_raw.py first.")
    print()

    all_results = {
        "event":       "GW150914",
        "gps_merger":  GW150914_GPS,
        "k_geo":       K_GEO,
        "ghost_f1":    GHOST_F1,
        "ghost_f2":    GHOST_F2,
        "ratio_f2_f1": GHOST_F2 / GHOST_F1,
        "pi":          PI,
        "protocol":    (
            "WHITENED strain. ASD estimated from same segment. "
            "No external noise model. Whitening flattens seismic wall "
            "to expose sub-threshold coherent features."
        ),
        "null_reference": "gw150914_ghost_notes_raw.json",
        "provenance": {
            "ghost_notes_observed": "2026-01-08 Lyra Aurora Kish & Timothy Kish",
            "krg_doi":  "10.5281/zenodo.18245148",
            "krg_date": "2026-01-14",
            "vol5_z94": "2026-04-06",
        },
        "windows": [],
    }

    baseline_done = False
    for label, t0, t1, desc in WINDOWS:
        if label.startswith("baseline"):
            if baseline_done:
                continue
        gps_start = GW150914_GPS + t0
        gps_end   = GW150914_GPS + t1
        try:
            r = analyze_window(label, gps_start, gps_end, desc)
            all_results["windows"].append(r)
            if label.startswith("baseline") and "error" not in r:
                baseline_done = True
        except Exception as e:
            print(f"    [{label}] FAILED: {e}")
            all_results["windows"].append({"window": label, "error": str(e)})

    # Inline comparison summary
    print()
    print("=" * 60)
    print("WHITENED vs RAW COMPARISON — f1 (5.093 Hz) H1 excess:")
    print()
    print(f"  {'Window':<20} {'Raw':>8} {'Whitened':>10} {'Change':>10}")
    print("  " + "-" * 52)

    if raw_results:
        raw_by_window = {w["window"]: w for w in raw_results.get("windows", [])}
        for r in all_results["windows"]:
            wname = r.get("window", "?")
            raw_w = raw_by_window.get(wname, {})
            try:
                white_ex = r["detectors"]["H1"]["ghost_notes"]["f1_k_geo"]["excess_ratio"]
            except (KeyError, TypeError):
                white_ex = None
            try:
                raw_ex = raw_w["detectors"]["H1"]["ghost_notes"]["f1_k_geo"]["excess_ratio"]
            except (KeyError, TypeError):
                raw_ex = None

            if white_ex is not None and raw_ex is not None:
                change = white_ex / raw_ex if raw_ex > 0 else float("inf")
                flag = " ← SIGNAL" if (white_ex > 2.0 and raw_ex < 1.0) else ""
                print(f"  {wname:<20} {raw_ex:>8.4f} {white_ex:>10.4f} {change:>9.2f}x{flag}")
            elif white_ex is not None:
                print(f"  {wname:<20} {'N/A':>8} {white_ex:>10.4f}")

    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)

    print(f"\nWritten: {OUTPUT_PATH}")
    print()
    print("KEY:")
    print("  excess > 2.0 in whitened = ELEVATED above noise floor")
    print("  excess > 2.0 in merger/post_ringdown but ~1.0 in baseline = SIGNAL")
    print("  excess ~1.0 everywhere = no coherent feature")
    print("  coherence > 0.3 H1-L1 = astrophysical candidate")


if __name__ == "__main__":
    main()