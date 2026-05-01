# ==============================================================================
# SCRIPT: build_biology_scalars.py
# TARGET: Compute geometric scalar invariants for B3 (amino) and B1 (chirality)
#         promoted lakes and write scalar_invariant into _raw_payload
#
# SCALARIZATION:
#   B3 Amino:    scalar = N-Cα-C backbone bond angle (radians, unsigned)
#                Range: ~1.84 - 1.96 rad (105-112 degrees)
#                Chirality-independent. Varies per amino acid geometry.
#
#   B1 Chirality: scalar = sign(N-Cα-C-O dihedral) * bond_angle (radians, signed)
#                 L-amino acids: negative (~-1.88)
#                 D-amino acids: positive (~+1.88)
#                 Clearly separates enantiomers.
#
# BACKBONE IDENTIFICATION:
#   N  = amine nitrogen (first N in coords list)
#   Cα = carbon closest to N
#   Cc = carboxyl carbon (C minimizing sum of distances to both O atoms)
#   O  = first oxygen (for dihedral)
#
# PROVENANCE: PubChem 3D conformer data (coords in Angstroms)
# AUTHORS: Timothy John Kish & Mondy
# AUDIT STATUS: mondy_verified_2026-04
# PENDING: Null lake (D-amino scramble) required before Vol5 promotion
# ==============================================================================

import json
import math
from pathlib import Path

# --------------------------------------------------------------------
# Configuration — paths relative to script location
# Script lives at: B-Series/B1_Biology/scripts/
# Raw lakes live at: B-Series/B3_Biology/lake/ and B-Series/B1_Biology/lake/
# Promoted output goes to: vol5/lakes/inputs_promoted/
# --------------------------------------------------------------------

SCRIPTS_DIR = Path(__file__).resolve().parent          # B1_Biology/scripts/
B_SERIES    = SCRIPTS_DIR.parents[1]                   # B-Series/
VOL5_ROOT   = B_SERIES.parent                          # vol5/
PROMOTED    = VOL5_ROOT / "lakes" / "inputs_promoted"

# Raw lake inputs (flat format: coords at top level)
B3_INPUT  = B_SERIES / "B3_Biology" / "lake" / "b3_amino.jsonl"
B1_INPUT  = B_SERIES / "B1_Biology" / "lake" / "b1_chirality.jsonl"

# Outputs: write directly to inputs_promoted, replacing old zero-scalar files
B3_OUTPUT = PROMOTED / "b3_amino_promoted.jsonl"
B1_OUTPUT = PROMOTED / "b1_chirality_promoted.jsonl"

# --------------------------------------------------------------------
# Vector math (no numpy dependency)
# --------------------------------------------------------------------

def vsub(a, b):
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def dot(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def norm(a):
    return math.sqrt(dot(a, a))

def cross(a, b):
    return (
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0]
    )

def bond_angle_rad(p1, vertex, p2):
    """Unsigned bond angle at vertex, in radians."""
    v1 = vsub(p1, vertex)
    v2 = vsub(p2, vertex)
    cos_a = dot(v1, v2) / (norm(v1) * norm(v2))
    return math.acos(max(-1.0, min(1.0, cos_a)))

def dihedral_rad(p1, p2, p3, p4):
    """Signed dihedral angle p1-p2-p3-p4, in radians. Range: (-pi, pi)."""
    b1 = vsub(p2, p1)
    b2 = vsub(p3, p2)
    b3 = vsub(p4, p3)
    n1 = cross(b1, b2)
    n2 = cross(b2, b3)
    m1 = cross(n1, b2)
    x = dot(n1, n2) / (norm(n1) * norm(n2))
    y = dot(m1, n2) / (norm(m1) * norm(n2))
    return math.atan2(y, x)

# --------------------------------------------------------------------
# Backbone identification
# --------------------------------------------------------------------

def find_backbone(coords):
    """
    Identify N, Cα, Cc, O from raw coord list.
    Returns (N, Cα, Cc, O) as (x,y,z) tuples, or None on failure.

    Strategy:
      N  = first nitrogen in coords (amine N)
      Cα = carbon closest to N
      Cc = carbon minimising sum of distances to the two nearest oxygens
      O  = oxygen closest to Cc (for dihedral)
    """
    by_type = {}
    for a in coords:
        by_type.setdefault(a['atom'], []).append((a['x'], a['y'], a['z']))

    ns = by_type.get('N', [])
    cs = by_type.get('C', [])
    os = by_type.get('O', [])

    if not ns or len(cs) < 2 or len(os) < 2:
        return None, None, None, None

    N_pos = ns[0]

    # Cα: C closest to N
    Ca = min(cs, key=lambda c: norm(vsub(c, N_pos)))

    # Cc: C closest to both oxygens (carboxyl carbon)
    O1, O2 = os[0], os[1]
    Cc = min(cs, key=lambda c: norm(vsub(c, O1)) + norm(vsub(c, O2)))

    # Guard: Cα and Cc must be different atoms
    if Ca == Cc:
        # Fall back: second-closest C to N
        cs_sorted = sorted(cs, key=lambda c: norm(vsub(c, N_pos)))
        if len(cs_sorted) < 2:
            return None, None, None, None
        Ca = cs_sorted[0]
        Cc = cs_sorted[1]

    # O: oxygen closest to Cc
    O_pos = min(os, key=lambda o: norm(vsub(o, Cc)))

    return N_pos, Ca, Cc, O_pos

