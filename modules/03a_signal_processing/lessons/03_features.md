# Lesson 3: Build feature tables with timing and provenance

**Goal:** turn windows or event-defined cycles into clearly defined numerical features without losing the information needed for honest evaluation.

**Allow 45–60 minutes**, plus 30 minutes to compare window choices on a generated signal.

## Why summarize a waveform?

A model may not need every raw sample. A feature compresses a segment into a quantity such as average, variability, RMS, or range. The tradeoff is information loss: different waveforms can have the same feature values.

For a segment `v`, this training uses:

```python
import numpy as np

v = np.array([1, -1, 1, -1], dtype=float)
mean = v.mean()                      # 0
std = v.std(ddof=0)                   # 1
rms = np.sqrt(np.mean(v ** 2))        # 1
peak_to_peak = np.ptp(v)              # 2
```

Mean describes baseline. Population standard deviation describes spread about that baseline. RMS measures the square-root average squared amplitude relative to zero. Peak-to-peak measures the difference between maximum and minimum, so a single extreme artifact can dominate it.

The project explicitly uses `ddof=0`. pandas Series `.std()` defaults to `ddof=1`, so switching methods without specifying the convention changes results.

## Work through an offset example

```python
shifted = v + 3
print(shifted.mean())                  # 3
print(shifted.std(ddof=0))             # 1
print(np.sqrt(np.mean(shifted ** 2)))  # sqrt(10), about 3.162
print(np.ptp(shifted))                 # 2
```

Mean and RMS change; standard deviation and range do not. This shows why RMS is not simply another name for standard deviation. Calibration errors can change features even if movement shape is unchanged.

## Fixed windows and overlap

A window of 100 samples at 100 Hz represents one second of nominal sampled content. With `step=50`, neighboring windows overlap by 50 samples.

```python
x = np.arange(250, dtype=float)
window, step = 100, 50
bounds = [(start, start + window)
          for start in range(0, len(x) - window + 1, step)]
print(bounds)  # [(0,100), (50,150), (100,200), (150,250)]
```

Only include complete windows for this task. A shorter trailing segment is discarded rather than padded with zeros. State that choice in the report. If the signal is shorter than a window, return an empty feature table with the expected columns.

Long windows provide more context but can blend transitions between activities. Short windows respond faster but can produce noisier estimates. Overlap produces more rows, not proportionally more independent information.

## Build a table instead of parallel unnamed lists

```python
import pandas as pd

rows = []
for start, stop in bounds:
    segment = x[start:stop]
    rows.append({
        "start": start,
        "stop": stop,
        "mean": segment.mean(),
        "std": segment.std(ddof=0),
        "rms": np.sqrt(np.mean(segment ** 2)),
    })
features = pd.DataFrame(rows)
print(features.head())
```

Named columns make assumptions reviewable. Preserve `start` and `stop` as half-open sample positions, not seconds. Convert to seconds explicitly when displaying time. For event cycles, duration comes from consecutive event indices divided by `fs`.

## Preserve where each row came from

A real feature table should also carry subject, session, sensor placement, and time bounds. These columns explain provenance, but identifiers should not automatically become model inputs.

For example, two overlapping windows from subject S01 can share half their raw samples. Randomly putting one in training and the other in test leaks nearly identical observations across the split. Group by subject or session according to the generalization question before fitting preprocessing or a model.

Do not interpret an activity label crossing a window boundary casually. Choose a rule such as excluding ambiguous transition windows, and document it. Synthetic examples with one class per segment avoid some of this complexity; real labels will not always be so clean.

## Try it

1. Calculate features by hand for `[2, 2, 2, 2]`. Expected mean=2, std=0, RMS=2, range=0.
2. Use 250 samples, window=100, step=100. Explain which 50 samples are discarded.
3. Compare window sizes of 50, 100, and 200 on a 1.5 Hz waveform. Plot RMS against window start time.
4. Add one extreme artifact. Which feature changes most, and does that change describe movement?
5. Design a feature-table schema including subject and session IDs. Mark which columns are predictors and which are provenance.

**Ready for the checkpoint when:** you can explain each feature's units, indexing convention, missing-data policy, and limitations.

Continue: [Project](../project/README.md) · [Checkpoint](../checkpoint/README.md)
