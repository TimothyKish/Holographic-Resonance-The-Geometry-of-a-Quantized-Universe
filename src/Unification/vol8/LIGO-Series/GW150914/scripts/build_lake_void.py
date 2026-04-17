# ==============================================================================
# SCRIPT: build_lake_void.py
# SERIES: LIGO-Series / GW150914
# PURPOSE: Test whether L1's 5.093 Hz elevation is mass-density dependent
#          by comparing L1 data when its antenna points toward a cosmic void
#          versus when it points toward a mass-dense sky region.
#
# THE HYPOTHESIS:
#   If 5.093 Hz (k_geo = 16/π) is the kinematic fingerprint of mass,
#   then the L1 elevation at that frequency should be LOWER when L1's
#   sensitivity is directed toward a region of near-zero mass density
#   (a cosmic void) compared to a region of high mass density.
#
# VOID vs MASS TARGET:
#   VOID:   Boötes Void — one of the largest known cosmic voids
#           RA 14h 50m (222.5°)  Dec +46°
#           Diameter ~330 million light years of near-empty space
#           ~60 galaxies where there should be ~2000
#
#   MASS:   Virgo Cluster — nearest rich galaxy cluster to Milky Way
#           RA 12h 27m (186.6°)  Dec +12.7°
#           ~1300 confirmed galaxies, M87 supergiant elliptical at center
#           Virgo A black hole mass: 6.5 billion solar masses
#
#   CONTROL: Galactic Center (Sgr A*)
#           RA 17h 45m (266.4°)  Dec -29°
#           4 million solar mass SMBH, 26,000 light years
#
# PROTOCOL:
#   L1's sensitivity pattern rotates with Earth (sidereal period).
#   We compute which sky direction L1 is most sensitive to at each GPS time,
#   then select data segments where L1 is pointing toward the void
#   vs toward the Virgo Cluster.
#   For each group, compute mean whitened 5.093 Hz excess.
#   If void < mass-dense: mass-density dependent — kinematic fingerprint
#   If void ≈ mass-dense: not mass-dependent — site noise
#
# DATA:
#   LIGO O1 science run. Using 7 days of quiet data:
#   GPS 1129200000 to 1129804800 (~7 days, ~1 week before GW150914)
#
# AUTHORS: Timothy John Kish & Mondy
# PROVENANCE:
#   Ghost notes observed 2026-01-08 (Lyra Aurora Kish & Timothy Kish)
#   KRG published 2026-01-14 (DOI: 10.5281/zenodo.18245148)
#   Vol5 z=94 kinematic confirmation 2026-04-06
#   Void hypothesis formulated 2026-04-07
# AUDIT: mondy_verified_2026-04
# ==============================================================================

import json
import math
import sys
import time
from pathlib import Path

PI    = math.pi
K_GEO = 16.0 / PI

GHOST_F1  = K_GEO
GHOST_TOL = 0.20

# Sky targets
TARGETS = {
    "bootes_void": {
        "ra_deg":  222.5,
        "dec_deg": +46.0,
        "note":    "Boötes Void — 330Mly diameter, ~60 galaxies where ~2000 expected",
        "type":    "void",
    },
    "virgo_cluster": {
        "ra_deg":  186.6,
        "dec_deg": +12.7,
        "note":    "Virgo Cluster — nearest rich cluster, M87/Virgo A 6.5B solar masses",
        "type":    "mass_dense",
    },
    "sgr_a_star": {
        "ra_deg":  266.4,
        "dec_deg": -29.0,
        "note":    "Sgr A* — Milky Way SMBH, 4M solar masses",
        "type":    "mass_dense",
    },
    "eridanus_void": {
        "ra_deg":  51.0,
        "dec_deg": -20.0,
        "note":    "Eridanus Void — large underdensity south of equator",
        "type":    "void",
    },
}

# L1 site
L1_LAT = 30.5629
L1_LON = -90.7742

# 7 days of quiet O1
GPS_START = 1129200000
GPS_DAYS  = 7
GPS_END   = GPS_START + GPS_DAYS * 86400
SEGMENT_S = 900    # 15 min
FFTLENGTH = 4.0

# Elevation threshold: target must be above 20° to count as "pointing toward"
ELEVATION_THRESHOLD = 20.0

