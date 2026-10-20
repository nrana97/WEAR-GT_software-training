import json
import shutil
from pathlib import Path
import numpy as np
import pandas as pd

def write_session(df, metadata, directory):
    """Validate and write a new CSV/JSON session without overwriting."""
    required = ("session_id", "subject_id", "task", "sensor_placement", "firmware_version")
    if not all(isinstance(metadata.get(k), str) and metadata[k].strip() for k in required):
        raise ValueError("Missing metadata")
    try:
        payload = json.dumps(metadata, indent=2, allow_nan=False)
    except (ValueError, TypeError) as exc:
        raise ValueError("Metadata must be JSON serializable") from exc
    if "timestamp_s" not in df or len(df.columns) < 2 or not df.columns.is_unique:
        raise ValueError("Missing/duplicate columns")
    try:
        t = df["timestamp_s"].to_numpy(dtype=float)
    except (ValueError, TypeError) as exc:
        raise ValueError("Invalid timestamps") from exc
    if len(t) < 2 or not np.isfinite(t).all() or (np.diff(t) <= 0).any():
        raise ValueError("Invalid timestamps")
    if not all(pd.api.types.is_numeric_dtype(df[c]) for c in df if c != "timestamp_s"):
        raise ValueError("Sensors must be numeric")
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=False)
    try:
        df.to_csv(path / "samples.csv", index=False)
        (path / "metadata.json").write_text(payload)
    except Exception:
        shutil.rmtree(path)
        raise
    return path
