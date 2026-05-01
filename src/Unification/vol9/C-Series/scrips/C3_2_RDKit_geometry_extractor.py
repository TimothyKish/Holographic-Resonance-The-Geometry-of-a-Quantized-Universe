#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
C3.2 — RDKit Sovereign Geometry Extractor
-----------------------------------------
Generates 3D geometries for the sovereign chemistry lake using RDKit’s
ETKDG embedding with robust fallback behavior. Input molecules are
structure‑unique and sorted lexicographically by SMILES, ensuring a
deterministic, geometry‑first processing order aligned with the
materials pipeline.

Input:
  ../lakes/zinc_3d_manifest/zinc20_manifest_unique_smiles_sorted.jsonl
    - One entry per unique SMILES (C3.1.1)
    - Sorted lexicographically by SMILES (C3.1.2)
    - ZINC IDs, tranche names, and metadata preserved for audit

Output:
  ../lakes/zinc_3d_geom_jsonl/<zinc_id>.jsonl
    - Sovereign 3D geometries (ETKDG)
    - One geometry per unique molecular graph
    - Deterministic ordering and reproducible coordinates

Geometry pipeline:
  1. Build unsanitized RDKit molecule from SMILES
  2. Update property cache (strict=False) to define implicit valence
  3. Add hydrogens with coordinates
  4. Initialize ring information (FastFindRings)
  5. Embed with ETKDG (robust mode)
  6. Extract atomic coordinates into sovereign JSONL format

