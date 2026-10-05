"""SYNTHETIC DEMONSTRATION DATA. Random points near Karachi's bounding box; NOT real observations."""
import numpy as np, pandas as pd
def make(n=150, seed=42):
    r = np.random.default_rng(seed)
    types = ["pothole", "waterlogging", "garbage", "road_damage", "open_drain"]
    df = pd.DataFrame({"code": [f"SYN-{i:05d}" for i in range(n)], "type": r.choice(types, n),
        "lat": r.uniform(24.82, 25.03, n), "lon": r.uniform(66.95, 67.20, n),
        "severity": r.uniform(0.2, 1, n).round(2), "n_observations": r.integers(1, 7, n),
        "evidence_confidence": r.uniform(0.3, 0.95, n).round(2), "traffic_exposure": r.uniform(0, 1, n).round(2),
        "date": pd.Timestamp("2025-01-01") + pd.to_timedelta(r.integers(0, 365, n), "D"),
        "is_synthetic": True})
    return df
if __name__ == "__main__":
    make().to_csv("data/demo/synthetic_incidents.csv", index=False); print("written")
