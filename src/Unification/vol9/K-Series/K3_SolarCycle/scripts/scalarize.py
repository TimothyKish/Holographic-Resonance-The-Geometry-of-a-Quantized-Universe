"""
scalarize.py -- K3_SolarCycle
Two scalar modes:
  - Annual mean sunspot number: log(sn + 1) / log(k_geo)
  - Cycle interval: log(interval_days + 1) / log(k_geo)
"""
import json, os, math

PI = math.pi; K_GEO = 16/PI; LOG_K = math.log(K_GEO)

PROMOTED_PATH   = os.path.join(os.path.dirname(__file__), "..", "..", "..", "lakes",
                                "inputs_promoted", "k3_solar_cycle_promoted.jsonl")
SCALARIZED_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "lakes",
                                "unified", "k3_solar_cycle_scalarized.jsonl")
os.makedirs(os.path.dirname(SCALARIZED_PATH), exist_ok=True)

def scalarize():
    records = []
    with open(PROMOTED_PATH, encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line.strip()))

    out = []
    for r in records:
        mtype = r.get("measurement_type", "")
        if mtype == "cycle_interval":
            # Primary scalar for P26: interval in days
            val = float(r["interval_days"])
        elif mtype == "annual_mean":
            # Secondary scalar: sunspot number amplitude
            val = float(r["sunspot_number_annual_mean"])
        else:
            val = float(r.get("interval_days", r.get("sunspot_number_annual_mean", 1)))

        if val <= 0:
            val = 0.01  # guard against zero

        scalar = math.log(val + 1.0) / LOG_K
        s = dict(r)
        s["kish_scalar"]   = round(scalar, 8)
        s["scalar_input"]  = round(val, 4)
        s["scalar_source"] = "interval_days" if mtype == "cycle_interval" else "sunspot_number"
        s["k_geo"]         = round(K_GEO, 10)
        s["n_approx"]      = round(scalar * PI, 4)
        s["nearest_n"]     = round(scalar * PI)
        out.append(s)

    with open(SCALARIZED_PATH, "w", encoding="utf-8") as f:
        for s in out:
            f.write(json.dumps(s) + "\n")

    intervals = [r for r in out if r.get("measurement_type") == "cycle_interval"]
    annual    = [r for r in out if r.get("measurement_type") == "annual_mean"]

    print(f"[K3_SolarCycle] scalarize complete — {len(out)} records")
    print(f"  Annual means: {len(annual)}  |  Cycle intervals: {len(intervals)}")
    if intervals:
        iv_days = [r["scalar_input"] for r in intervals]
        print(f"  Interval range: {min(iv_days):.0f} - {max(iv_days):.0f} days")
        print(f"  ~11yr = 4017 days → scalar = {math.log(4018)/LOG_K:.4f}, N~{math.log(4018)/LOG_K*PI:.2f}")
    print(f"  Output: {SCALARIZED_PATH}")

if __name__ == "__main__":
    scalarize()