import json
import os
from collections import Counter

# 🛡️ NS6_37: THE REFEREED CARDINAL AUDIT (Mondy-Standard)
# -----------------------------------------------------------
def audit_cardinality_refereed():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_path = os.path.join(project_root, 'lake', 'Master_Galaxy_Vol5.jsonl')
    
    if not os.path.exists(input_path):
        print("❌ ERROR: Galaxy Lake not found.")
        return

    # Four MUTUALLY EXCLUSIVE quadrants
    quads = {
        'NE': Counter(),  # Dec > 15, RA > 180
        'NW': Counter(),  # Dec > 15, RA <= 180
        'SE': Counter(),  # Dec <= 15, RA > 180
        'SW': Counter(),  # Dec <= 15, RA <= 180
    }
    totals = {q: 0 for q in quads}

    print("🔭 SECTORING SKY DATA INTO FOUR MUTUALLY EXCLUSIVE QUADRANTS...")
    
    with open(input_path, 'r') as f:
        for line in f:
            d = json.loads(line)
            ra = float(d.get('ra', 0))
            dec = float(d.get('dec', 0))
            bin_idx = d.get('kish_bin')
            
            if bin_idx is None: continue

            # Mondy's Waterfall Logic: Exclusive Assignment
            if dec > 15:
                if ra > 180:
                    quads['NE'][bin_idx] += 1
                    totals['NE'] += 1
                else:
                    quads['NW'][bin_idx] += 1
                    totals['NW'] += 1
            else: # dec <= 15
                if ra > 180:
                    quads['SE'][bin_idx] += 1
                    totals['SE'] += 1
                else:
                    quads['SW'][bin_idx] += 1
                    totals['SW'] += 1

    print("\n" + "="*65)
    print(f"{'Sector':<8} {'N':>10} {'Peak Bin':>10} {'Peak %':>10} {'Chi2':>12}")
    print("-" * 65)
    
    all_n = sum(totals.values())
    peak_bins = []

    for q_name in ['NE', 'NW', 'SE', 'SW']:
        count = totals[q_name]
        if count < 500: # Threshold for statistical relevance
            print(f"{q_name:<8} {count:10,}    [INSUFFICIENT DATA FOR SECTOR]")
            continue
        
        peak_bin = quads[q_name].most_common(1)[0][0]
        peak_perc = (quads[q_name][peak_bin] / count) * 100
        peak_bins.append(peak_bin)
        
        # Calculate Chi-Squared for this specific quadrant
        expected = count / 10.0
        chi2 = sum([((quads[q_name][i] - expected)**2) / expected for i in range(10)])
        
        print(f"{q_name:<8} {count:10,} {peak_bin:10} {peak_perc:9.2f}% {chi2:12.2f}")

    print("="*65)
    print(f"TOTAL GALAXIES AUDITED: {all_n:,}")
    
    if len(set(peak_bins)) == 1 and len(peak_bins) > 1:
        print(f"\n✅ VERDICT: ALL SECTORS PEAK AT BIN {peak_bins[0]}.")
        print("PHASE IS CONSTANT ACROSS SKY — METRIC PROPERTY CONFIRMED.")
    elif len(peak_bins) > 1:
        print(f"\n⚠️ VERDICT: SECTORS PEAK AT DIFFERENT BINS {set(peak_bins)}.")
        print("PHASE VARIES BY DIRECTION — CONSISTENT WITH LOCAL STRUCTURE.")
    
    # Visual distribution per quadrant
    for q_name in ['NE', 'NW', 'SE', 'SW']:
        if totals[q_name] > 500:
            print(f"\n📊 {q_name} DISTRIBUTION:")
            for i in range(10):
                p = (quads[q_name][i] / totals[q_name]) * 100
                print(f"  Bin {i}: {'█' * int(p)} {p:.2f}%")

if __name__ == "__main__":
    audit_cardinality_refereed()
    input("\nPress ENTER to close...")