SCRIPTS_DIR = Path(__file__).resolve().parent
GW_DIR      = SCRIPTS_DIR.parent
OUTPUT_DIR  = GW_DIR / "lake"
OUTPUT_PATH = OUTPUT_DIR / "ligo_void_control.json"


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


def sky_elevation_at_gps(ra_deg, dec_deg, gps_time, lat_deg, lon_deg):
    """Compute altitude of sky target above horizon at given GPS time."""
    utc_unix = gps_time - 17 + 315964800
    jd       = utc_unix / 86400.0 + 2440587.5
    T        = (jd - 2451545.0) / 36525.0
    gmst_deg = (280.46061837 + 360.98564736629 * (jd - 2451545.0)
                + 0.000387933 * T * T) % 360
    lst_deg  = (gmst_deg + lon_deg) % 360
    ha_rad   = math.radians((lst_deg - ra_deg) % 360)
    dec_rad  = math.radians(dec_deg)
    lat_rad  = math.radians(lat_deg)
    sin_alt  = (math.sin(dec_rad) * math.sin(lat_rad)
                + math.cos(dec_rad) * math.cos(lat_rad) * math.cos(ha_rad))
    return round(math.degrees(math.asin(max(-1, min(1, sin_alt)))), 2)


def download_segment(detector, gps_start, gps_end, retries=2):
    from gwpy.timeseries import TimeSeries
    for attempt in range(retries):
        try:
            ts = TimeSeries.fetch_open_data(
                detector, gps_start, gps_end,
                sample_rate=4096, verbose=False
            )
            return ts
        except Exception:
            if attempt < retries - 1:
                time.sleep(2)
    return None


def get_excess(strain, freq, fftlen=FFTLENGTH, tol=GHOST_TOL):
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


