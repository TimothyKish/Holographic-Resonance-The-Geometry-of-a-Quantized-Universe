# ==============================================================================
# SCRIPT: analyse_sidereal_lake.py
# PURPOSE: Load existing ligo_sidereal_rotation_test.json lake and run
#          the Lomb-Scargle periodogram analysis — no re-download required.
#
# The sidereal build script successfully collected all 288 segments.
# The crash was only in the final Lomb-Scargle step (scipy.signal.lombscargle
# returns a 0-dimensional array when passed a single frequency — needs float).
#
# This script loads the saved lake and runs the full analysis.
#
# AUTHORS: Timothy John Kish & Mondy
# AUDIT: mondy_verified_2026-04
# ==============================================================================

import json
import math
import sys
from pathlib import Path

PI     = math.pi
K_GEO  = 16.0 / PI
SIDEREAL_S = 86164.09
SOLAR_S    = 86400.00

SGR_A_RA   = 266.4168
SGR_A_DEC  = -29.0078
L1_LAT     = 30.5629

SCRIPTS_DIR = Path(__file__).resolve().parent
GW_DIR      = SCRIPTS_DIR.parent
LAKE_DIR    = GW_DIR / "lake"
LAKE_PATH   = LAKE_DIR / "ligo_sidereal_rotation_test.json"
OUTPUT_PATH = LAKE_DIR / "ligo_sidereal_analysis.json"


def lomb_scargle_periods(times, values, periods):
    """
    Fixed Lomb-Scargle — handles both scalar and array lombscargle output.
    scipy.signal.lombscargle needs angular frequencies (rad/s), not periods.
    """
    import numpy as np
    from scipy.signal import lombscargle

    t = np.array(times, dtype=float)
    v = np.array(values, dtype=float)
    v = (v - v.mean()) / (v.std() + 1e-10)

    results = {}
    for period in periods:
        omega = 2.0 * PI / period
        # Pass as 1-element array to guarantee array output
        pgram = lombscargle(t, v, np.array([omega]), normalize=True)
        results[period] = float(np.asarray(pgram).flat[0])
    return results


def elevation_at_gps(gps_time):
    """Sgr A* elevation above L1 horizon."""
    utc_unix = gps_time - 17 + 315964800
    jd = utc_unix / 86400.0 + 2440587.5
    T = (jd - 2451545.0) / 36525.0
    gmst = (280.46061837 + 360.98564736629*(jd-2451545.0)
            + 0.000387933*T*T) % 360
    lst  = (gmst + (-90.7742)) % 360
    ha   = math.radians((lst - SGR_A_RA) % 360)
    dec  = math.radians(SGR_A_DEC)
    lat  = math.radians(L1_LAT)
    sin_alt = (math.sin(dec)*math.sin(lat)
               + math.cos(dec)*math.cos(lat)*math.cos(ha))
    return math.degrees(math.asin(max(-1, min(1, sin_alt))))


