import numpy as np
import pandas as pd
from scipy.signal import find_peaks

def cycle_features(x, fs, min_interval_s=0.5, prominence=0.5):
    """Detect synthetic movement peaks and summarize consecutive cycles."""
    x = np.asarray(x, dtype=float)
    if x.ndim != 1 or not len(x) or not np.isfinite(x).all():
        raise ValueError("Invalid signal")
    if not np.isfinite(fs) or fs <= 0 or not np.isfinite(min_interval_s) or min_interval_s <= 0 or not np.isfinite(prominence) or prominence < 0:
        raise ValueError("Invalid event settings")
    peaks, _ = find_peaks(x, distance=max(1,int(np.ceil(fs*min_interval_s))), prominence=prominence)
    rows=[]
    for a,b in zip(peaks[:-1],peaks[1:]):
        v=x[a:b]
        rows.append((a,b,(b-a)/fs,v.mean(),np.sqrt(np.mean(v*v)),np.ptp(v)))
    return peaks, pd.DataFrame(rows, columns=['start','stop','duration_s','mean','rms','peak_to_peak'])
