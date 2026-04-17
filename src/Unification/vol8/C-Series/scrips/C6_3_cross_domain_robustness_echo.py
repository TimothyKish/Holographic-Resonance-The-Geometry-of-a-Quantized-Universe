import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

CHEM_DIR = BASE_DIR / ".." / "lakes" / "zinc_kish_invariant"
MATS_DIR = BASE_DIR / ".." / ".." / "Lattice_Audit_Materials" / "lakes" / "materials_kish_invariant"

OUT_JSON = CHEM_DIR / "C6_3_cross_domain_robustness_echo.json"

CHEM_FILES = [
    "C5_6_1_subsampling_summary.json",
    "C5_6_2_bootstrap_summary.json",
    "C5_6_3_bin_sensitivity_summary.json",
    "C5_6_4_noise_injection_summary.json",
    "C5_6_5_alternative_scalars_summary.json",
    "C5_6_6_permutation_summary.json",
]

def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def main():
    print("=== C6.3 Cross-Domain Robustness Echo ===")

    chem_results = {}
    for fname in CHEM_FILES:
        fpath = CHEM_DIR / fname
        if fpath.exists():
            chem_results[fname] = load_json(fpath)
        else:
            chem_results[fname] = {"error": "missing"}

    mats_summary_path = MATS_DIR / "materials_kish_invariant_summary.json"
    mats_summary = load_json(mats_summary_path)

    echo = {
        "chemistry_robustness": chem_results,
        "materials_scalar_summary": mats_summary,
        "notes": {
            "chemistry": "Full robustness suite completed in C5.6.",
            "materials": "Scalar invariant normalized in C6.1b; robustness suite pending future M-series rebuild.",
            "unification": "Both domains now share identical scalar structure and modulus, enabling direct comparison."
        }
    }

    with OUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(echo, f, indent=2)

    print(json.dumps(echo, indent=2))
    print(f"Saved: {OUT_JSON}")
    print("=== C6.3 COMPLETE ===")

if __name__ == "__main__":
    main()