def main():
    import numpy as np

    if not LAKE_PATH.exists():
        print(f"Lake not found: {LAKE_PATH}")
        print("Run build_lake_sidereal.py first.")
        sys.exit(1)

    print("=" * 65)
    print("LIGO Sidereal Analysis — Loading Existing Lake")
    print("=" * 65)
    print(f"Lake: {LAKE_PATH.name}")
    print()

    with LAKE_PATH.open("r", encoding="utf-8") as f:
        lake = json.load(f)

    segments = lake.get("segments", [])
    print(f"Loaded {len(segments)} segments")

    # Extract valid L1 time series
    valid = []
    for seg in segments:
        ex = seg.get("L1_excess_5093")
        t  = seg.get("gps_mid")
        el = seg.get("sgr_a_elevation_L1_deg")
        if ex is not None and ex > 0 and t is not None:
            valid.append((t, ex, el if el is not None else 0.0))

    print(f"Valid L1 segments: {len(valid)}")
    if len(valid) < 10:
        print("Insufficient data. Exiting.")
        sys.exit(1)

    times_l1  = [v[0] for v in valid]
    excess_l1 = [v[1] for v in valid]
    elevs_l1  = [v[2] for v in valid]

    print()
    print(f"L1 excess range: {min(excess_l1):.3f} — {max(excess_l1):.3f}")
    print(f"L1 excess mean:  {np.mean(excess_l1):.4f}")
    print(f"L1 excess std:   {np.std(excess_l1):.4f}")
    print()

    # -------------------------------------------------------------------------
    # Lomb-Scargle periodogram
    # -------------------------------------------------------------------------
    test_periods = {
        "sidereal_day":   SIDEREAL_S,
        "solar_day":      SOLAR_S,
        "half_sidereal":  SIDEREAL_S / 2.0,
        "control_20h":    72000.0,
        "control_18h":    64800.0,
        "control_16h":    57600.0,
        "control_12h":    43200.0,
    }

    print("=" * 65)
    print("LOMB-SCARGLE PERIODOGRAM")
    print("=" * 65)
    print()

    ls = lomb_scargle_periods(times_l1, excess_l1, list(test_periods.values()))

    print(f"  {'Label':<20} {'Period (s)':>12} {'LS Power':>10}  Note")
    print("  " + "-" * 60)
    for label, period in test_periods.items():
        power = ls[period]
        note  = ""
        if label == "sidereal_day":
            if power > 0.3:
                note = " *** SKY-FIXED SOURCE CANDIDATE ***"
            elif power > 0.1:
                note = " ← moderate sidereal signal"
        if label == "solar_day" and power > 0.3:
            note = " ← Earth-fixed noise"
        print(f"  {label:<20} {period:>12.1f} {power:>10.4f} {note}")

    sidereal_power = ls[SIDEREAL_S]
    solar_power    = ls[SOLAR_S]
    ratio          = sidereal_power / max(solar_power, 1e-10)

    print()
    print(f"  Sidereal/Solar ratio: {ratio:.2f}x")
    if ratio > 3.0 and sidereal_power > 0.1:
        verdict_ls = f"SIDEREAL DOMINANT ({ratio:.1f}x over solar) — sky-fixed candidate"
    elif ratio < 0.5:
        verdict_ls = "SOLAR DOMINANT — Earth-fixed or site noise"
    elif sidereal_power < 0.05:
        verdict_ls = "NO CLEAR PERIOD — signal not periodic at these timescales"
    else:
        verdict_ls = f"INCONCLUSIVE — sidereal/solar ratio {ratio:.2f}"
    print(f"  Verdict: {verdict_ls}")

    # -------------------------------------------------------------------------
    # Elevation correlation
    # -------------------------------------------------------------------------
    print()
    print("=" * 65)
    print("SGR A* ELEVATION CORRELATION")
    print("=" * 65)
    print()

    from scipy.stats import pearsonr, spearmanr

    # All valid segments
    r_p, p_p = pearsonr(elevs_l1, excess_l1)
    r_s, p_s = spearmanr(elevs_l1, excess_l1)
    print(f"  All {len(valid)} valid segments:")
    print(f"    Pearson  r={r_p:+.4f}  p={p_p:.4f}")
    print(f"    Spearman r={r_s:+.4f}  p={p_s:.4f}")

    if abs(r_p) > 0.2 and p_p < 0.05:
        print(f"    *** SIGNIFICANT — elevation predicts L1 5.093 Hz excess ***")
        if r_p > 0:
            print(f"    Direction: POSITIVE — higher elevation = stronger signal")
            print(f"    Consistent with Sgr A* as sky source")
        else:
            print(f"    Direction: NEGATIVE — unexpected (lower elevation = stronger?)")
    else:
        print(f"    No significant linear correlation with Sgr A* elevation")

    # Split by elevation quartile
    print()
    print(f"  L1 excess by Sgr A* elevation quartile:")
    elev_arr = np.array(elevs_l1)
    ex_arr   = np.array(excess_l1)
    q25, q50, q75 = np.percentile(elev_arr, [25, 50, 75])
    for label, mask in [
        (f"Q1 elev < {q25:.0f}°",  elev_arr < q25),
        (f"Q2 {q25:.0f}°–{q50:.0f}°", (elev_arr >= q25) & (elev_arr < q50)),
        (f"Q3 {q50:.0f}°–{q75:.0f}°", (elev_arr >= q50) & (elev_arr < q75)),
        (f"Q4 elev > {q75:.0f}°",  elev_arr >= q75),
    ]:
        subset = ex_arr[mask]
        if len(subset) > 0:
            print(f"    {label:<22}  n={len(subset):>3}  "
                  f"mean={subset.mean():.4f}  std={subset.std():.4f}")

    # -------------------------------------------------------------------------
    # Time series summary
    # -------------------------------------------------------------------------
    print()
    print("=" * 65)
    print("EXCESS TIME SERIES — Sample (every 24 segments ≈ 6 hours)")
    print("=" * 65)
    print()
    print(f"  {'GPS mid':<14} {'Sgr A* elev':>12} {'L1 excess':>10}")
    print("  " + "-" * 40)
    for i in range(0, len(valid), 24):
        t, ex, el = valid[i]
        bar = "+" * min(20, max(0, int((ex-1)*5))) if ex > 1 else ""
        print(f"  {t:<14.0f} {el:>+12.1f}° {ex:>10.4f}  {bar}")

    # -------------------------------------------------------------------------
    # Save results
    # -------------------------------------------------------------------------
    result = {
        "analysis":         "sidereal_rotation",
        "lake_source":      str(LAKE_PATH.name),
        "n_valid_segments": len(valid),
        "l1_excess_mean":   float(np.mean(excess_l1)),
        "l1_excess_std":    float(np.std(excess_l1)),
        "lomb_scargle":     {str(k): v for k, v in ls.items()},
        "sidereal_power":   sidereal_power,
        "solar_power":      solar_power,
        "sidereal_solar_ratio": ratio,
        "verdict_ls":       verdict_ls,
        "pearson_r":        r_p,
        "pearson_p":        p_p,
        "spearman_r":       float(r_s),
        "spearman_p":       float(p_s),
    }

    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print()
    print(f"Analysis written: {OUTPUT_PATH}")
    print()
    print("INTERPRETATION:")
    print("  LS sidereal >> solar AND r > 0.2, p < 0.05:")
    print("    → Sky-fixed source. L1 sees it, H1 does not.")
    print("    → Consistent with Sgr A* or local MW gravitational field.")
    print("  LS flat AND r ≈ 0:")
    print("    → No sky dependence. Site noise at k_geo by coincidence.")


if __name__ == "__main__":
    main()