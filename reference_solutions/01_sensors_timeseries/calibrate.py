import numpy as np

def convert_counts(counts, vref=3.3, max_count=4095, zero_v=1.65, sensitivity_v_per_g=0.33):
    """Convert calibrated ADC counts to g, preserving NaNs."""
    x = np.asarray(counts, dtype=float)
    if not all(np.isfinite(v) and v > 0 for v in (vref, max_count, sensitivity_v_per_g)) or not np.isfinite(zero_v):
        raise ValueError("Invalid calibration")
    if np.isinf(x).any() or ((x < 0) | (x > max_count)).any():
        raise ValueError("Counts outside ADC range")
    return (x / max_count * vref - zero_v) / sensitivity_v_per_g

def sampling_rate(t):
    """Estimate Hz from valid strictly increasing seconds."""
    t = np.asarray(t, dtype=float)
    if t.ndim != 1 or len(t) < 2 or not np.isfinite(t).all() or (np.diff(t) <= 0).any():
        raise ValueError("Need increasing finite timestamps")
    return float(1 / np.median(np.diff(t)))
