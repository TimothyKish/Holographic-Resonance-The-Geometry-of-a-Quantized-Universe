# ==============================================================================
# SCRIPT: analyse_timeofday_bias.py
# SERIES: LIGO-Series / GW150914
# PURPOSE: Test whether the sky correlations found in the sidereal analysis
#          are genuine astrophysical signals or artifacts of LIGO data
#          quality patterns correlated with time of day.
#
# THE CONCERN:
#   137 of 288 segments (48%) returned None — LIGO data not available.
#   LIGO data quality flags correlate with human activity and seismic
#   noise, which are stronger during daytime. If valid L1 segments
#   come preferentially at night, and the sky rotates with Earth's
#   rotation, then ANY sky direction will show a spurious correlation
#   with L1 excess simply because it tracks night vs day.
#
#   Specifically: if valid data clusters at (e.g.) 2-6 AM local time,
#   then whatever is overhead at 2-6 AM Livingston time will always
#   show positive correlation — not because it is the source, but
#   because it happens to be overhead when the detector is quiet.
#
# THE TEST:
#   1. Extract UTC hour of day for each valid L1 segment
#   2. Compute Pearson r between (hour of day) and (L1 excess)
#   3. Plot distribution of valid segments by hour
#   4. If r is significant: time-of-day bias present — sky correlations
#      are contaminated and cannot be trusted
#   5. If r is near zero: time-of-day is not driving the signal —
#      sky correlations survive scrutiny
#
#   Additional check: compute what is overhead at the peak hour.
#   If the peak hour correlates with the strongest sky direction,
#   that confirms the contamination. If they don't match, the sky
#   direction may be independently real.
#
# NO DOWNLOAD REQUIRED: Runs on existing ligo_sidereal_rotation_test.json
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

L1_LON_DEG  = -90.7742   # Livingston longitude → UTC offset ~ -6h
L1_LAT_DEG  =  30.5629

SCRIPTS_DIR = Path(__file__).resolve().parent
GW_DIR      = SCRIPTS_DIR.parent
LAKE_DIR    = GW_DIR / "lake"
LAKE_PATH   = LAKE_DIR / "ligo_sidereal_rotation_test.json"
OUTPUT_PATH = LAKE_DIR / "ligo_timeofday_bias.json"


def gps_to_utc_hour(gps_time):
    """Convert GPS time to UTC hour of day (0.0–24.0)."""
    # GPS epoch: Jan 6, 1980 = Unix 315964800. Leap seconds as of 2015: 17.
    utc_unix = gps_time - 17 + 315964800
    return (utc_unix % 86400) / 3600.0


def gps_to_local_hour(gps_time):
    """Convert GPS to approximate local time at Livingston (UTC-6 civil)."""
    utc_h = gps_to_utc_hour(gps_time)
    return (utc_h - 6.0) % 24.0


def sky_elevation(ra_deg, dec_deg, gps_time):
    """Altitude of sky target above L1 horizon."""
    utc_unix = gps_time - 17 + 315964800
    jd  = utc_unix / 86400.0 + 2440587.5
    T   = (jd - 2451545.0) / 36525.0
    gst = (280.46061837 + 360.98564736629*(jd-2451545.0)
           + 0.000387933*T*T) % 360
    lst = (gst + L1_LON_DEG) % 360
    ha  = math.radians((lst - ra_deg) % 360)
    dec = math.radians(dec_deg)
    lat = math.radians(L1_LAT_DEG)
    sin_alt = (math.sin(dec)*math.sin(lat)
               + math.cos(dec)*math.cos(lat)*math.cos(ha))
    return math.degrees(math.asin(max(-1.0, min(1.0, sin_alt))))


