import numpy as np

def run_gearing_audit():
    print("🛡️  INITIATING UNIVERSAL GEARING AUDIT (RATIO SYNC)...")
    
    # Stable Nodes from previous runs
    g_nodes = np.array([92.7, 139.1, 189.7, 242.2, 318.2]) # km/s
    f_nodes = np.array([191.8, 221.4, 367.8, 660.2, 1152.5]) # DM
    
    def get_ratios(nodes):
        return nodes[1:] / nodes[:-1]

    g_ratios = get_ratios(g_nodes)
    f_ratios = get_ratios(f_nodes)
    
    print("\n" + "="*55)
    print(f"{'Step':<10} | {'Galaxy Ratio':<15} | {'FRB Ratio':<15}")
    print("-" * 55)
    for i in range(4):
        print(f"Node {i+1}->{i+2} | {g_ratios[i]:<14.3f} | {f_ratios[i]:<14.3f}")
    print("="*55)

    # Calculate the "Log-Step" (The actual 'L' of the staircase)
    g_L = np.mean(np.log(g_ratios))
    f_L = np.mean(np.log(f_ratios))
    
    print(f"\n📈 MEAN LOG-STEP (THE REAL L):")
    print(f"   Galaxy L-Factor: {g_L:.4f}")
    print(f"   FRB L-Factor:    {f_L:.4f}")
    
    delta = abs(g_L - f_L)
    print(f"\n📝 ARCHITECTURAL SYNC: ΔL = {delta:.4f}")
    
    if delta < 0.1:
        print("🚨 RESONANCE CONFIRMED: The 'Staircase' has the same slope.")
    else:
        print("✅ PHOENIX NULL: The staircases have different slopes.")

if __name__ == "__main__":
    run_gearing_audit()