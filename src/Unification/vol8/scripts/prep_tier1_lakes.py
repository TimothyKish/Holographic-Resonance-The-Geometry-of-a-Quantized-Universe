# ==============================================================================
# SCRIPT: prep_tier1_lakes.py
# PURPOSE: Check what fields exist in your current raw lakes, then tell you
#          exactly what to do next for each Tier 1 new lake.
#
# RUN THIS FIRST before any build scripts.
# It checks your existing data and gives you precise next steps.
#
# USAGE:
#   cd vol8/scripts
#   python prep_tier1_lakes.py
# ==============================================================================

import json
import math
from pathlib import Path

PI    = math.pi
K_GEO = 16.0 / PI

# Paths relative to vol8 root
VOL8 = Path(__file__).resolve().parent.parent

S2_RAW = VOL8 / "S-Series" / "S2_StellarKinematics" / "lake" / "s2_stellar_kinematics_raw.jsonl"
G1_RAW = VOL8 / "G-Series" / "G1_GalaxyKinematics"  / "lake" / "g1_galaxy_kinematics_raw.jsonl"

S3_DEST = VOL8 / "S-Series" / "S3_GalacticNASA"      / "lake" / "s3_gaia_luminosity_raw.jsonl"
S4_DEST = VOL8 / "S-Series" / "S4_AstroMaster"       / "lake" / "s4_gaia_colour_raw.jsonl"
G2_DEST = VOL8 / "G-Series" / "G2_GalaxyLuminosity"  / "lake" / "g2_sdss_luminosity_raw.jsonl"
G3_DEST = VOL8 / "G-Series" / "G3_GalaxyColour"      / "lake" / "g3_sdss_colour_raw.jsonl"


def peek_fields(path: Path, n: int = 3) -> dict:
    """Read first n records and return the union of all fields seen."""
    all_fields = set()
    records = []
    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= n:
                break
            try:
                rec = json.loads(line.strip())
                all_fields.update(rec.keys())
                records.append(rec)
            except json.JSONDecodeError:
                continue
    return {"fields": sorted(all_fields), "sample": records}


def check_field(records: list, field: str) -> bool:
    return any(field in r and r[field] is not None for r in records)


