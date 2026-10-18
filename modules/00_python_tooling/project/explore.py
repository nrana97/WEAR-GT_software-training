"""Walking Data Explorer: starter file.

Fill in each function below. Run `pytest` in this folder to check your work.
Read project/README.md first for the full description of each function.
"""

import matplotlib

matplotlib.use("Agg")  # draw to files, not to a window
import matplotlib.pyplot as plt  # noqa: E402,F401
import numpy as np  # noqa: E402,F401
import pandas as pd  # noqa: E402,F401


def load_data(path):
    """Read a recording from a CSV file and return it as a DataFrame."""
    raise NotImplementedError("Write load_data")


def summarize(df):
    """Return a dict summarizing the recording.

    Keys:
        "n_samples"      number of rows (int)
        "duration_s"     last timestamp minus first timestamp (float)
        "sample_rate_hz" 1 / the median time step between samples (float)
        "column_means"   dict mapping each sensor column name to its mean
                         (every column except "timestamp_s")
    """
    raise NotImplementedError("Write summarize")


def acc_magnitude(df):
    """Return a Series: sqrt(acc_x^2 + acc_y^2 + acc_z^2) for every row."""
    raise NotImplementedError("Write acc_magnitude")


def count_steps(df, window=5):
    """Return the number of steps in the recording (an int).

    Method:
        1. Compute the acceleration magnitude.
        2. Smooth it with a centered rolling mean of `window` samples.
        3. Count the points where the smoothed signal crosses UPWARD through
           its own mean. Each upward crossing is one step.
    """
    raise NotImplementedError("Write count_steps")


def plot_signals(df, out_path):
    """Save a PNG with three stacked panels sharing a time axis:
    acceleration (acc_x, acc_y, acc_z), rotation rate (gyro_x, gyro_y, gyro_z),
    and acceleration magnitude. Label every axis with units and add a title.
    Return None.
    """
    raise NotImplementedError("Write plot_signals")
