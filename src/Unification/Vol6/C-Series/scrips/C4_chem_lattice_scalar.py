#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
C4 — Chemistry Lattice Scalar (16/pi Litmus)
--------------------------------------------
Reads the Kish geometry lake from C3.3 and computes a scalar invariant
per molecule, analogous to the materials-side Lattice Deviation Scalar.

For each molecule:
  - Use max_radius as a proxy for bounding sphere radius R
  - Volume V = (4/3) * pi * R^3
  - ratio = V / n_atoms
  - deviation = abs(ratio % (16/pi))

Outputs:
  ../lakes/zinc_kish_invariant/zinc_kish_invariant.jsonl
  ../lakes/zinc_kish_invariant/summary.json
"""

import os
import json
import math

KISH_LAKE_PATH = "../lakes/zinc_kish_lake/zinc_kish_geom.jsonl"
INV_DIR = "../lakes/zinc_kish_invariant/"
INV_PATH = os.path.join(INV_DIR, "zinc_kish_invariant.jsonl")
SUMMARY_PATH = os.path.join(INV_DIR, "summary.json")

os.makedirs(INV_DIR, exist_ok=True)

MOD_CONST = 16.0 / math.pi


def compute_scalar_invariant(n_atoms, max_radius):
    """
    Chemistry analogue of the materials Lattice Deviation Scalar.

    V = (4/3) * pi * R^3
    ratio = V / n_atoms
    deviation = abs(ratio % (16/pi))
    """
    if n_atoms <= 0 or max_radius <= 0:
        return None

    volume = (4.0 / 3.0) * math.pi * (max_radius ** 3)
    ratio = volume / float(n_atoms)
    deviation = abs(ratio % MOD_CONST)
    return deviation


def run_c4():
    print("=== C4 Chemistry Lattice Scalar (16/pi Litmus) ===")

    invariants = []

    with open(KISH_LAKE_PATH, "r", encoding="utf-8") as f_in, \
         open(INV_PATH, "w", encoding="utf-8") as f_out:

        for line in f_in:
            rec = json.loads(line)
            zinc_id = rec["zinc_id"]
            n_atoms = rec.get("n_atoms", len(rec.get("atoms", [])))
            max_radius = rec.get("max_radius", 0.0)

            scalar = compute_scalar_invariant(n_atoms, max_radius)
            if scalar is None:
                continue

            inv_rec = {
                "zinc_id": zinc_id,
                "n_atoms": n_atoms,
                "max_radius": max_radius,
                "scalar_invariant": scalar
            }

            f_out.write(json.dumps(inv_rec) + "\n")
            invariants.append(scalar)

    # Summary stats
    if invariants:
        n = len(invariants)
        mean_val = sum(invariants) / n
        var = sum((x - mean_val) ** 2 for x in invariants) / n
        std_val = math.sqrt(var)

        summary = {
            "count": n,
            "mean_scalar": mean_val,
            "std_scalar": std_val,
            "min_scalar": min(invariants),
            "max_scalar": max(invariants),
            "modulus": MOD_CONST
        }
    else:
        summary = {
            "count": 0,
            "mean_scalar": None,
            "std_scalar": None,
            "min_scalar": None,
            "max_scalar": None,
            "modulus": MOD_CONST
        }

    with open(SUMMARY_PATH, "w", encoding="utf-8") as f_sum:
        f_sum.write(json.dumps(summary, indent=2))

    print(f"=== C4 COMPLETE — {summary['count']} scalars written ===")


if __name__ == "__main__":
    run_c4()