This stage completes the chemistry lake’s geometry backbone, producing
a structure‑unique, reproducible, and fully sovereign molecular dataset
for downstream lattice mapping and empirical unification.
"""


import os
import json
import hashlib
from rdkit import Chem
from rdkit.Chem import AllChem

# -----------------------------
# PATHS
# -----------------------------
MANIFEST_PATH = "../lakes/zinc_3d_manifest/zinc20_manifest_unique_smiles.jsonl"

GEOM_JSONL_DIR = "../lakes/zinc_3d_geom_jsonl/"
GEOM_AUDIT_PATH = "../lakes/zinc_3d_geom_manifest/geometry_audit.jsonl"
FAILED_LOG_PATH = "../lakes/zinc_3d_geom_manifest/failed_geometry.log"

os.makedirs(GEOM_JSONL_DIR, exist_ok=True)
os.makedirs(os.path.dirname(GEOM_AUDIT_PATH), exist_ok=True)


# -----------------------------
# HELPERS
# -----------------------------
def sha256_string(s):
    h = hashlib.sha256()
    h.update(s.encode("utf-8"))
    return h.hexdigest()


def per_molecule_seed(zinc_id):
    try:
        return int(zinc_id) & 0xFFFFFFFF
    except Exception:
        return 42


def neutralize_mol(mol):
    """
    Neutralize common +1 centers for embedding stability.
    Does NOT change the stored SMILES, only the internal
    molecule used for 3D generation.
    """
    try:
        patt = Chem.MolFromSmarts("[+1!H0]")
        while mol.HasSubstructMatch(patt):
            at_idx = mol.GetSubstructMatch(patt)[0]
            atom = mol.GetAtomWithIdx(at_idx)
            atom.SetFormalCharge(0)
            atom.SetNumExplicitHs(atom.GetTotalNumHs() + 1)
        Chem.SanitizeMol(mol, sanitizeOps=Chem.SanitizeFlags.SANITIZE_ADJUSTHS)
    except Exception:
        pass
    return mol


def optimize_mmff_uff(mol):
    """
    Try MMFF94 first, then UFF as fallback.
    If both fail, return False; else True.
    """
    try:
        if AllChem.MMFFHasAllMoleculeParams(mol):
            res = AllChem.MMFFOptimizeMolecule(mol)
            if res == 0:
                return True
    except Exception:
        pass

    try:
        res = AllChem.UFFOptimizeMolecule(mol)
        if res == 0:
            return True
    except Exception:
        pass

    return False


def embed_with_params(mol, params):
    """
    Try embedding with given ETKDG params.
    Returns True on success, False on failure.
    """
    try:
        cid = AllChem.EmbedMolecule(mol, params)
        if cid < 0:
            return False
        return True
    except Exception:
        return False


def embed_random(mol, seed):
    """
    Random-coordinate embedding without ETKDG.
    Returns True on success, False on failure.
    """
    try:
        cid = AllChem.EmbedMolecule(
            mol,
            useRandomCoords=True,
            randomSeed=seed
        )
        if cid < 0:
            return False
        return True
    except Exception:
        return False


def mol_to_atoms(mol):
    """
    Convert a molecule with a conformer to a list of atom dicts.
    """
    try:
        conf = mol.GetConformer()
        atoms = []
        for atom in mol.GetAtoms():
            pos = conf.GetAtomPosition(atom.GetIdx())
            atoms.append({
                "element": atom.GetSymbol(),
                "x": pos.x,
                "y": pos.y,
                "z": pos.z
            })
        return atoms
    except Exception:
        return None


def prepare_mol_for_embedding(smiles):
    """
    Build an unsanitized molecule, update property cache so implicit
    valence is defined, add hydrogens, and initialize ring information
    so ETKDG does not trip on internal preconditions.
    """
    mol = Chem.MolFromSmiles(smiles, sanitize=False)
    if mol is None:
        return None

    # Ensure implicit valence / H counts are computed, but be lenient
    try:
        mol.UpdatePropertyCache(strict=False)
    except Exception:
        pass

    # Now it's safe to add hydrogens
    try:
        mol_h = Chem.AddHs(mol, addCoords=True)
    except Exception:
        return None

    # Initialize ring info without full sanitization
    try:
        Chem.FastFindRings(mol_h)
    except Exception:
        pass

    return mol_h


def generate_conformer(smiles, zinc_id):
    """
    Best-geometry-first, multi-stage embedding pipeline.

    Order:
      1) ETKDGv3 (no sanitization, ring info initialized)
      2) ETKDGv2 (no sanitization)
      3) ETKDGv3 on neutralized mol
      4) Random embedding + MMFF94/UFF
      5) Random embedding + UFF only
      6) Random embedding only

    Returns list of atoms with x,y,z,element or None on failure.
    """
    seed = per_molecule_seed(zinc_id)

    base_h = prepare_mol_for_embedding(smiles)
    if base_h is None:
        return None

    try:
        # 1) ETKDGv3
        mol1 = Chem.Mol(base_h)
        params_v3 = AllChem.ETKDGv3()
        params_v3.randomSeed = seed
        params_v3.useRandomCoords = False
        if embed_with_params(mol1, params_v3):
            optimize_mmff_uff(mol1)
            atoms = mol_to_atoms(mol1)
            if atoms:
                return atoms

        # 2) ETKDGv2
        mol2 = Chem.Mol(base_h)
        params_v2 = AllChem.ETKDGv2()
        params_v2.randomSeed = seed
        params_v2.useRandomCoords = False
        if embed_with_params(mol2, params_v2):
            optimize_mmff_uff(mol2)
            atoms = mol_to_atoms(mol2)
            if atoms:
                return atoms

        # 3) ETKDGv3 on neutralized mol
        mol3 = Chem.Mol(base_h)
        mol3 = neutralize_mol(mol3)
        params_v3n = AllChem.ETKDGv3()
        params_v3n.randomSeed = seed
        params_v3n.useRandomCoords = False
        if embed_with_params(mol3, params_v3n):
            optimize_mmff_uff(mol3)
            atoms = mol_to_atoms(mol3)
            if atoms:
                return atoms

        # 4) Random embedding + MMFF94/UFF
        mol4 = Chem.Mol(base_h)
        if embed_random(mol4, seed):
            if optimize_mmff_uff(mol4):
                atoms = mol_to_atoms(mol4)
                if atoms:
                    return atoms

        # 5) Random embedding + UFF only
        mol5 = Chem.Mol(base_h)
        if embed_random(mol5, seed):
            try:
                AllChem.UFFOptimizeMolecule(mol5)
            except Exception:
                pass
            atoms = mol_to_atoms(mol5)
            if atoms:
                return atoms

        # 6) Random embedding only
        mol6 = Chem.Mol(base_h)
        if embed_random(mol6, seed):
            atoms = mol_to_atoms(mol6)
            if atoms:
                return atoms

        return None

    except Exception:
        return None


# -----------------------------
# MAIN EXTRACTION
# -----------------------------
def run_geometry_extraction():
    print("=== C3.2 RDKit Geometry Extractor (robust + ring init) ===")

    audit_f = open(GEOM_AUDIT_PATH, "w", encoding="utf-8")
    failed_f = open(FAILED_LOG_PATH, "w", encoding="utf-8")  # overwrite each run

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest_entries = [json.loads(line) for line in f]

    manifest_entries.sort(key=lambda e: e["zinc_id"])

    processed = 0

    for entry in manifest_entries:
        zinc_id = entry["zinc_id"]
        smiles = entry["smiles"]
        tranche = entry.get("tranche") or entry.get("tranche_name") or "UNKNOWN"

        print(f"[{processed+1}] ZINC {zinc_id} — generating geometry")

        atoms = generate_conformer(smiles, zinc_id)
        if atoms is None:
            print(f"[SKIP] Could not generate geometry for ZINC {zinc_id}")
            failed_f.write(f"{zinc_id}\t{smiles}\n")
            continue

        geom_record = {
            "zinc_id": zinc_id,
            "smiles": smiles,
            "tranche": tranche,
            "geometry": atoms
        }

        out_path = os.path.join(GEOM_JSONL_DIR, f"{zinc_id}.jsonl")
        with open(out_path, "w", encoding="utf-8") as out:
            out.write(json.dumps(geom_record) + "\n")

        audit_f.write(json.dumps({
            "zinc_id": zinc_id,
            "sha256": sha256_string(json.dumps(geom_record)),
            "jsonl_file": f"{zinc_id}.jsonl"
        }) + "\n")

        processed += 1

    audit_f.close()
    failed_f.close()
    print("=== C3.2 COMPLETE (RDKit sovereign geometry, robust + ring init) ===")


if __name__ == "__main__":
    run_geometry_extraction()
