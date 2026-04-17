# ==============================================================================
# SCRIPT: build_k2_pulsar_periods_lake.py
# SERIES: K-Series / K2_PulsarPeriods
# DOMAIN: stellar_rotation
#
# SOURCE: ATNF Pulsar Catalogue via VizieR mirror (B/psr)
#         ATNF direct site was HTTP 500 on 2026-04-05.
#         VizieR is the stable, continuously-updated mirror.
#
# AUTO-FETCH: No manual download required.
#   Script tries VizieR B/psr first, then VII/245 as fallback.
#   Downloaded data is cached locally for reruns.
#
# KINEMATIC TYPE: SPIN (neutron star rotation)
#   Period range: ~1.4ms to ~10+ seconds -> scalar 0.0009 to 2.41
#   Bridges near-zero through chemistry into biology range.
#
# SCALAR:
#   scalar = log(P0_ms + 1) / log(k_geo)   P0_ms = P0_seconds * 1000
#
# AUTHORS: Timothy John Kish & Mondy
# AUDIT STATUS: mondy_verified_2026-04
# ==============================================================================

import csv, io, json, math, time, uuid, urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path

PI    = math.pi
K_GEO = 16.0 / PI
LOG_K = math.log(K_GEO)

SCRIPTS_DIR = Path(__file__).resolve().parent
K2_DIR      = SCRIPTS_DIR.parent
K_SERIES    = K2_DIR.parent
VOL5_ROOT   = K_SERIES.parent
PROMOTED    = VOL5_ROOT / "lakes" / "inputs_promoted"
RAW_CACHE   = K2_DIR / "lake" / "atnf_pulsars_raw.csv"
OUT_REAL    = PROMOTED / "k2_pulsar_periods_promoted.jsonl"
P0_MAX_MS   = 30000.0

VIZIER_URLS = [
    ("VizieR B/psr",
     "https://vizier.cds.unistra.fr/viz-bin/VizieR-4?"
     "-source=B/psr&-out.max=unlimited&-out=PSRJ+P0&-oc.form=csv"),
    ("VizieR VII/245",
     "https://vizier.cds.unistra.fr/viz-bin/VizieR-4?"
     "-source=VII/245&-out.max=unlimited&-out=PSR+P0&-oc.form=csv"),
]


def fetch_url(url, label):
    print(f"  Fetching {label}...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "KishLattice/1.0"})
        with urllib.request.urlopen(req, timeout=90) as r:
            c = r.read().decode("utf-8", errors="replace")
            print(f"  {len(c):,} bytes received")
            return c
    except Exception as ex:
        print(f"  Failed: {ex}")
    return None


def parse_csv(content):
    lines = content.splitlines()
    hdr = None
    for i, line in enumerate(lines):
        if not line.strip() or line.startswith("#"):
            continue
        hdr = i
        break
    if hdr is None:
        return []
    reader = csv.DictReader(io.StringIO("\n".join(lines[hdr:])))
    results = []
    for row in reader:
        name = next((row[k].strip() for k in ("PSRJ","PSR","JName","BName","Name")
                     if k in row and row[k].strip()), None)
        p0_str = next((row[k].strip() for k in ("P0","p0","Period","period")
                       if k in row and row[k].strip()), None)
        if not name or not p0_str:
            continue
        try:
            p0 = float(p0_str)
            if p0 > 0:
                results.append((name, p0))
        except ValueError:
            pass
    return results


def compute_scalar(p0_ms):
    try:
        p = float(p0_ms)
        return math.log(p + 1.0) / LOG_K if 0 < p <= P0_MAX_MS else None
    except Exception:
        return None


def main():
    print("=" * 60)
    print("K2 ATNF Pulsar Periods Lake Builder (VizieR auto-fetch)")
    print("=" * 60)
    print(f"k_geo = {K_GEO:.10f}")
    print()

    PROMOTED.mkdir(parents=True, exist_ok=True)
    RAW_CACHE.parent.mkdir(parents=True, exist_ok=True)

    pulsars = []

    if RAW_CACHE.exists():
        print(f"Loading from cache: {RAW_CACHE.name}")
        pulsars = parse_csv(RAW_CACHE.read_text(encoding="utf-8"))
        print(f"  {len(pulsars):,} records from cache")
    else:
        for label, url in VIZIER_URLS:
            content = fetch_url(url, label)
            if content:
                pulsars = parse_csv(content)
                if len(pulsars) > 100:
                    RAW_CACHE.write_text(content, encoding="utf-8")
                    print(f"  Cached {len(pulsars):,} records -> {RAW_CACHE.name}")
                    break
                print(f"  Only {len(pulsars)} records — trying fallback")
            time.sleep(0.5)

    if not pulsars:
        print()
        print("Auto-fetch failed. Manual fallback:")
        print("  Visit: https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=B/psr")
        print("  Select PSRJ + P0, output CSV, save as:")
        print(f"  {RAW_CACHE}")
        raise SystemExit("No data.")

    now_ts  = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    scalars = []
    computed = failed = 0

    with OUT_REAL.open("w", encoding="utf-8") as fout:
        for name, p0_s in pulsars:
            p0_ms = p0_s * 1000.0
            s = compute_scalar(p0_ms)
            if s is None:
                failed += 1
                continue
            computed += 1
            scalars.append(s)
            fout.write(json.dumps({
                "entity_id": str(uuid.uuid4()),
                "domain":    "stellar_rotation",
                "volume":    5,
                "lake_id":   "k2_pulsar_periods",
                "geometry_payload": {"coordinates": [], "dimensionality": 0,
                                     "geometry_type": "stellar_rotation"},
                "scalar_kls": s, "scalar_klc": s,
                "meta": {
                    "source":           "ATNF Pulsar Catalogue via VizieR (B/psr)",
                    "ingest_timestamp": now_ts, "sovereign": True,
                    "audit_status":     "mondy_verified_2026-04",
                    "scalarization":    "log(P0_ms + 1) / log(k_geo)",
                    "kinematic_type":   "spin_period",
                    "pulsar_name":      name, "p0_seconds": p0_s, "p0_ms": p0_ms,
                },
                "_raw_payload": {"name": name, "p0_s": p0_s, "p0_ms": p0_ms},
            }, ensure_ascii=False) + "\n")

    print(f"\ntotal={len(pulsars):,}  computed={computed:,}  failed={failed:,}")
    if scalars:
        print(f"scalar range: {min(scalars):.4f} to {max(scalars):.4f}  "
              f"mean={sum(scalars)/len(scalars):.4f}")
        g = sum(1 for s in scalars if 1.05 <= s <= 1.67)
        print(f"Gap 1 records (1.05-1.67): {g:,}")
    print(f"-> {OUT_REAL.name}")
    print()
    print("Set k2_pulsar_periods to enabled:true in configs/volumes.json")


if __name__ == "__main__":
    main()