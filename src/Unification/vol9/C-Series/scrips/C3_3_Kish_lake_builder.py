#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
C3.3 — Kish Geometry Lake Builder
---------------------------------
Reads sovereign geometry JSONL files from C3.2 and produces a
normalized, Kish-ready geometry lake.

Input:
  ../lakes/zinc_3d_geom_jsonl/*.jsonl

Output:
  ../lakes/zinc_kish_lake/zinc_kish_geom.jsonl
"""

import os
import json
import math

GEOM_JSONL_DIR = "../lakes/zinc_3d_geom_jsonl/"
KISH_LAKE_DIR = "../lakes/zinc_kish_lake/"
KISH_LAKE_PATH = os.path.join(KISH_LAKE_DIR, "zinc_kish_geom.jsonl")

os.makedirs(KISH_LAKE_DIR, exist_ok=True)


def center_and_scale(atoms, unit_radius=True):
    """
    Center molecule at origin and optionally scale so that
    max distance from origin is 1.0.
    """
    if not atoms:
        return atoms

    xs = [a["x"] for a in atoms]
    ys = [a["y"] for a in atoms]
    zs = [a["z"] for a in atoms]

    cx = sum(xs) / len(xs)
    cy = sum(ys) / len(ys)
    cz = sum(zs) / len(zs)

    centered = []
    max_r = 0.0
    for a in atoms:
        x = a["x"] - cx
        y = a["y"] - cy
        z = a["z"] - cz
        r = math.sqrt(x*x + y*y + z*z)
        if r > max_r:
            max_r = r
        centered.append({
            "element": a["element"],
            "x": x,
            "y": y,
            "z": z
        })

    if unit_radius and max_r > 0:
        scaled = []
        for a in centered:
            scaled.append({
                "element": a["element"],
                "x": a["x"] / max_r,
                "y": a["y"] / max_r,
                "z": a["z"] / max_r
            })
        return scaled

    return centered


def build_kish_lake():
    print("=== C3.3 Kish Geometry Lake Builder ===")

    files = sorted(
        f for f in os.listdir(GEOM_JSONL_DIR)
        if f.endswith(".jsonl")
    )

    count = 0
    with open(KISH_LAKE_PATH, "w", encoding="utf-8") as out:
        for fname in files:
            path = os.path.join(GEOM_JSONL_DIR, fname)
            with open(path, "r", encoding="utf-8") as f:
                rec = json.loads(f.readline())

            zinc_id = rec["zinc_id"]
            smiles = rec["smiles"]
            tranche = rec["tranche"]
            atoms = rec["geometry"]

            norm_atoms = center_and_scale(atoms, unit_radius=True)

            kish_record = {
                "zinc_id": zinc_id,
                "smiles": smiles,
                "tranche": tranche,
                "atoms": norm_atoms,
                # hooks for C4:
                "n_atoms": len(norm_atoms),
                "max_radius": max(
                    math.sqrt(a["x"]**2 + a["y"]**2 + a["z"]**2)
                    for a in norm_atoms
                ) if norm_atoms else 0.0
            }

            out.write(json.dumps(kish_record) + "\n")
            count += 1

    print(f"=== C3.3 COMPLETE — {count} molecules in Kish lake ===")


if __name__ == "__main__":
    build_kish_lake()