def main():
    print("=" * 65)
    print("LIGO Void Control Test — k_geo Mass-Density Dependence")
    print("=" * 65)
    print(f"k_geo = 16/π = {K_GEO:.6f} Hz")
    print()
    print("Targets:")
    for name, t in TARGETS.items():
        print(f"  {name:<20} RA {t['ra_deg']:>6.1f}°  Dec {t['dec_deg']:>+6.1f}°  "
              f"[{t['type']}]")
    print()
    print(f"Elevation threshold: {ELEVATION_THRESHOLD}°")
    print(f"Analysing {GPS_DAYS} days = "
          f"{int(GPS_DAYS * 86400 / SEGMENT_S)} segments")
    print()

    if not check_dependencies():
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    n_segs   = int(GPS_DAYS * 86400 / SEGMENT_S)
    segments = []

    print("Processing segments...")
    for i in range(n_segs):
        t0    = GPS_START + i * SEGMENT_S
        t1    = t0 + SEGMENT_S
        t_mid = (t0 + t1) / 2

        # Elevation of each target at this time
        elevations = {}
        for name, tgt in TARGETS.items():
            elev = sky_elevation_at_gps(
                tgt["ra_deg"], tgt["dec_deg"], t_mid, L1_LAT, L1_LON
            )
            elevations[name] = elev

        # Determine which category this segment belongs to
        pointing = []
        for name, elev in elevations.items():
            if elev > ELEVATION_THRESHOLD:
                pointing.append((name, TARGETS[name]["type"], elev))

        # Download L1
        l1 = download_segment("L1", t0, t1)
        l1_ex = get_excess(l1, GHOST_F1) if l1 is not None else None

        seg = {
            "segment":      i,
            "gps_mid":      t_mid,
            "L1_excess":    l1_ex,
            "elevations":   elevations,
            "pointing_at":  pointing,
        }
        segments.append(seg)

        if (i + 1) % 20 == 0:
            above = [f"{p[0]}({p[2]:.0f}°)" for p in pointing]
            print(f"  Seg {i+1:>4}/{n_segs}  L1_ex={str(l1_ex):>6}  "
                  f"above threshold: {above if above else 'none'}")

    # Group segments by sky category
    void_excess    = []
    mass_excess    = []
    neutral_excess = []

    for seg in segments:
        ex = seg["L1_excess"]
        if ex is None:
            continue
        types_above = set(p[1] for p in seg["pointing_at"])
        if "void" in types_above and "mass_dense" not in types_above:
            void_excess.append(ex)
        elif "mass_dense" in types_above and "void" not in types_above:
            mass_excess.append(ex)
        else:
            neutral_excess.append(ex)

    import numpy as np

    print()
    print("=" * 65)
    print("VOID vs MASS-DENSE COMPARISON — L1 5.093 Hz whitened excess")
    print("=" * 65)
    print()

    def stats(lst, label):
        if not lst:
            print(f"  {label:<25} No data")
            return
        a = np.array(lst)
        print(f"  {label:<25} n={len(lst):>4}  "
              f"mean={a.mean():.4f}  std={a.std():.4f}  "
              f"min={a.min():.4f}  max={a.max():.4f}")

    stats(void_excess,    "VOID segments")
    stats(mass_excess,    "MASS-DENSE segments")
    stats(neutral_excess, "NEUTRAL segments")

    print()

    if void_excess and mass_excess:
        from scipy.stats import ttest_ind, mannwhitneyu
        v = np.array(void_excess)
        m = np.array(mass_excess)
        t_stat, t_pval = ttest_ind(v, m)
        u_stat, u_pval = mannwhitneyu(v, m, alternative='two-sided')

        print(f"  Student t-test:       t={t_stat:.3f}  p={t_pval:.4f}")
        print(f"  Mann-Whitney U test:  U={u_stat:.0f}  p={u_pval:.4f}")
        print()

        mean_void = np.mean(v)
        mean_mass = np.mean(m)
        if mean_mass > mean_void * 1.2 and t_pval < 0.05:
            verdict = (f"MASS-DENSITY DEPENDENT — mass-dense {mean_mass:.3f}x "
                       f"vs void {mean_void:.3f}x  (p={t_pval:.4f})")
        elif t_pval > 0.05:
            verdict = "NOT MASS-DENSITY DEPENDENT — no significant difference"
        else:
            verdict = f"MARGINAL — difference exists but small"

        print(f"  VERDICT: {verdict}")
    else:
        verdict = "INSUFFICIENT DATA — not enough void or mass segments"
        print(f"  {verdict}")

    # Per-target mean excess
    print()
    print("  Per-target mean L1 excess when target > 20° elevation:")
    for name, tgt in TARGETS.items():
        segs_with_target = [s["L1_excess"] for s in segments
                            if s["L1_excess"] is not None
                            and s["elevations"].get(name, -99) > ELEVATION_THRESHOLD]
        if segs_with_target:
            mean_ex = np.mean(segs_with_target)
            print(f"    {name:<22} [{tgt['type']:<11}] "
                  f"mean={mean_ex:.4f}  n={len(segs_with_target)}")
        else:
            print(f"    {name:<22} [{tgt['type']:<11}] no data above threshold")

    # Write lake
    result = {
        "test":       "void_control",
        "ghost_f1":   GHOST_F1,
        "k_geo":      K_GEO,
        "gps_start":  GPS_START,
        "gps_end":    GPS_END,
        "n_segments": n_segs,
        "elevation_threshold_deg": ELEVATION_THRESHOLD,
        "targets":    TARGETS,
        "summary": {
            "void_n":         len(void_excess),
            "void_mean":      float(np.mean(void_excess)) if void_excess else None,
            "mass_n":         len(mass_excess),
            "mass_mean":      float(np.mean(mass_excess)) if mass_excess else None,
            "verdict":        verdict,
        },
        "protocol": (
            "15-min whitened PSD segments. L1 segments classified by which "
            "sky target is above 20° elevation. Void mean vs mass-dense mean "
            "compared with t-test and Mann-Whitney U. "
            "If mass_mean > void_mean with p<0.05: mass-density dependent."
        ),
        "provenance": {
            "ghost_notes_observed": "2026-01-08 Lyra Aurora Kish & Timothy Kish",
            "krg_doi":  "10.5281/zenodo.18245148",
            "vol5_z94": "2026-04-06",
            "void_test_formulated": "2026-04-07",
        },
        "segments": segments,
    }

    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print()
    print(f"Lake written: {OUTPUT_PATH}")
    print()
    print("KEY:")
    print("  mass_mean > void_mean, p < 0.05 → mass-density dependent")
    print("  mass_mean ≈ void_mean            → not mass-dependent (site noise)")
    print("  Per-target: compare Virgo/SgrA* vs Boötes/Eridanus directly")


if __name__ == "__main__":
    main()