# --------------------------------------------------------------------
# Scalar computation
# --------------------------------------------------------------------

def compute_b3_scalar(coords):
    """
    B3 Amino: unsigned N-Cα-C backbone bond angle in radians.
    Returns float or None if backbone not found.
    """
    N, Ca, Cc, O = find_backbone(coords)
    if N is None:
        return None
    return bond_angle_rad(N, Ca, Cc)

def compute_b1_scalar(coords):
    """
    B1 Chirality: sign(N-Cα-C-O dihedral) * backbone bond angle.
    L-amino: negative, D-amino: positive.
    Returns float or None if backbone not found.
    """
    N, Ca, Cc, O = find_backbone(coords)
    if N is None:
        return None
    angle = bond_angle_rad(N, Ca, Cc)
    dih   = dihedral_rad(N, Ca, Cc, O)
    return math.copysign(angle, dih)

# --------------------------------------------------------------------
# Lake processor
# --------------------------------------------------------------------

def process_lake(input_path, output_path, scalar_fn, lake_label, lake_id, domain):
    """
    Reads raw lake format (coords at top level of each record).
    Computes scalar and writes V5-compliant promoted record to output_path.

    Raw format:  {"cid": ..., "name": ..., "coords": [...], "_raw_payload": {}}
    Output format: full V5 promoted record with scalar_kls/klc set.
    """
    import uuid
    from datetime import datetime, timezone

    if not input_path.exists():
        print(f"[WARN] Input not found, skipping: {input_path}")
        print(f"  Expected: {input_path}")
        return 0, 0

    total = 0
    computed = 0
    failed = 0
    now_ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with input_path.open('r', encoding='utf-8') as fin, \
         output_path.open('w', encoding='utf-8') as fout:

        for line in fin:
            line = line.strip()
            if not line:
                continue
            total += 1
            raw_rec = json.loads(line)

            # Coords live at top level in raw format
            coords = raw_rec.get('coords')

            scalar = None
            if coords:
                scalar = scalar_fn(coords)

            if scalar is not None:
                computed += 1
            else:
                failed += 1
                scalar = 0.0

            # Store scalar_invariant back into raw payload
            raw_rec['scalar_invariant'] = scalar

            # Build V5-compliant promoted record
            promoted = {
                "entity_id":   str(uuid.uuid4()),
                "domain":      domain,
                "volume":      5,
                "lake_id":     lake_id,
                "geometry_payload": {
                    "coordinates":    [],
                    "dimensionality": 0,
                    "geometry_type":  "unknown",
                },
                "scalar_kls":  scalar,
                "scalar_klc":  scalar,
                "meta": {
                    "source":            f"PubChem 3D conformer data ({input_path.name})",
                    "ingest_timestamp":  now_ts,
                    "sovereign":         True,
                    "audit_status":      "mondy_verified_2026-04",
                    "scalarization":     "N-Ca-C backbone bond angle (rad)" if scalar >= 0
                                         else "sign(dihedral)*bond_angle (rad, chirality)",
                },
                "_raw_payload": raw_rec,
            }

            fout.write(json.dumps(promoted, ensure_ascii=False) + '\n')

    print(f"[{lake_label}] total={total}, computed={computed}, failed={failed}")
    if computed > 0:
        print(f"  Output: {output_path}")
    return computed, failed

# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------

def main():
    print("=" * 60)
    print("Biology Scalar Builder")
    print("=" * 60)
    print(f"  B3 input:  {B3_INPUT}")
    print(f"  B1 input:  {B1_INPUT}")
    print(f"  Output to: {PROMOTED}")
    print()

    # B3 Amino — unsigned backbone bond angle, L-amino acids
    c, f = process_lake(
        B3_INPUT, B3_OUTPUT, compute_b3_scalar,
        "B3 Amino", lake_id="b3_amino", domain="biology"
    )

    print()

    # B1 Chirality — signed scalar separates D from L enantiomers
    c, f = process_lake(
        B1_INPUT, B1_OUTPUT, compute_b1_scalar,
        "B1 Chirality", lake_id="b1_chirality", domain="biology"
    )

    print()
    print("Next steps:")
    print("  1. Verify output scalars look reasonable:")
    print("     B3: values ~1.84-1.96 rad (105-112 degrees)")
    print("     B1: L-amino ~-1.88 rad, D-amino ~+1.88 rad")
    print("  2. Run scalarize.py -> unify.py -> build_pinch_table.py")
    print()
    print("PENDING BEFORE VOL5 PROMOTION:")
    print("  B3: requires null lake (scrambled coordinates, same amino acids)")
    print("  B1: requires null lake (L-only baseline, no D-amino mixing)")

if __name__ == "__main__":
    main()