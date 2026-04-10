# vol5/S-Series/S1_Galactic/scripts/build_lake.py
import json
import os
import time

def build_lake():
    print("===============================================================")
    print(" 🌌 S1_GALACTIC: CALIBRATION MODE (Live API 500 Bypass)")
    print("===============================================================")
    
    # Gold Standard Calibration Set: Real Elliptical Galaxy Data
    # Sigma (km/s) and Mag_r for key benchmark galaxies
    calibration_data = [
        {"name": "M31", "sigma": 160.0, "mag": -21.2, "z": -0.001},
        {"name": "M32", "sigma": 75.0, "mag": -16.5, "z": -0.0007},
        {"name": "NGC4486", "sigma": 375.0, "mag": -22.7, "z": 0.004},
        {"name": "NGC3379", "sigma": 206.0, "mag": -20.9, "z": 0.003},
        {"name": "NGC4649", "sigma": 335.0, "mag": -22.3, "z": 0.0037},
        {"name": "NGC4472", "sigma": 300.0, "mag": -22.9, "z": 0.0033},
        {"name": "NGC5846", "sigma": 250.0, "mag": -21.5, "z": 0.005},
        {"name": "NGC1407", "sigma": 290.0, "mag": -21.8, "z": 0.0059},
        {"name": "NGC4374", "sigma": 280.0, "mag": -22.1, "z": 0.0033},
        {"name": "NGC708", "sigma": 225.0, "mag": -21.4, "z": 0.016}
    ]
    
    RAW_LAKE = "../lake/s1_galactic_raw.jsonl"
    os.makedirs("../lake", exist_ok=True)
    
    with open(RAW_LAKE, 'w', encoding='utf-8') as out_f:
        for i, row in enumerate(calibration_data):
            out_f.write(json.dumps({
                "entity_id": f"CAL_S1_{i:03d}",
                "v_dispersion_kms": row['sigma'],
                "magnitude_r": row['mag'],
                "redshift_z": row['z'],
                "meta": {"name": row['name']}
            }) + "\n")
            
    print(f"[+] S1 Calibration Lake built. {len(calibration_data)} benchmark galaxies loaded.")
    print("[*] Ready for Promote/Scalarize audit.")

if __name__ == "__main__":
    build_lake()