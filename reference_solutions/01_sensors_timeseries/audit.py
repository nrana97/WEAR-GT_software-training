import numpy as np

def audit(df, max_count=4095):
    """Return independent timing, missing-value, and rail diagnostics."""
    t = df["timestamp_s"].to_numpy(dtype=float)
    x = df["raw"].to_numpy(dtype=float)
    if not np.isfinite(max_count) or max_count <= 0:
        raise ValueError("Invalid rail")
    if len(t) < 2 or not np.isfinite(t).all() or (np.diff(t) <= 0).any():
        raise ValueError("Invalid time")
    dt = np.diff(t)
    median = np.median(dt)
    finite = np.isfinite(x)
    return {"sample_rate_hz": float(1 / median), "missing_values": int((~finite).sum()),
            "saturated_samples": int((finite & ((x <= 0) | (x >= max_count))).sum()),
            "gap_after_indices": np.flatnonzero(dt > 1.5 * median).tolist()}
