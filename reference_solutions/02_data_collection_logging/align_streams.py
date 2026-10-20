import numpy as np
import pandas as pd

def _validate(t, minimum):
    if t.ndim != 1 or len(t) < minimum or not np.isfinite(t).all() or (np.diff(t) <= 0).any():
        raise ValueError("Invalid timeline")

def _resample(t, x, grid, gap):
    out = np.full(len(grid), np.nan)
    for i, target in enumerate(grid):
        pos = np.searchsorted(t, target)
        exact = next((j for j in (pos, pos-1) if 0 <= j < len(t) and abs(t[j]-target) <= 1e-12), None)
        if exact is not None:
            if np.isfinite(x[exact]): out[i] = x[exact]
        elif 0 < pos < len(t) and t[pos]-t[pos-1] <= gap + 1e-12 and np.isfinite(x[pos-1:pos+1]).all():
            out[i] = x[pos-1] + (x[pos]-x[pos-1]) * (target-t[pos-1])/(t[pos]-t[pos-1])
    return out

def align(a, b, grid, offset_b_s=0.0, max_gap_s=0.1):
    """Align offset-corrected streams without extrapolation or gap bridging."""
    grid = np.asarray(grid, dtype=float)
    _validate(grid, 1)
    if not np.isfinite(offset_b_s) or not np.isfinite(max_gap_s) or max_gap_s <= 0:
        raise ValueError("Invalid alignment parameters")
    arrays = []
    for frame, offset in ((a, 0), (b, offset_b_s)):
        t = frame['timestamp_s'].to_numpy(dtype=float) + offset
        _validate(t, 2)
        arrays.append(_resample(t, frame['value'].to_numpy(dtype=float), grid, max_gap_s))
    return pd.DataFrame({'timestamp_s':grid,'a':arrays[0],'b':arrays[1]})
