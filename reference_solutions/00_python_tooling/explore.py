"""Walking Data Explorer: reference solution.

Try the project yourself before reading this.
"""

import matplotlib

matplotlib.use("Agg")  # draw to files, not to a window
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402


def load_data(path):
    """Read a recording from a CSV file and return it as a DataFrame."""
    return pd.read_csv(path)


def summarize(df):
    """Return a dict summarizing the recording."""
    t = df["timestamp_s"]
    # Median step, not mean: a few big gaps (dropouts) would distort the mean.
    typical_dt = t.diff().median()
    sensor_cols = [c for c in df.columns if c != "timestamp_s"]
    return {
        "n_samples": len(df),
        "duration_s": float(t.iloc[-1] - t.iloc[0]),
        "sample_rate_hz": float(1.0 / typical_dt),
        "column_means": {c: float(df[c].mean()) for c in sensor_cols},
    }


def acc_magnitude(df):
    """Return a Series: sqrt(acc_x^2 + acc_y^2 + acc_z^2) for every row."""
    return np.sqrt(df["acc_x"] ** 2 + df["acc_y"] ** 2 + df["acc_z"] ** 2)


def count_steps(df, window=5):
    """Return the number of steps: upward crossings of the smoothed magnitude's mean."""
    mag = acc_magnitude(df)
    smooth = mag.rolling(window=window, center=True, min_periods=1).mean()
    above = (smooth > smooth.mean()).to_numpy()
    # An upward crossing is a sample that is above where the previous one was not.
    crossings = above[1:] & ~above[:-1]
    return int(crossings.sum())


def plot_signals(df, out_path):
    """Save a PNG with acceleration, rotation rate, and magnitude panels."""
    t = df["timestamp_s"]
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    for col in ["acc_x", "acc_y", "acc_z"]:
        axes[0].plot(t, df[col], label=col, linewidth=0.8)
    axes[0].set_ylabel("Acceleration (m/s^2)")
    axes[0].set_title("Walking recording")
    axes[0].legend(loc="upper right")

    for col in ["gyro_x", "gyro_y", "gyro_z"]:
        axes[1].plot(t, df[col], label=col, linewidth=0.8)
    axes[1].set_ylabel("Rotation rate (deg/s)")
    axes[1].legend(loc="upper right")

    axes[2].plot(t, acc_magnitude(df), color="black", linewidth=0.8)
    axes[2].set_ylabel("Acc. magnitude (m/s^2)")
    axes[2].set_xlabel("Time (s)")

    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
