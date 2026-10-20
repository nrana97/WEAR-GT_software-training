# Lesson 3: Audit a recording before cleaning it

**Goal:** detect several independent kinds of data-quality problems and explain what the evidence does and does not establish.

**Allow 45–60 minutes**, then reserve another 30 minutes to write your first short quality report.

## An audit answers “what arrived?”

Cleaning changes data. An audit describes the original data so that the team can decide what changes are defensible. Keep the raw recording immutable, report its dimensions and timing, and compute flags before interpolation or filtering hides problems.

Start with familiar pandas inspection:

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({
    "timestamp_s": [0, .01, .02, .06, .07, .08],
    "raw": [2048, np.nan, 4095, 2050, 0, np.inf],
})
print(df.head())
print(df.dtypes)
print(df.describe())
```

A numeric dtype does not guarantee a valid measurement. `describe()` is useful but does not replace explicit checks, particularly for infinity and time ordering.

## Missing values and missing rows

There are two different failure patterns:

1. A timestamp exists but its sensor value is NaN or infinity.
2. Entire samples are absent, leaving a long interval between neighboring rows.

```python
x = df["raw"].to_numpy(dtype=float)
finite = np.isfinite(x)
missing_values = int((~finite).sum())  # 2

t = df["timestamp_s"].to_numpy(dtype=float)
dt = np.diff(t)
gap_after = np.flatnonzero(dt > 1.5 * np.median(dt))
print(gap_after.tolist())             # [2]
```

`df.isna()` catches NaNs but does not count infinity. The audit contract treats both as missing/unusable sensor values. Missing rows will not appear in a NaN count at all. Report both timing gaps and missing values.

## Saturation and clipping

A rail is a sensor/ADC limit. In the teaching ADC, counts at 0 or 4095 are flagged; finite values outside those limits are also flagged by the checkpoint audit.

```python
saturated = finite & ((x <= 0) | (x >= 4095))
print(np.flatnonzero(saturated))  # [2, 4]
```

If a signal hits its upper limit, the true amplitude could be higher than the stored value. Replacing it with an interpolated estimate does not restore the missing physical information. A single rail-valued sample is evidence to inspect; a long plateau at the rail is stronger evidence of clipping. The project converter rejects out-of-range counts, while the audit reports them. Validation and diagnosis serve different purposes.

## Offset, drift, and flat channels

Offset is a baseline displacement. Drift is a changing baseline. A constant channel may indicate a stuck sensor, but it can also represent an unmoving device or a quantity that genuinely is constant.

```python
t = np.arange(1000) / 100
motion = np.sin(2 * np.pi * 1.5 * t)
with_offset = motion + 0.4
with_drift = motion + 0.05 * t
flat = np.full_like(t, 2.0)
```

Plot these together in separate panels. A summary mean cannot distinguish a fixed offset from part of a movement, and an overall standard deviation can conceal a short flat section. Inspect both the full session and shorter intervals. Do not declare a hardware failure solely because a statistical threshold fired.

## Make the report reproducible

A useful report identifies the file, assumptions, counts, locations, and next actions. For the six-row example:

| Check | Finding | Interpretation |
|---|---|---|
| Typical interval | 0.01 s | Nominal rate near 100 Hz |
| Missing/unusable values | 2 | NaN and infinity need a policy |
| Rail/out-of-range values | 2 | Inspect for clipping |
| Timing gaps | After position 2 | A 0.04 s interval interrupts the trace |

List the units of thresholds. “Above 4095” only makes sense for the raw-count channel. The same threshold has no useful interpretation on a calibrated g channel.

## Try it

1. Recreate the table and counts above without modifying `df`.
2. Give the DataFrame row labels `[10, 20, 30, 40, 50, 60]`. Show why a positional index of 2 is not the same as label 2.
3. Generate a 20-second trace with a 1-second flat section and a slow drift. Plot full and zoomed views. Which summary statistics miss the local problem?
4. Write a half-page report with observations, possible explanations, and recommended follow-up. Keep those three categories distinct.
5. Propose separate policies for a single missing sample, a 2-second disconnect, and 50 consecutive saturated samples. Explain when discarding a segment is more honest than filling it.

**Ready for the project when:** you can convert units, validate timestamps, locate rather than merely count problems, and justify why the raw file should remain unchanged.

Continue: [Project](../project/README.md) · [Checkpoint](../checkpoint/README.md)
