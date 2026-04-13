import json
import random
import math
import os

# 🛡️ NS6_30: THE TRUE NULL MIRROR (Twin Architecture)
# -----------------------------------------------------------
def build_true_null():
    L = 16.0 / math.pi
    ANCHOR = 6.6069e10
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    source_path = os.path.join(project_root, 'lake', 'Master_Galaxy_Vol5.jsonl')
    null_path = os.path.join(project_root, 'lake', 'Master_Galaxy_Null_Vol5.jsonl')
    
    print("💎 CONSTRUCTING TRUE NULL MIRROR...")

    # Load real physics pools
    v_pool, m_pool, z_pool = [], [], []
    with open(source_path, 'r') as f:
        for line in f:
            d = json.loads(line)
            v_pool.append(float(d['Vdisp']))
            m_pool.append(float(d['rpmag']))
            z_pool.append(float(d['zsp']))

    # Scramble the pools completely
    random.shuffle(v_pool)
    random.shuffle(m_pool)
    random.shuffle(z_pool)

    with open(null_path, 'w') as f_out:
        for v, m, z in zip(v_pool, m_pool, z_pool):
            lum = 10**((25 - m) / 2.5)
            ks = ((v**4) / lum) / ANCHOR
            phi = math.log(ks) % L
            bin_idx = min(int((phi / L) * 10), 9)
            
            # Create a 1-to-1 mirrored JSON entry
            entry = {
                "Vdisp": v, "rpmag": m, "zsp": z,
                "kish_phi": round(phi, 6),
                "kish_bin": bin_idx,
                "vol5_status": "TRUE_NULL_MIRROR"
            }
            f_out.write(json.dumps(entry) + '\n')

    print(f"🏆 TRUE NULL MIRROR BUILT: {len(v_pool):,} mirrored entries.")

if __name__ == "__main__":
    build_true_null()