def extract_and_copy(src: Path, dest: Path, needed_fields: list):
    """
    If src records already contain the needed fields,
    copy them to dest (keeping only needed + identity fields).
    Returns number of records written.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with src.open("r", encoding="utf-8") as fin, \
         dest.open("w", encoding="utf-8") as fout:
        for line in fin:
            try:
                rec = json.loads(line.strip())
                out = {f: rec.get(f) for f in needed_fields if f in rec}
                if len(out) == len(needed_fields):
                    fout.write(json.dumps(out) + "\n")
                    n += 1
            except json.JSONDecodeError:
                continue
    return n


print()
print("=" * 65)
print("TIER 1 LAKE PREPARATION CHECK")
print("=" * 65)

# ─── CHECK S2 (Gaia stellar kinematics) ───────────────────────────────────
print()
print("Checking S2 Gaia raw file...")

if not S2_RAW.exists():
    print(f"  NOT FOUND: {S2_RAW}")
    print("  The S2 raw file is missing from this location.")
    print("  Check your LARGE_FILE_DOWNLOAD.md for the Google Drive link.")
else:
    info = peek_fields(S2_RAW)
    fields = info["fields"]
    sample = info["sample"]
    print(f"  Found. Fields in S2 raw: {fields}")
    print()

    has_mag   = check_field(sample, "phot_g_mean_mag")
    has_bprp  = check_field(sample, "bp_rp")
    has_plx   = check_field(sample, "parallax")

    # ── S3: Gaia Luminosity ──────────────────────────────────────────────
    print("  S3 (Gaia Luminosity) needs: phot_g_mean_mag + parallax")
    if has_mag and has_plx:
        print("  STATUS: ✓ Fields present in S2 raw.")
        print("  ACTION: Extracting to S3 location now...")
        n = extract_and_copy(S2_RAW, S3_DEST,
                             ["source_id", "ra", "dec",
                              "parallax", "phot_g_mean_mag", "ruwe"])
        print(f"  Done. {n:,} records written to:")
        print(f"  {S3_DEST}")
        print(f"  Next: python S-Series/S3_GalacticNASA/scripts/build_s3_gaia_luminosity_lake.py --litmus")
    else:
        print("  STATUS: ✗ phot_g_mean_mag NOT in S2 raw.")
        print()
        print("  ┌─────────────────────────────────────────────────────┐")
        print("  │  REQUIRED ACTION: Re-run your Gaia query adding     │")
        print("  │  one column. Use the ADQL below at:                 │")
        print("  │  https://gea.esac.esa.int/tap-server/tap-server     │")
        print("  │  (Gaia Archive → TAP → ADQL query)                  │")
        print("  └─────────────────────────────────────────────────────┘")
        print()
        print("  ADQL QUERY (paste exactly):")
        print("  ─────────────────────────────────────────────────────")
        print("  SELECT source_id, ra, dec, parallax, parallax_error,")
        print("         pmra, pmdec, phot_g_mean_mag, bp_rp, ruwe")
        print("  FROM gaiadr3.gaia_source")
        print("  WHERE parallax > 0")
        print("    AND parallax_over_error > 10")
        print("    AND ruwe < 1.4")
        print("    AND phot_g_mean_mag IS NOT NULL")
        print("  LIMIT 2000000")
        print()
        print("  SAVE AS:")
        print(f"  {S3_DEST}")
        print()
        print("  NOTE: This same download also provides S4 (colour).")
        print("  bp_rp is included in the query — you get both lakes")
        print("  from one download.")
        print()

    # ── S4: Gaia Colour ──────────────────────────────────────────────────
    print()
    print("  S4 (Gaia Colour) needs: bp_rp + parallax")
    if has_bprp and has_plx:
        print("  STATUS: ✓ Fields present in S2 raw.")
        print("  ACTION: Extracting to S4 location now...")
        n = extract_and_copy(S2_RAW, S4_DEST,
                             ["source_id", "ra", "dec", "parallax", "bp_rp"])
        print(f"  Done. {n:,} records written to:")
        print(f"  {S4_DEST}")
        print(f"  Next: python S-Series/S4_AstroMaster/scripts/build_s4_gaia_colour_lake.py --litmus")
    elif has_mag or has_bprp:
        print("  STATUS: Partial — run the query above (bp_rp is already")
        print("  included) and both S3 and S4 raw files will be ready.")
    else:
        print("  STATUS: Will be ready after the Gaia re-query above.")
        print("  bp_rp is already in the ADQL query shown above.")


# ─── CHECK G1 (SDSS galaxy kinematics) ────────────────────────────────────
print()
print()
print("Checking G1 SDSS raw file...")

if not G1_RAW.exists():
    print(f"  NOT FOUND: {G1_RAW}")
    print("  Check your LARGE_FILE_DOWNLOAD.md for the Google Drive link.")
else:
    info = peek_fields(G1_RAW)
    fields = info["fields"]
    sample = info["sample"]
    print(f"  Found. Fields in G1 raw: {fields}")
    print()

    has_r   = check_field(sample, "modelMag_r")
    has_ur  = check_field(sample, "modelMag_u") or check_field(sample, "u_minus_r")
    has_z   = check_field(sample, "z")

    # ── G2: SDSS Luminosity ───────────────────────────────────────────────
    print("  G2 (SDSS Luminosity) needs: modelMag_r + z (redshift)")
    if has_r and has_z:
        print("  STATUS: ✓ Fields present in G1 raw!")
        print("  ACTION: Extracting to G2 location now...")
        n = extract_and_copy(G1_RAW, G2_DEST,
                             ["specobjid", "ra", "dec", "z",
                              "veldisp", "modelMag_r"])
        print(f"  Done. {n:,} records written to:")
        print(f"  {G2_DEST}")
        print(f"  Next: python G-Series/G2_GalaxyLuminosity/scripts/build_g2_sdss_luminosity_lake.py --litmus")
    else:
        print("  STATUS: ✗ modelMag_r NOT in G1 raw.")
        print()
        print("  ┌─────────────────────────────────────────────────────┐")
        print("  │  REQUIRED ACTION: Re-run your SDSS query adding     │")
        print("  │  two columns. Use SDSS CasJobs at:                  │")
        print("  │  https://skyserver.sdss.org/casjobs/                │")
        print("  └─────────────────────────────────────────────────────┘")
        print()
        print("  SQL QUERY (paste into CasJobs, context = DR16):")
        print("  ─────────────────────────────────────────────────────")
        print("  SELECT s.specobjid, s.ra, s.dec, s.z,")
        print("         s.veldisp, s.veldisperr,")
        print("         p.modelMag_r, p.modelMag_u,")
        print("         p.modelMagErr_r")
        print("  INTO mydb.G2_luminosity")
        print("  FROM SpecObj AS s")
        print("  JOIN PhotoObj AS p ON s.bestobjid = p.objid")
        print("  WHERE s.class = 'GALAXY'")
        print("    AND s.zWarning = 0")
        print("    AND s.z BETWEEN 0.01 AND 0.3")
        print("    AND s.veldisp > 0")
        print("    AND p.modelMag_r BETWEEN 10.0 AND 22.0")
        print()
        print("  EXPORT as JSON, convert to JSONL, save as:")
        print(f"  {G2_DEST}")
        print()
        print("  NOTE: modelMag_u is included so G3 (colour) also works.")
        print("  u - r colour = modelMag_u - modelMag_r")
        print("  One SDSS query provides both G2 and G3.")

    # ── G3: SDSS Colour ───────────────────────────────────────────────────
    print()
    print("  G3 (SDSS Colour) needs: modelMag_u + modelMag_r + z")
    if has_ur and has_r and has_z:
        print("  STATUS: ✓ Fields present in G1 raw.")
        print("  Extracting to G3 location now...")
        n = extract_and_copy(G1_RAW, G3_DEST,
                             ["specobjid", "ra", "dec", "z",
                              "veldisp", "modelMag_u", "modelMag_r"])
        print(f"  Done. {n:,} records written to: {G3_DEST}")
    else:
        print("  STATUS: Will be ready after the SDSS re-query above.")
        print("  modelMag_u is already in the SQL query shown above.")


# ─── SUMMARY ──────────────────────────────────────────────────────────────
print()
print()
print("=" * 65)
print("SUMMARY — WHAT TO DO NEXT")
print("=" * 65)
print()
print("1. If any STATUS showed ✗:")
print("   Run the query shown for that source (Gaia or SDSS).")
print("   Save the result to the path shown.")
print("   Then re-run this script — it will extract automatically.")
print()
print("2. Once all STATUS show ✓, run in order:")
print()
print("   S3:")
print("   cd vol8/S-Series/S3_GalacticNASA/scripts")
print("   python build_s3_gaia_luminosity_lake.py --litmus")
print("   python build_s3_gaia_luminosity_lake.py")
print()
print("   S4:")
print("   cd vol8/S-Series/S4_AstroMaster/scripts")
print("   python build_s4_gaia_colour_lake.py --litmus")
print("   python build_s4_gaia_colour_lake.py")
print()
print("   G2:")
print("   cd vol8/G-Series/G2_GalaxyLuminosity/scripts")
print("   python build_g2_sdss_luminosity_lake.py --litmus")
print("   python build_g2_sdss_luminosity_lake.py")
print()
print("   G3:")
print("   cd vol8/G-Series/G3_GalaxyColour/scripts")
print("   python build_g3_sdss_colour_lake.py --litmus")
print("   python build_g3_sdss_colour_lake.py")
print()
print("3. Add the volumes.json entries printed by each build script.")
print()
print("4. Run the pipeline:")
print("   cd vol8/scripts")
print("   python scalarize.py")
print("   python unify.py")
print("   python build_chaos_nulls.py    <- overnight")
print("   python build_pinch_table.py    <- overnight")
print()
print("That is the complete sequence. Run this script first.")
print("It will tell you exactly what is missing and what to do.")