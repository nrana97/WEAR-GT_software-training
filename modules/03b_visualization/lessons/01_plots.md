# Lesson 1: Make plots that help someone inspect a recording

**Goal:** build labeled multi-panel sensor plots that preserve missing data and make timing comparisons clear.

**Allow 45–60 minutes**, including saving and inspecting a figure. A passing file-exists test is not enough to establish a useful visualization.

## Decide what the viewer needs to answer

For session review, the first questions are usually: which signal is this, what are its units, when did something happen, and is the measurement trustworthy? A plot that cannot answer those questions is incomplete even if it looks polished.

Raw ADC counts and calibrated acceleration need separate labels. Two signals with different units generally need separate panels rather than a shared y-axis. A shared x-axis helps a viewer align events across sensors without mentally translating time scales.

## Construct a multi-channel example

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

t = np.arange(500) / 100
df = pd.DataFrame({
    "timestamp_s": t,
    "acc_z": 1 + .15 * np.sin(2 * np.pi * 1.5 * t),
    "gyro_y": 30 * np.cos(2 * np.pi * 1.5 * t),
})
df.loc[200:220, "acc_z"] = np.nan
```

The accelerometer example uses g and the gyroscope degrees/s. These are synthetic signals, not an anatomical model. The gap is intentional and should remain visible.

## Use the object-oriented plotting interface

```python
fig, grid = plt.subplots(2, 1, sharex=True, squeeze=False, figsize=(10, 6))
axes = grid[:, 0]

axes[0].plot(df.timestamp_s, df.acc_z)
axes[0].set_ylabel("acc_z (g)")
axes[0].set_title("Synthetic session review")
axes[1].plot(df.timestamp_s, df.gyro_y)
axes[1].set_ylabel("gyro_y (degrees/s)")
axes[1].set_xlabel("Time (s)")
for ax in axes:
    ax.grid(alpha=.2)
fig.tight_layout()
fig.savefig("practice_review.png", dpi=140)
plt.show()
plt.close(fig)
```

`squeeze=False` ensures a two-dimensional axes grid even for one channel. Selecting `grid[:,0]` produces the one-dimensional array required by the project. Without that precaution, one-channel and multi-channel code can receive different object shapes.

Use the `fig` and `ax` objects explicitly rather than relying on whichever plot is currently active. Close figures when a script finishes with them to avoid accumulating resources across many sessions.

## Preserve missing samples as breaks

Matplotlib breaks a line at NaN values. Do not drop rows only from the values or only from time; that can misalign the two arrays. Do not fill missing values with zero just to get a continuous line.

```python
values = np.array([1, np.inf, 2, np.nan, 3])
plot_values = np.where(np.isfinite(values), values, np.nan)
```

This converts unusable infinity to a visible break while retaining the original DataFrame. A review plot can reveal a gap; it should not silently repair it.

## Scale choices change interpretation

Independent y-scales are useful for different units, but they can make a tiny variation look as large as a major change. Label clearly and include context. When comparing two recordings of the same quantity, consider consistent y-limits to avoid exaggerating one recording's variation.

Avoid connecting disconnected sessions with a single continuous line. Identify session boundaries or use separate panels. If a trace is densely sampled, alpha or thinner lines may help; careless downsampling can hide spikes and dropouts.

## Validate the timeline before drawing

Reject nonfinite or nonincreasing timestamps and require unit strings for all sensor columns. A shuffled timeline can create zigzags unrelated to physical behavior. A missing unit makes numerical interpretation impossible. Error messages should help the user repair the input, not produce a plausible-looking misleading figure.

## Try it

1. Save the worked figure and open the PNG. Confirm labels are not cut off and the acceleration gap is visible.
2. Add a third channel with units of N. Make sure panel creation still works.
3. Run the same code with only one sensor channel. Verify your axes handling remains consistent.
4. Compare plots with fixed and automatic y-limits for two recordings with different amplitudes. Write which comparison is fairer and why.
5. Introduce an infinity and a repeated timestamp in separate copies. Show missing-value handling and timeline rejection.

**Review criterion:** another teammate should identify every channel, unit, and plotted interval without reading your code.

Next: [Replay and live views](02_live_view.md)