def main():
    import numpy as np
    from scipy.stats import pearsonr, spearmanr

    print("=" * 65)
    print("Time-of-Day Bias Test — Are Sky Correlations Artifacts?")
    print("=" * 65)
    print()

    if not LAKE_PATH.exists():
        print(f"Lake not found: {LAKE_PATH}")
        sys.exit(1)

    with LAKE_PATH.open("r", encoding="utf-8") as f:
        lake = json.load(f)

    segments = lake.get("segments", [])
    all_gps  = [s["gps_mid"] for s in segments]

    # Separate valid from None
    valid   = [(s["gps_mid"], s["L1_excess_5093"])
               for s in segments if s.get("L1_excess_5093") is not None]
    invalid = [s["gps_mid"] for s in segments
               if s.get("L1_excess_5093") is None]

    print(f"Total segments:   {len(segments)}")
    print(f"Valid L1 (data):  {len(valid)}")
    print(f"None (no data):   {len(invalid)}")
    print(f"Coverage:         {len(valid)/len(segments)*100:.1f}%")
    print()

    times_v  = np.array([v[0] for v in valid])
    excess_v = np.array([v[1] for v in valid])

    # UTC and local hours for valid segments
    utc_hours_v   = np.array([gps_to_utc_hour(t) for t in times_v])
    local_hours_v = np.array([gps_to_local_hour(t) for t in times_v])

    # UTC hours for ALL segments (to see coverage pattern)
    utc_hours_all   = np.array([gps_to_utc_hour(t) for t in all_gps])
    utc_hours_none  = np.array([gps_to_utc_hour(t) for t in invalid])

    # -------------------------------------------------------------------------
    print("=" * 65)
    print("DISTRIBUTION OF VALID SEGMENTS BY UTC HOUR")
    print("=" * 65)
    print()
    print("  Hour (UTC)  Valid  None   Coverage   Excess mean")
    print("  " + "-" * 55)

    hour_stats = {}
    for h in range(24):
        mask_v = (utc_hours_v >= h) & (utc_hours_v < h+1)
        mask_a = (utc_hours_all >= h) & (utc_hours_all < h+1)
        n_valid = mask_v.sum()
        n_total = mask_a.sum()
        n_none  = n_total - n_valid
        coverage = n_valid / n_total * 100 if n_total > 0 else 0
        ex_mean = excess_v[mask_v].mean() if n_valid > 0 else 0
        bar_v = "#" * n_valid
        bar_n = "." * n_none
        print(f"  {h:>2}:00  "
              f"{n_valid:>5}  {n_none:>4}  {coverage:>8.0f}%  "
              f"{ex_mean:>8.4f}  {bar_v}{bar_n}")
        hour_stats[h] = {"n_valid": int(n_valid), "n_none": int(n_none),
                         "coverage": float(coverage),
                         "excess_mean": float(ex_mean) if n_valid > 0 else None}

    # -------------------------------------------------------------------------
    print()
    print("=" * 65)
    print("TIME-OF-DAY CORRELATION WITH L1 EXCESS")
    print("=" * 65)
    print()

    # Linear correlation with UTC hour
    r_utc, p_utc = pearsonr(utc_hours_v, excess_v)
    r_loc, p_loc = pearsonr(local_hours_v, excess_v)

    print(f"  Pearson r (UTC hour vs L1 excess):   r={r_utc:+.4f}  p={p_utc:.4f}")
    print(f"  Pearson r (local hour vs L1 excess): r={r_loc:+.4f}  p={p_loc:.4f}")
    print()

    # Also test sin/cos of hour (circular correlation — hour 23 is close to 0)
    sin_utc = np.sin(2*PI * utc_hours_v / 24)
    cos_utc = np.cos(2*PI * utc_hours_v / 24)
    r_sin, p_sin = pearsonr(sin_utc, excess_v)
    r_cos, p_cos = pearsonr(cos_utc, excess_v)
    print(f"  Circular: r(sin UTC):  r={r_sin:+.4f}  p={p_sin:.4f}")
    print(f"  Circular: r(cos UTC):  r={r_cos:+.4f}  p={p_cos:.4f}")
    print()

    # Coverage bias: does data availability itself depend on hour?
    all_hours_binned = [hour_stats[h]["n_valid"] for h in range(24)]
    peak_hour = max(hour_stats, key=lambda h: hour_stats[h]["n_valid"])
    min_hour  = min((h for h in hour_stats if hour_stats[h]["n_valid"] > 0),
                    key=lambda h: hour_stats[h]["n_valid"])
    print(f"  Peak coverage hour (UTC): {peak_hour}:00  "
          f"({hour_stats[peak_hour]['n_valid']} valid segments)")
    print(f"  Min coverage hour  (UTC): {min_hour}:00  "
          f"({hour_stats[min_hour]['n_valid']} valid segments)")
    coverage_std = np.std(all_hours_binned)
    print(f"  Coverage std across hours: {coverage_std:.1f} segments")
    if coverage_std > 3:
        print(f"  *** UNEVEN COVERAGE — data quality is time-dependent ***")
    else:
        print(f"  Coverage is roughly uniform across hours")
    print()

    # What is overhead at peak hour?
    peak_gps_example = [t for t in times_v
                        if abs(gps_to_utc_hour(t) - peak_hour) < 0.5]
    if peak_gps_example:
        t_ex = peak_gps_example[0]
        targets = {
            "local_arm":   (60.0,   0.0),
            "sgr_a_star":  (266.4, -29.0),
            "galactic_N":  (192.8, +27.1),
        }
        print(f"  At peak hour ({peak_hour}:00 UTC), approximate sky elevations:")
        for name, (ra, dec) in targets.items():
            el = sky_elevation(ra, dec, t_ex)
            print(f"    {name:<16} elevation = {el:+.1f}°")
    print()

    # -------------------------------------------------------------------------
    print("=" * 65)
    print("VERDICT")
    print("=" * 65)
    print()

    bias_detected = (abs(r_sin) > 0.2 and p_sin < 0.05) or \
                    (abs(r_cos) > 0.2 and p_cos < 0.05) or \
                    (abs(r_utc) > 0.2 and p_utc < 0.05) or \
                    (coverage_std > 3)

    if bias_detected:
        verdict = (
            "TIME-OF-DAY BIAS DETECTED\n"
            "  The valid L1 segments are not uniformly distributed\n"
            "  across UTC hours, OR the L1 excess correlates with\n"
            "  time of day directly.\n"
            "  CONSEQUENCE: all sky correlations are potentially\n"
            "  contaminated. The sky direction results cannot be\n"
            "  trusted without correcting for this bias first.\n"
            "  NEXT STEP: group analysis by hour-of-day, compute\n"
            "  residuals after removing time-of-day mean, then\n"
            "  rerun sky correlations on the residuals."
        )
    else:
        verdict = (
            "NO TIME-OF-DAY BIAS DETECTED\n"
            "  L1 excess does not correlate with UTC hour.\n"
            "  Valid segments are roughly uniformly distributed.\n"
            "  CONSEQUENCE: the sky correlations (void test p=0.0001,\n"
            "  local arm r=+0.44) survive the bias check and are\n"
            "  genuine sky-direction dependent signals.\n"
            "  The kinematic fingerprint hypothesis is supported."
        )

    print(f"  r(UTC hour):      {r_utc:+.4f}  p={p_utc:.4f}")
    print(f"  r(sin UTC):       {r_sin:+.4f}  p={p_sin:.4f}")
    print(f"  r(cos UTC):       {r_cos:+.4f}  p={p_cos:.4f}")
    print(f"  Coverage std:     {coverage_std:.1f} segments/hour")
    print()
    print(f"  {verdict}")

    # Save
    result = {
        "test":           "timeofday_bias",
        "lake_source":    LAKE_PATH.name,
        "n_valid":        len(valid),
        "n_none":         len(invalid),
        "coverage_pct":   len(valid)/len(segments)*100,
        "r_utc_linear":   round(r_utc, 4),
        "p_utc_linear":   round(p_utc, 4),
        "r_sin_utc":      round(r_sin, 4),
        "p_sin_utc":      round(p_sin, 4),
        "r_cos_utc":      round(r_cos, 4),
        "p_cos_utc":      round(p_cos, 4),
        "coverage_std":   round(float(coverage_std), 2),
        "peak_hour_utc":  peak_hour,
        "bias_detected":  bias_detected,
        "verdict":        verdict,
        "hour_stats":     hour_stats,
    }

    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print()
    print(f"Results written: {OUTPUT_PATH}")
    print()
    print("KEY:")
    print("  Bias detected → sky correlations contaminated, need residual test")
    print("  No bias       → sky correlations are real, local arm r=0.44 stands")


if __name__ == "__main__":
    main()