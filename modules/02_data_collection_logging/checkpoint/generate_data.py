"""Generate a reproducible synthetic recording. Run from this folder."""
from pathlib import Path
import numpy as np
import pandas as pd

def generate(seed=42):
    rng = np.random.default_rng(seed)
    t = np.arange(1000) / 100
    raw = 2048 + 400 * np.sin(2 * np.pi * 1.5 * t) + rng.normal(0, 8, len(t))
    raw[200:205] = np.nan
    raw[500] = 4095
    return pd.DataFrame({"timestamp_s": t, "raw": raw,
                         "signal": np.sin(2 * np.pi * 1.5 * t) + rng.normal(0, .03, len(t))})

if __name__ == "__main__":
    path = Path("sample.csv")
    generate().to_csv(path, index=False)
    print(f"Wrote {path}: 100 Hz, 10 seconds, synthetic data only")
