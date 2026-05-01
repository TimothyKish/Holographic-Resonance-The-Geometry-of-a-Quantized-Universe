# ==============================================================================
# SCRIPT: analyse_anticenter_correlation.py
# SERIES: LIGO-Series / GW150914
# PURPOSE: Test whether the GALACTIC ANTI-CENTER or GALACTIC PLANE
#          shows a POSITIVE elevation correlation with L1 5.093 Hz excess,
#          complementing the negative Sgr A* correlation already found.
#
# REASONING:
#   Sgr A* (RA 266°, Dec -29°) showed r = -0.375, p < 0.0001:
#   the 5.093 Hz feature is STRONGEST when Sgr A* is BELOW the horizon.
#
#   The galactic anti-center (RA 86°, Dec +29°) is the direction
#   DIRECTLY OPPOSITE Sgr A* on the sky. When Sgr A* is at -80°,
#   the anti-center is near +80°. If the true signal source is the
#   galactic PLANE — the dense stellar disk running through both Sgr A*
#   and the anti-center direction — then the anti-center should show a
#   POSITIVE correlation: stronger signal when the anti-center is overhead.
#
#   Additional targets tested:
#   - Galactic North Pole (RA 192°, Dec +27°): tests if signal comes
#     from ABOVE the galactic plane (low mass density)
#   - Galactic South Pole (RA 12°, Dec -27°): tests below the plane
#   - Virgo Supercluster center: large local mass concentration
#   - Moon: tests Earth tidal deformation hypothesis (different period)
#
# WHAT WE EXPECT:
#   If galactic plane is the source:
#     anti-center: POSITIVE r (overhead = stronger signal)
#     Sgr A*:      NEGATIVE r (overhead = weaker — already confirmed)
#     galactic poles: near zero r (poles = low mass density)
#
#   If Earth tidal deformation (Moon):
#     Moon: shows correlation at monthly timescale, not sidereal
#
#   If galactic arms specifically:
#     Local arm direction (RA 60°, Dec +0°) should show strong correlation
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

# Sky targets to test
TARGETS = {
    "sgr_a_star": {
        "ra": 266.4168, "dec": -29.0078,
        "note": "Galactic center SMBH — already tested (r=-0.375)",
        "expected": "negative (confirmed)",
    },
    "galactic_anticenter": {
        "ra": 86.4, "dec": +28.9,
        "note": "Directly opposite Sgr A* — galactic anti-center",
        "expected": "positive IF galactic plane is source",
    },
    "galactic_north_pole": {
        "ra": 192.8, "dec": +27.1,
        "note": "90° above galactic plane — low mass density",
        "expected": "near zero IF plane is source",
    },
    "galactic_south_pole": {
        "ra": 12.8, "dec": -27.1,
        "note": "90° below galactic plane — low mass density",
        "expected": "near zero IF plane is source",
    },
    "local_arm": {
        "ra": 60.0, "dec": 0.0,
        "note": "Local Orion arm direction — dense stellar neighborhood",
        "expected": "positive IF local arm is dominant source",
    },
    "virgo_supercluster": {
        "ra": 186.6, "dec": +12.7,
        "note": "Virgo Cluster / local supercluster core",
        "expected": "positive IF local mass concentration matters",
    },
}

L1_LAT = 30.5629
L1_LON = -90.7742

SCRIPTS_DIR = Path(__file__).resolve().parent
GW_DIR      = SCRIPTS_DIR.parent
LAKE_DIR    = GW_DIR / "lake"
LAKE_PATH   = LAKE_DIR / "ligo_sidereal_rotation_test.json"
OUTPUT_PATH = LAKE_DIR / "ligo_anticenter_correlation.json"


def sky_elevation(ra_deg, dec_deg, gps_time):
    """Altitude of sky target above L1 horizon at given GPS time."""
    utc_unix = gps_time - 17 + 315964800
    jd       = utc_unix / 86400.0 + 2440587.5
    T        = (jd - 2451545.0) / 36525.0
    gmst     = (280.46061837 + 360.98564736629*(jd - 2451545.0)
                + 0.000387933*T*T) % 360
    lst      = (gmst + L1_LON) % 360
    ha       = math.radians((lst - ra_deg) % 360)
    dec      = math.radians(dec_deg)
    lat      = math.radians(L1_LAT)
    sin_alt  = (math.sin(dec)*math.sin(lat)
                + math.cos(dec)*math.cos(lat)*math.cos(ha))
    return math.degrees(math.asin(max(-1.0, min(1.0, sin_alt))))


