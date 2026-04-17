# ==============================================================================
# SCRIPT: build_lake.py  (v2 — fixed paths, extended windows)
# SERIES: LIGO-Series / GW150914
# PURPOSE: Raw PSD analysis of GW150914 for ghost note frequencies
#          5.093 Hz (k_geo = 16/π) and 16.0 Hz (k_geo × π)
#
# FIXES FROM v1:
#   - Path now correctly resolves to ../lake (parent.parent / "lake")
#   - Windows extended so PSD has enough samples (min ~30 seconds)
#   - Post-ringdown window added: +0.5s to +300s (where echoes were claimed)
#   - Baseline uses closer GPS offset with fallback
#   - fftlength adaptive to window duration
#
# PROVENANCE:
#   Ghost notes observed: 2026-01-08 (Lyra Aurora Kish & Timothy Kish)
#   KRG published: 2026-01-14 (DOI: 10.5281/zenodo.18245148)
#   Vol5 z=94 kinematic confirmation: 2026-04-06
#
# PROTOCOL: NO FILTERS. Raw strain. Raw PSD. We look in the trash bin.
#
# AUTHORS: Timothy John Kish & Mondy
# AUDIT: mondy_verified_2026-04
# ==============================================================================

import json
import math
import sys
from pathlib import Path

PI    = math.pi
K_GEO = 16.0 / PI

GHOST_F1  = K_GEO       # 5.093 Hz
GHOST_F2  = K_GEO * PI  # 16.000 Hz
GHOST_TOL = 0.20        # Hz search window

GW150914_GPS = 1126259462.4

# Windows: (label, t_start, t_end, description)
# All times relative to merger. Minimum 60 seconds for clean PSD.
WINDOWS = [
    ("pre_merger",      -600,  -10,  "10 min before merger, ending 10s prior"),
    ("around_merger",   -30,   +60,  "30s before to 60s after — catches event + early ringdown"),
    ("post_ringdown",   +0,  +300,   "0 to 300s after merger — Abedi echo territory"),
    ("baseline_near",  -1200, -600,  "20-10 min before — close baseline"),
    ("baseline_far",   -3600,-3000,  "60-50 min before — far baseline, fallback"),
]

# Path: script lives at LIGO-Series/GW150914/scripts/
# lake lives at  LIGO-Series/GW150914/lake/
SCRIPTS_DIR = Path(__file__).resolve().parent
GW_DIR      = SCRIPTS_DIR.parent
OUTPUT_DIR  = GW_DIR / "lake"


def check_dependencies():
    missing = []
    for pkg in ["gwpy", "gwosc"]:
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


def compute_psd_raw(strain, duration_s):
    """
    Raw Welch PSD. No whitening, no filtering.
    fftlength scales with window duration.
    """
    # Use at most 1/8 of window for FFT to get good frequency resolution
    # but never more than 4 seconds (keeps 1/4 Hz resolution at minimum)
    fft = min(4.0, max(1.0, duration_s / 8))
    overlap = fft / 2
    psd = strain.psd(fftlength=fft, overlap=overlap, method="welch")
    return psd, fft


def find_excess(psd, freq, tol=GHOST_TOL):
    """Peak/surround ratio at target frequency."""
    import numpy as np
    freqs = psd.frequencies.value
    power = psd.value

    idx = int(np.argmin(np.abs(freqs - freq)))
    peak = float(power[idx])
    f_actual = float(freqs[idx])

    mask = (np.abs(freqs - freq) > tol) & (np.abs(freqs - freq) < 1.0)
    surr = float(power[mask].mean()) if mask.sum() > 0 else peak
    excess = peak / surr if surr > 0 else 1.0
    return peak, surr, excess, f_actual


