"""Level 0 checkpoint: reference solution.

Try the checkpoint yourself before reading this.
"""

import pandas as pd

TIME_COLUMN = "timestamp_s"


def _sort_and_dedupe(df):
    """Sort by time and keep the first row for each timestamp."""
    return (
        df.sort_values(TIME_COLUMN, kind="stable")
        .drop_duplicates(subset=TIME_COLUMN, keep="first")
        .reset_index(drop=True)
    )


def clean(df):
    """Return a cleaned copy: sorted, one row per timestamp, gaps filled."""
    out = _sort_and_dedupe(df)
    sensor_cols = [c for c in out.columns if c != TIME_COLUMN]
    # Interpolate along row order (rows are now in time order), then fill
    # any gaps left at the very start or end with the nearest valid value.
    out[sensor_cols] = (
        out[sensor_cols]
        .interpolate(method="linear", limit_direction="both")
    )
    return out


def report(raw, cleaned):
    """Return a dict describing what cleaning changed."""
    sensor_cols = [c for c in raw.columns if c != TIME_COLUMN]
    deduped = _sort_and_dedupe(raw)
    return {
        "rows_raw": len(raw),
        "rows_clean": len(cleaned),
        "duplicates_removed": len(raw) - len(cleaned),
        "was_sorted": bool(raw[TIME_COLUMN].is_monotonic_increasing),
        "missing_filled": int(deduped[sensor_cols].isna().sum().sum()),
    }
