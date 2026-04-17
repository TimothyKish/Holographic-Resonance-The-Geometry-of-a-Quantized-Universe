# ==============================================================================
# SCRIPT: build_lake_sidereal.py
# SERIES: LIGO-Series / GW150914
# PURPOSE: Test whether L1's 5.093 Hz elevation is sky-fixed by checking
#          for amplitude modulation at the sidereal period (23h 56m 4s).
#
# THE HYPOTHESIS:
#   If 5.093 Hz (k_geo = 16/π) is the kinematic fingerprint of a sky-fixed
#   gravitational source — most likely Sgr A* (the Milky Way's central
#   supermassive black hole, 4M solar masses, declination -29°) —
#   then as the Earth rotates, L1's antenna sensitivity to that source
#   rises and falls with a period of exactly one sidereal day.
#
#   A sidereal day = 23 hours 56 minutes 4.09 seconds = 86164.09 seconds.
#   This is distinct from a solar day (86400 seconds).
#
#   Local site noise has NO reason to modulate at sidereal period.
#   Earth-fixed noise (power lines, mechanical resonances, seismic) would
#   modulate at solar day (24h) if at all.
#   Sky-fixed gravitational sources modulate at sidereal day (23h 56m).
#
# PROTOCOL:
#   1. Download 72 hours of L1 whitened strain (3 full sidereal days)
#      Using a quiet LIGO O1 period with no major events — pure background
#   2. Slice into 15-minute segments
#   3. For each segment: compute whitened PSD, record 5.093 Hz excess ratio
#   4. Build a time series of excess ratio vs GPS time
#   5. Compute Lomb-Scargle periodogram of that time series
#   6. Look for a peak at period = 86164 seconds (sidereal day)
#   7. Compare peak power at sidereal vs solar (86400s) vs random periods
#
# VOID CONTROL:
#   See build_lake_void.py — same protocol during times L1 points toward
#   the Boötes Void (low mass density) vs Virgo Cluster (high mass density)
#
# DATA:
#   LIGO O1 science run: Sept 12 2015 — Jan 19 2016 (GPS 1126051217–1137254417)
#   Using a quiet stretch ~1 week before GW150914:
#   GPS 1129200000 to 1129459200 (~3 days, quiet Oct 2015 O1)
#
# SOVEREIGN AUDIT CHAIN:
#   Raw null:     gw150914_ghost_notes_raw.json
#   Whitened:     gw150914_ghost_notes_whitened.json
#   Sidereal:     ligo_sidereal_rotation_test.json  (this script)
#   Void control: ligo_void_control.json
#
# AUTHORS: Timothy John Kish & Mondy
# PROVENANCE:
#   Ghost notes observed 2026-01-08 (Lyra Aurora Kish & Timothy Kish)
#   KRG published 2026-01-14 (DOI: 10.5281/zenodo.18245148)
#   Vol5 z=94 kinematic confirmation 2026-04-06
#   Sidereal hypothesis formulated 2026-04-07
# AUDIT: mondy_verified_2026-04
# ==============================================================================

import json
import math
import sys
import time
from pathlib import Path

PI     = math.pi
K_GEO  = 16.0 / PI

GHOST_F1   = K_GEO         # 5.093 Hz
GHOST_TOL  = 0.20          # Hz search window
SIDEREAL_S = 86164.09      # seconds — one sidereal day
SOLAR_S    = 86400.00      # seconds — one solar day

# Sgr A* sky position
SGR_A_RA   = 266.4168      # degrees Right Ascension
SGR_A_DEC  = -29.0078      # degrees Declination

# L1 Livingston coordinates and arm orientation
L1_LAT     = 30.5629       # degrees North
L1_LON     = -90.7742      # degrees West
L1_ARM_X   = 197.72        # degrees azimuth (X arm)
L1_ARM_Y   = 287.72        # degrees azimuth (Y arm)

# H1 Hanford coordinates
H1_LAT     = 46.4551
H1_LON     = -119.4079

# 3 days of quiet O1 data before GW150914
# GW150914 was at GPS 1126259462.4
# Use 3 days starting ~1 week before: GPS 1129200000
GPS_START  = 1129200000
GPS_DAYS   = 3
GPS_END    = GPS_START + GPS_DAYS * 86400