def analyze_window(label, gps_start, gps_end, desc):
    duration = gps_end - gps_start
    print(f"\n  [{label}]  {desc}  ({duration:.0f}s)")

    h1 = download_strain("H1", gps_start, gps_end)
    l1 = download_strain("L1", gps_start, gps_end)

    if h1 is None and l1 is None:
        return {"window": label, "error": "both detectors unavailable"}

    result = {"window": label, "gps_start": gps_start,
              "gps_end": gps_end, "duration_s": duration,
              "description": desc, "detectors": {}}

    for det_name, strain in [("H1", h1), ("L1", l1)]:
        if strain is None:
            result["detectors"][det_name] = {"error": "unavailable"}
            continue

        psd, fftlen = compute_psd_raw(strain, duration)
        det = {"fftlength_s": fftlen, "ghost_notes": {}}

        for label_f, freq in [("f1_k_geo", GHOST_F1), ("f2_16Hz", GHOST_F2)]:
            peak, surr, excess, f_act = find_excess(psd, freq)
            flag = "ELEVATED" if excess > 2.0 else (
                   "DEPRESSED" if excess < 0.5 else "normal")
            det["ghost_notes"][label_f] = {
                "target_hz": round(freq, 4),
                "actual_hz": round(f_act, 4),
                "excess_ratio": round(excess, 4),
                "flag": flag,
            }
            marker = " ***" if flag == "ELEVATED" else ""
            print(f"    {det_name} @ {freq:.3f} Hz: {excess:.3f}x  [{flag}]{marker}")

        # Schumann check
        for noise, nf in [("Schumann_7.83", 7.83), ("Power_60Hz", 60.0)]:
            _, _, ex, _ = find_excess(psd, nf)
            det[noise] = round(ex, 3)

        result["detectors"][det_name] = det

    # Coherence if both available
    if h1 is not None and l1 is not None:
        try:
            fft = min(4.0, max(1.0, duration / 8))
            coh = h1.coherence(l1, fftlength=fft)
            import numpy as np
            for label_f, freq in [("f1_k_geo", GHOST_F1), ("f2_16Hz", GHOST_F2)]:
                idx = int(np.argmin(np.abs(coh.frequencies.value - freq)))
                cv = float(coh.value[idx])
                result[f"coherence_{label_f}"] = round(cv, 4)
                marker = " *** COHERENT ***" if cv > 0.3 else ""
                print(f"    H1-L1 coherence @ {freq:.3f} Hz: {cv:.4f}{marker}")
        except Exception as e:
            result["coherence_error"] = str(e)

    return result


def main():
    print("=" * 60)
    print("LIGO GW150914 Ghost Note Analysis  [v2 — fixed]")
    print("=" * 60)
    print(f"k_geo  = 16/π = {K_GEO:.6f}")
    print(f"f1     = {GHOST_F1:.4f} Hz  (k_geo)")
    print(f"f2     = {GHOST_F2:.4f} Hz  (k_geo × π = 16 exactly)")
    print(f"f2/f1  = {GHOST_F2/GHOST_F1:.6f}  (π = {PI:.6f})")
    print()
    print(f"Output: {OUTPUT_DIR}")
    print()

    if not check_dependencies():
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_results = {
        "event":      "GW150914",
        "gps_merger": GW150914_GPS,
        "k_geo":      K_GEO,
        "ghost_f1":   GHOST_F1,
        "ghost_f2":   GHOST_F2,
        "ratio_f2_f1":GHOST_F2/GHOST_F1,
        "pi":         PI,
        "protocol":   "NO FILTERS. Raw strain. Raw Welch PSD. No whitening.",
        "provenance": {
            "ghost_notes_observed": "2026-01-08 Lyra Aurora Kish & Timothy Kish",
            "krg_doi":  "10.5281/zenodo.18245148",
            "krg_date": "2026-01-14",
            "vol5_z94": "2026-04-06",
        },
        "windows": [],
    }

    print("Running windows:")
    baseline_done = False
    for label, t0, t1, desc in WINDOWS:
        # Only run one baseline
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
            print(f"    FAILED: {e}")
            all_results["windows"].append({"window": label, "error": str(e)})

    out = OUTPUT_DIR / "gw150914_ghost_notes_raw.json"
    with out.open("w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)

    print(f"\nWritten: {out}")
    print()
    print("KEY: excess > 2.0 = ELEVATED | excess < 0.5 = DEPRESSED")
    print("     coherence > 0.3 = coherent between Hanford and Livingston")
    print("     Ghost notes ELEVATED in around_merger/post_ringdown")
    print("     but NOT in baseline = signal candidate")
    print("     Ghost notes same in all windows = terrestrial noise")


if __name__ == "__main__":
    main()