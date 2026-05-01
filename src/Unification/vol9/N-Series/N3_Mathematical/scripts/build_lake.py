# vol5/N-Series/N3_Noise/scripts/build_lake.py
import json
import random
import os

def build_noise_null():
    print("[*] Building N3_Noise (Pure RNG) Raw Lake...")
    
    os.makedirs("../lake", exist_ok=True)
    
    with open("../lake/noise_null_raw.jsonl", "w") as f:
        # Generate 1000 purely random data points
        for _ in range(1000):
            noise_entry = {
                "rng_alpha": random.uniform(0.0, 1000.0),
                "rng_beta": random.uniform(0.0, 1000.0)
            }
            f.write(json.dumps(noise_entry) + "\n")
            
    print("[*] N3_Noise Raw Lake built successfully. Pure mathematical noise generated.")

if __name__ == "__main__":
    build_noise_null()