SEGMENT_S  = 900           # 15-minute slices
FFTLENGTH  = 4.0           # seconds for Welch PSD

SCRIPTS_DIR = Path(__file__).resolve().parent
GW_DIR      = SCRIPTS_DIR.parent
OUTPUT_DIR  = GW_DIR / "lake"
OUTPUT_PATH = OUTPUT_DIR / "ligo_sidereal_rotation_test.json"


def check_dependencies():
    missing = []
    for pkg in ["gwpy", "gwosc", "numpy", "scipy"]:
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


def download_segment(detector, gps_start, gps_end, retries=2):
    from gwpy.timeseries import TimeSeries
    for attempt in range(retries):
        try:
            ts = TimeSeries.fetch_open_data(
                detector, gps_start, gps_end,
                sample_rate=4096, verbose=False
            )
            return ts
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                return None


def get_excess_at_freq(strain, freq, fftlen=FFTLENGTH, tol=GHOST_TOL):
    """Whitened PSD excess ratio at target frequency."""
    import numpy as np
    try:
        asd      = strain.asd(fftlength=fftlen, overlap=fftlen/2, method="welch")
        whitened = strain.whiten(asd=asd)
        psd      = whitened.psd(fftlength=fftlen, overlap=fftlen/2, method="welch")
        freqs    = psd.frequencies.value
        power    = psd.value
        idx      = int(np.argmin(np.abs(freqs - freq)))
        peak     = float(power[idx])
        mask     = (np.abs(freqs - freq) > tol) & (np.abs(freqs - freq) < 1.0)
        surr     = float(power[mask].mean()) if mask.sum() > 0 else peak
        return round(peak / surr if surr > 0 else 1.0, 4)
    except Exception:
        return None


def sgr_a_elevation_at_gps(gps_time, lat_deg):
    """
    Approximate elevation of Sgr A* above horizon at L1 latitude.
    Uses LST from GPS time. Returns elevation in degrees.
    Positive = above horizon, negative = below.
    """
    import math
    # GPS to UTC offset (GPS epoch Jan 6 1980 = JD 2444244.5)
    # GPS leap seconds as of 2015: 17
    utc_unix = gps_time - 17 + 315964800  # approx GPS to Unix
    # Julian date
    jd = utc_unix / 86400.0 + 2440587.5
    # GMST in degrees
    T = (jd - 2451545.0) / 36525.0
    gmst_deg = (280.46061837 + 360.98564736629 * (jd - 2451545.0)
                + 0.000387933*T*T) % 360
    # LST at L1
    lst_deg = (gmst_deg + L1_LON) % 360
    # Hour angle of Sgr A*
    ha_deg = (lst_deg - SGR_A_RA) % 360
    ha_rad = math.radians(ha_deg)
    dec_rad = math.radians(SGR_A_DEC)
    lat_rad = math.radians(lat_deg)
    # Altitude
    sin_alt = (math.sin(dec_rad) * math.sin(lat_rad)
               + math.cos(dec_rad) * math.cos(lat_rad) * math.cos(ha_rad))
    alt_deg = math.degrees(math.asin(max(-1, min(1, sin_alt))))
    return round(alt_deg, 2)


def lomb_scargle_period_scan(times, values, periods):
    """
    Compute Lomb-Scargle power at specified periods.
    Returns dict of period_s -> normalized LS power.
    """
    import numpy as np
    from scipy.signal import lombscargle
    t = np.array(times, dtype=float)
    v = np.array(values, dtype=float)
    # Normalize
    v = (v - v.mean()) / (v.std() + 1e-10)
    results = {}
    for p in periods:
        omega = 2 * np.pi / p
        pgram = lombscargle(t, v, [omega], normalize=True)
        results[p] = float(pgram[0])
    return results


