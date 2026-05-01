import json
import os
from collections import Counter

def run_stitch_audit():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Load both Master Lakes
    galaxy_path = os.path.join(project_root, 'lake', 'Master_Galaxy_Vol6_PHYSICAL.jsonl')
    gaia_path = os.path.join(project_root, 'lake', 'Master_Stellar_Gaia_Standard.jsonl')
    
    gal_counts = Counter()
    star_counts = Counter()

    print("📊 ANALYZING DOMAIN OVERLAP...")
    
    # Read Galaxies (Physical Faber-Jackson)
    with open(galaxy_path, 'r') as f:
        for line in f:
            gal_counts[json.loads(line)['kish_bin']] += 1
            
    # Read Stars (Physical Parallax)
    with open(gaia_path, 'r') as f:
        for line in f:
            star_counts[json.loads(line)['kish_bin']] += 1

    print("\n" + "="*45)
    print(f"{'Bin':<5} {'Galaxies %':<15} {'Stars %':<15}")
    print("-" * 45)

    g_total = sum(gal_counts.values())
    s_total = sum(star_counts.values())

    for b in range(10):
        g_p = (gal_counts[b] / g_total) * 100
        s_p = (star_counts[b] / s_total) * 100
        marker = " << LOCK" if b in [6, 7] else ""
        print(f"{b:<5} {g_p:<15.2f} {s_p:<15.2f} {marker}")
    print("="*45)

if __name__ == "__main__":
    run_stitch_audit()