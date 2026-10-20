import numpy as np
import pandas as pd
from scipy.signal import butter, sosfiltfilt

def _signal(x):
    x = np.asarray(x, dtype=float)
    if x.ndim != 1 or len(x) == 0 or not np.isfinite(x).all():
        raise ValueError("Need nonempty finite 1D signal")
    return x

def _integer(v):
    return isinstance(v, (int, np.integer)) and not isinstance(v, bool) and v > 0

def lowpass(x, fs, cutoff_hz=5.0, order=4):
    """Offline zero-phase Butterworth filtering; never a streaming operation."""
    x = _signal(x)
    if not np.isfinite(fs) or fs <= 0 or not np.isfinite(cutoff_hz) or not 0 < cutoff_hz < fs/2 or not _integer(order):
        raise ValueError("Invalid filter settings")
    return sosfiltfilt(butter(order, cutoff_hz, fs=fs, output='sos'), x)

def window_features(x, window=100, step=50):
    """Extract complete half-open windows and population statistics."""
    x = _signal(x)
    if not _integer(window) or not _integer(step):
        raise ValueError("Invalid window/step")
    rows = []
    for start in range(0, len(x)-window+1, step):
        v = x[start:start+window]
        rows.append((start, start+window, v.mean(), v.std(ddof=0), np.sqrt(np.mean(v*v))))
    return pd.DataFrame(rows, columns=['start','stop','mean','std','rms'])
