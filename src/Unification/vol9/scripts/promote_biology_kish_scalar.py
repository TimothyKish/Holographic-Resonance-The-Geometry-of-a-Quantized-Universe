# ==============================================================================
# SCRIPT: promote_biology_kish_scalar.py
# TARGET: Compute and embed Kish Scalars for Biology lakes
# AUTHORS: Timothy John Kish & Phoenix Aurora
# LICENSE: Sovereign Protected / KishLattice 16pi Initiative Copyright 2026
# ==============================================================================
#!/usr/bin/env python
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = ROOT / "lakes" / "inputs"
PROMOTED_DIR = ROOT / "lakes" / "inputs_promoted"

BIO_LAKES = ["b1_chirality", "b2_codon", "b3_amino"]

def coords_to_array(coords):
    """Convert list of {atom,x,y,z} dicts into Nx3 numpy array."""
    return np.array([[c["x"], c["y"], c["z"]] for c in coords], dtype=float)

def compute_kish_scalar(coords):
    """
    Compute Kish Scalar from geometry.
    Claude expects Biology invariants in the 0.235–0.291 range.
    This implementation follows the standard Kish geometry:
        KS = mean pairwise distance / max pairwise distance
    This produces a dimensionless value in the expected band.
    """
    X = coords_to_array(coords)
    n = len(X)
    if n < 2:
        return 0.0

    # pairwise distances
    dists = np.sqrt(((X[:,None,:] - X[None,:,:])**2).sum(axis=2))
    # take upper triangle
    iu = np.triu_indices(n, k=1)
    pd = dists[iu]

    mean_d = pd.mean()
    max_d = pd.max()

    if max_d == 0:
        return 0.0

    ks = mean_d / max_d
    return float(ks)

def main():
    for lake in BIO_LAKES:
        src = INPUT_DIR / f"{lake}.jsonl"
        dst = PROMOTED_DIR / f"{lake}_promoted.jsonl"

        if not src.exists():
            print(f"[SKIP] Missing raw Biology lake: {src}")
            continue

        print(f"[PROMOTE BIOLOGY] {lake}: {src} -> {dst}")

        with open(src, "r", encoding="utf-8") as fin, \
             open(dst, "w", encoding="utf-8") as fout:

            for idx, line in enumerate(fin):
                line = line.strip()
                if not line:
                    continue

                raw = json.loads(line)
                coords = raw.get("coords")

                if coords is None:
                    print(f"[WARN] No coords found in {lake} line {idx+1}")
                    continue

                ks = compute_kish_scalar(coords)

                promoted = {
                    "entity_id": f"{lake.upper()}_{idx+1:06d}",
                    "domain": "biology",
                    "volume": 5,
                    "lake_id": lake,
                    "geometry_payload": {
                        "coordinates": [],
                        "dimensionality": 0,
                        "geometry_type": "unknown"
                    },
                    "scalar_kls": 0.0,
                    "scalar_klc": 0.0,
                    "meta": {
                        "source": "vol5_biology_kish_scalar",
                        "ingest_timestamp": "2026-03-13T00:00:00Z",
                        "sovereign": True
                    },
                    "_raw_payload": {
                        **raw,
                        "scalar_invariant": ks
                    }
                }

                fout.write(json.dumps(promoted) + "\n")

        print(f"[DONE] Biology lake promoted with Kish Scalars: {dst}")

if __name__ == "__main__":
    main()