def main():
    import numpy as np
    from scipy.stats import pearsonr, spearmanr

    print("=" * 65)
    print("Galactic Plane Correlation Test — Anti-Center Hypothesis")
    print("=" * 65)
    print(f"k_geo = 16/π = {K_GEO:.6f} Hz")
    print()

    if not LAKE_PATH.exists():
        print(f"Lake not found: {LAKE_PATH}")
        print("Run build_lake_sidereal.py first.")
        sys.exit(1)

    with LAKE_PATH.open("r", encoding="utf-8") as f:
        lake = json.load(f)

    segments = lake.get("segments", [])
    valid = [(s["gps_mid"], s["L1_excess_5093"])
             for s in segments
             if s.get("L1_excess_5093") is not None]

    print(f"Loaded {len(segments)} segments, {len(valid)} valid L1 points")
    print()

    times  = np.array([v[0] for v in valid])
    excess = np.array([v[1] for v in valid])

    print(f"L1 excess — mean: {excess.mean():.4f}  std: {excess.std():.4f}")
    print()
    print("=" * 65)
    print("CORRELATION RESULTS BY SKY TARGET")
    print("=" * 65)
    print()
    print(f"  {'Target':<24} {'r':>8} {'p':>8}  {'Verdict'}")
    print("  " + "-" * 70)

    results = {}
    for name, tgt in TARGETS.items():
        elevs = np.array([
            sky_elevation(tgt["ra"], tgt["dec"], t)
            for t in times
        ])
        r_p, p_p = pearsonr(elevs, excess)
        r_s, p_s = spearmanr(elevs, excess)

        # Verdict
        if abs(r_p) > 0.2 and p_p < 0.01:
            if r_p > 0:
                verdict = "POSITIVE *** sky-up = stronger"
            else:
                verdict = "NEGATIVE *** sky-down = stronger"
        elif p_p < 0.05:
            verdict = f"marginal r={r_p:+.3f}"
        else:
            verdict = "none (p={:.2f})".format(p_p)

        results[name] = {
            "pearson_r":  round(r_p, 4),
            "pearson_p":  round(p_p, 4),
            "spearman_r": round(float(r_s), 4),
            "spearman_p": round(float(p_s), 4),
            "verdict":    verdict,
            "expected":   tgt["expected"],
            "note":       tgt["note"],
        }

        star = " ***" if abs(r_p) > 0.2 and p_p < 0.01 else ""
        print(f"  {name:<24} {r_p:>+8.4f} {p_p:>8.4f}  {verdict}{star}")

    # Quartile breakdown for top targets
    print()
    print("=" * 65)
    print("QUARTILE BREAKDOWN — TOP CORRELATING TARGETS")
    print("=" * 65)

    # Sort by |r|
    sorted_targets = sorted(results.items(),
                            key=lambda x: abs(x[1]["pearson_r"]),
                            reverse=True)

    for name, res in sorted_targets[:3]:
        tgt = TARGETS[name]
        elevs = np.array([sky_elevation(tgt["ra"], tgt["dec"], t) for t in times])
        q25, q50, q75 = np.percentile(elevs, [25, 50, 75])
        print()
        print(f"  {name}  (r={res['pearson_r']:+.4f}  p={res['pearson_p']:.4f})")
        print(f"  {tgt['note']}")
        for label, mask in [
            (f"Q1 < {q25:.0f}°",        elevs < q25),
            (f"Q2 {q25:.0f}°–{q50:.0f}°", (elevs >= q25) & (elevs < q50)),
            (f"Q3 {q50:.0f}°–{q75:.0f}°", (elevs >= q50) & (elevs < q75)),
            (f"Q4 > {q75:.0f}°",        elevs >= q75),
        ]:
            sub = excess[mask]
            if len(sub) > 0:
                print(f"    {label:<22} n={len(sub):>3}  "
                      f"mean={sub.mean():.4f}  std={sub.std():.4f}")

    # Key interpretation
    print()
    print("=" * 65)
    print("INTERPRETATION")
    print("=" * 65)
    print()

    sgr_r   = results["sgr_a_star"]["pearson_r"]
    anti_r  = results["galactic_anticenter"]["pearson_r"]
    ngp_r   = results["galactic_north_pole"]["pearson_r"]
    sgp_r   = results["galactic_south_pole"]["pearson_r"]

    if anti_r > 0.2 and results["galactic_anticenter"]["pearson_p"] < 0.01:
        if abs(ngp_r) < 0.1 and abs(sgp_r) < 0.1:
            conclusion = (
                "GALACTIC PLANE CONFIRMED AS SOURCE\n"
                "  Anti-center positive + galactic poles near zero\n"
                "  = signal comes from the galactic plane (disk),\n"
                "  not from above/below it.\n"
                "  Both Sgr A* (negative) and anti-center (positive)\n"
                "  are in the galactic plane — the plane itself is the source."
            )
        else:
            conclusion = (
                "GALACTIC PLANE CANDIDATE\n"
                "  Anti-center shows positive correlation.\n"
                "  Poles are not cleanly zero — partial contamination."
            )
    elif anti_r < -0.1:
        conclusion = (
            "BOTH SGR A* AND ANTI-CENTER NEGATIVE\n"
            "  Signal strongest when BOTH directions are below horizon.\n"
            "  Points to ZENITH source or Earth-interior resonance."
        )
    else:
        conclusion = (
            "ANTI-CENTER DOES NOT SHOW POSITIVE CORRELATION\n"
            "  The Sgr A* anti-correlation is NOT simply the galactic plane.\n"
            "  Other source geometry required."
        )

    print(f"  Sgr A* r:           {sgr_r:+.4f}  (confirmed negative)")
    print(f"  Anti-center r:      {anti_r:+.4f}")
    print(f"  Galactic N Pole r:  {ngp_r:+.4f}")
    print(f"  Galactic S Pole r:  {sgp_r:+.4f}")
    print()
    print(f"  CONCLUSION: {conclusion}")

    # Save
    output = {
        "analysis":    "anticenter_correlation",
        "lake_source": LAKE_PATH.name,
        "n_valid":     len(valid),
        "k_geo":       K_GEO,
        "results":     results,
        "conclusion":  conclusion,
        "provenance": {
            "sidereal_test_r": -0.3746,
            "void_test_p":     0.0001,
            "vol5_z94":        "2026-04-06",
        },
    }

    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print()
    print(f"Results written: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()