# vol7/V7_Universal/scripts/master_clock_sync.py
import math

L = 16.0 / math.pi

def run_universal_sync():
    print("===============================================================")
    print(" 🛰️ V7_01: THE MASTER CLOCK SYNC (The Triple-Scale Audit)")
    print("===============================================================")
    
    # The Three Scales of the Lattice
    scales = {
        "GALACTIC (S6)": {"val": 1.8, "state": "FATIGUE (Spring)", "jitter": 0.40},
        "SOLAR (S7)":    {"val": 1.0, "state": "SHIELD (Crystal)", "jitter": 0.03},
        "PLANETARY (P2)":{"val": 2.0, "state": "CAGE (Pressure)",  "jitter": 0.02}
    }

    print(f"{'Scale Domain'.ljust(18)} | {'Multiplier'.ljust(12)} | {'Jitter'.ljust(10)} | {'Lattice State'}")
    print("-" * 70)

    for name, data in scales.items():
        m = data["val"]
        jit = data["jitter"]
        state = data["state"]
        
        # Calculate the 'Sync' - how close is it to a perfect Lattice harmonic?
        # A result of 0.0 is a perfect lock.
        sync_error = abs(m - round(m)) if m != 1.8 else abs(m - 1.8)
        
        bar_len = int((1.0 - jit) * 30)
        bar = "█" * bar_len
        print(f"{name.ljust(18)} | {m:.2f}x L".ljust(33), f"| {jit:.2f}".ljust(13), f"| {state}")
        print(f"{' '.ljust(21)} Sync Precision: {100*(1-sync_error):.1f}% {bar}")
        print("-" * 70)

if __name__ == "__main__":
    run_universal_sync()