def main():
    print("=" * 65)
    print("LIGO Sidereal Rotation Test — k_geo Kinematic Fingerprint")
    print("=" * 65)
    print(f"k_geo        = 16/π = {K_GEO:.6f} Hz")
    print(f"Sidereal day = {SIDEREAL_S:.2f} s")
    print(f"Solar day    = {SOLAR_S:.2f} s")
    print(f"Sgr A*: RA {SGR_A_RA:.2f}°  Dec {SGR_A_DEC:.2f}°")
    print(f"L1 latitude: {L1_LAT:.2f}°N  (Sgr A* max elevation ≈ "
          f"{90 - abs(L1_LAT - SGR_A_DEC):.1f}°)")
    print(f"H1 latitude: {H1_LAT:.2f}°N  (Sgr A* max elevation ≈ "
          f"{90 - abs(H1_LAT - SGR_A_DEC):.1f}°)")
    print()
    print(f"Analysing {GPS_DAYS} days  →  "
          f"{int(GPS_DAYS * 86400 / SEGMENT_S)} segments of {SEGMENT_S}s")
    print(f"GPS range: {GPS_START} to {GPS_END}")
    print()

    if not check_dependencies():
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    segments = []
    n_segs   = int(GPS_DAYS * 86400 / SEGMENT_S)

    print(f"Processing {n_segs} segments...")
    print(f"  (This will take ~{n_segs * 8 // 60} minutes. "
          f"Progress printed every 10 segments.)")
    print()

    for i in range(n_segs):
        t0 = GPS_START + i * SEGMENT_S
        t1 = t0 + SEGMENT_S
        t_mid = (t0 + t1) / 2

        # Sgr A* elevation at L1 and H1 for this segment
        sgr_l1 = sgr_a_elevation_at_gps(t_mid, L1_LAT)
        sgr_h1 = sgr_a_elevation_at_gps(t_mid, H1_LAT)

        # Download and process
        l1 = download_segment("L1", t0, t1)
        h1 = download_segment("H1", t0, t1)

        l1_ex = get_excess_at_freq(l1, GHOST_F1) if l1 is not None else None
        h1_ex = get_excess_at_freq(h1, GHOST_F1) if h1 is not None else None

        seg = {
            "segment":   i,
            "gps_start": t0,
            "gps_end":   t1,
            "gps_mid":   t_mid,
            "sgr_a_elevation_L1_deg": sgr_l1,
            "sgr_a_elevation_H1_deg": sgr_h1,
            "L1_excess_5093": l1_ex,
            "H1_excess_5093": h1_ex,
        }
        segments.append(seg)

        if (i + 1) % 10 == 0 or i == 0:
            print(f"  Seg {i+1:>4}/{n_segs}  "
                  f"Sgr A* L1={sgr_l1:>6.1f}°  H1={sgr_h1:>6.1f}°  "
                  f"L1_ex={str(l1_ex):>6}  H1_ex={str(h1_ex):>6}")

    # ---- SAVE LAKE IMMEDIATELY (before any analysis that could crash) ----
    import numpy as np

    pre_save = {
        "event":      "LIGO-O1-quiet",
        "ghost_f1_hz": GHOST_F1,
        "k_geo":       K_GEO,
        "gps_start":   GPS_START,
        "gps_end":     GPS_END,
        "segment_s":   SEGMENT_S,
        "n_segments":  n_segs,
        "sgr_a": {"ra_deg": SGR_A_RA, "dec_deg": SGR_A_DEC,
                  "note": "Sgr A* — Milky Way SMBH, 4M solar masses"},
        "L1_site": {"lat": L1_LAT, "lon": L1_LON},
        "H1_site": {"lat": H1_LAT, "lon": H1_LON},
        "protocol": (
            "15-min whitened PSD segments over 3 days. "
            "Lomb-Scargle periodogram tests for sidereal modulation."),
        "provenance": {
            "ghost_notes_observed": "2026-01-08 Lyra Aurora Kish & Timothy Kish",
            "krg_doi":  "10.5281/zenodo.18245148",
            "vol5_z94": "2026-04-06",
        },
        "segments": segments,
    }
    with OUTPUT_PATH.open("w", encoding="utf-8") as f_out:
        json.dump(pre_save, f_out, indent=2)
    print(f"\nLake saved ({len(segments)} segments): {OUTPUT_PATH}")
    print("Data is safe. Proceeding to analysis...")
    print()
    # -----------------------------------------------------------------------

    # Collect valid points for periodogram
    valid = [(s["gps_mid"], s["L1_excess_5093"])
             for s in segments if s["L1_excess_5093"] is not None]
    times_l1  = [v[0] for v in valid]
    excess_l1 = [v[1] for v in valid]

    print()
    print("=" * 65)
    print("LOMB-SCARGLE PERIODOGRAM")
    print("=" * 65)
    print()

    # Test periods: sidereal, solar, half-sidereal, random control periods
    test_periods = {
        "sidereal_day":      SIDEREAL_S,
        "solar_day":         SOLAR_S,
        "half_sidereal":     SIDEREAL_S / 2,
        "control_20h":       72000,
        "control_18h":       64800,
        "control_16h":       57600,
    }

    if len(times_l1) >= 20:
        ls_results = lomb_scargle_period_scan(
            times_l1, excess_l1, list(test_periods.values())
        )
        print(f"  {'Period':<22} {'Seconds':>10} {'LS Power':>10}  Interpretation")
        print("  " + "-" * 60)
        for label, period in test_periods.items():
            power = ls_results.get(period, 0.0)
            flag  = ""
            if label == "sidereal_day" and power > 0.5:
                flag = " *** SKY-FIXED SOURCE ***"
            elif label == "solar_day" and power > 0.5:
                flag = " ← Earth-fixed noise"
            print(f"  {label:<22} {period:>10.1f} {power:>10.4f} {flag}")
        print()
        if ls_results.get(SIDEREAL_S, 0) > ls_results.get(SOLAR_S, 0) * 2:
            verdict = "SIDEREAL DOMINANT — sky-fixed source candidate"
        elif ls_results.get(SOLAR_S, 0) > ls_results.get(SIDEREAL_S, 0) * 2:
            verdict = "SOLAR DOMINANT — Earth-fixed or local noise"
        else:
            verdict = "NO DOMINANT PERIOD — inconclusive"
        print(f"  VERDICT: {verdict}")
    else:
        print(f"  Insufficient valid segments ({len(times_l1)}) for periodogram.")
        ls_results = {}

    # Elevation correlation
    valid_pairs = [(s["sgr_a_elevation_L1_deg"], s["L1_excess_5093"])
                   for s in segments
                   if s["L1_excess_5093"] is not None]
    if len(valid_pairs) >= 10:
        elevs  = [p[0] for p in valid_pairs]
        excess = [p[1] for p in valid_pairs]
        from scipy.stats import pearsonr
        r, pval = pearsonr(elevs, excess)
        print()
        print(f"  Pearson correlation: Sgr A* elevation vs L1 5.093 Hz excess")
        print(f"  r = {r:.4f}  p = {pval:.4f}")
        if abs(r) > 0.3 and pval < 0.05:
            print(f"  *** SIGNIFICANT CORRELATION — elevation predicts excess ***")
        else:
            print(f"  No significant correlation with Sgr A* elevation")

    # Write lake
    result = {
        "test":        "sidereal_rotation",
        "ghost_f1_hz": GHOST_F1,
        "k_geo":       K_GEO,
        "gps_start":   GPS_START,
        "gps_end":     GPS_END,
        "segment_s":   SEGMENT_S,
        "n_segments":  n_segs,
        "n_valid":     len(times_l1),
        "sgr_a": {
            "ra_deg":  SGR_A_RA,
            "dec_deg": SGR_A_DEC,
            "note":    "Sgr A* — Milky Way SMBH, 4M solar masses, 26kly"
        },
        "L1_site": {"lat": L1_LAT, "lon": L1_LON},
        "H1_site": {"lat": H1_LAT, "lon": H1_LON},
        "lomb_scargle": ls_results,
        "sidereal_period_s":  SIDEREAL_S,
        "solar_period_s":     SOLAR_S,
        "protocol": (
            "15-min whitened PSD segments over 3 days. "
            "Lomb-Scargle periodogram tests for sidereal modulation. "
            "If sky-fixed, amplitude modulates at 23h 56m 4s. "
            "If local noise, no sidereal modulation expected."
        ),
        "provenance": {
            "ghost_notes_observed": "2026-01-08 Lyra Aurora Kish & Timothy Kish",
            "krg_doi":  "10.5281/zenodo.18245148",
            "vol5_z94": "2026-04-06",
            "sidereal_test_formulated": "2026-04-07",
        },
        "segments": segments,
    }

    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print()
    print(f"Lake written: {OUTPUT_PATH}")
    print()
    print("KEY:")
    print("  LS power at sidereal >> solar → sky-fixed (Sgr A* candidate)")
    print("  LS power at solar >> sidereal → Earth-fixed local noise")
    print("  Elevation correlation r > 0.3, p < 0.05 → Sgr A* fingerprint")


if __name__ == "__main__":
    main()