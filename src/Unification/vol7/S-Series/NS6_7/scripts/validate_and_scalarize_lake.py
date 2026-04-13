import json
import math
import os

# 🛡️ NS6_14: VOL5 SCALARIZE & VALIDATE
# -----------------------------------------------------------
# Goal: Inject Kish Scalars and Binning into the Master JSONL.
# Standards: Dimensionless 16/pi Phase-Fold.

def validate_and_scalarize_lake(input_file):
    L = 16.0 / math.pi
    ANCHOR = 6.6069e10 # The Faber-Jackson Universal Anchor
    
    output_file = input_file.replace(".jsonl", "_Vol5_Validated.jsonl")
    valid_count = 0
    
    print(f"🧬 UPGRADING TO VOL5: {input_file}")
    
    with open(input_file, 'r') as src, open(output_file, 'w') as dst:
        for line in src:
            data = json.loads(line)
            
            try:
                # 1. Calculate Luminosity (r-band)
                # Formula: 10^((25 - mag) / 2.5)
                lum = 10**((25 - data['rpmag']) / 2.5)
                
                # 2. Calculate the Kish Scalar (Dimensionless)
                # FJ Invariant: (sigma^4 / L) / Anchor
                ks = ((data['Vdisp']**4) / lum) / ANCHOR
                
                # 3. Log-Modulo 16/pi Folding
                phi = math.log(ks) % L
                bin_idx = min(int((phi / L) * 10), 9)
                
                # 4. Inject "Vol5 Standard" Fields
                data['kish_phi'] = round(phi, 6)
                data['kish_bin'] = bin_idx
                data['vol5_status'] = "VALIDATED"
                
                dst.write(json.dumps(data) + '\n')
                valid_count += 1
                
            except (KeyError, ZeroDivisionError, TypeError):
                # If a row is missing data, we skip it to keep the lake 'Pure'
                continue

    print(f"🏆 VALIDATION COMPLETE: {valid_count} Probes Commissioned.")
    print(f"Final Archive: {output_file}")

if __name__ == "__main__":
    # We run this after the 'knock_on_sloan' harvest succeeds
    validate_and_scalarize_lake('../lake/Lake_SDSS_DR16_100K_z01_z70_V70_G.jsonl')