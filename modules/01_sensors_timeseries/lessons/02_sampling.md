# Lesson 2: Sampling rate, timestamps, and aliasing

**Goal:** infer a recording's timing from timestamps, distinguish gaps from ordinary spacing, and explain why sampling can hide motion.

**Allow 45–60 minutes**, including the sampling experiment. Keep time in seconds throughout.

## Samples are observations at particular times

A 100 Hz sensor ideally produces one measurement every 0.01 seconds. Frequency describes observations per second; period describes seconds per observation:

```python
sample_rate_hz = 100.0
period_s = 1.0 / sample_rate_hz  # 0.01
```

A 1000-sample array at 100 Hz has timestamps from 0 through 9.99 s. The elapsed time between first and last samples is 9.99 s, while the acquisition covers 1000 nominal sample intervals. State which duration you report rather than switching conventions silently.

```python
import numpy as np

t = np.arange(1000) / 100
print(len(t), t[0], t[-1])  # 1000, 0.0, 9.99
```

Use `np.arange(n) / fs` when you know the sample count. `np.linspace(0, 10, 1000)` includes both endpoints by default, so its interval is not exactly 0.01 s.

## Inspect before estimating

The differences between neighboring times reveal timing problems:

```python
t = np.array([0, 0.01, 0.02, 0.05, 0.06])
dt = np.diff(t)
print(dt)                       # [0.01 0.01 0.03 0.01]
print(1 / np.median(dt))         # about 100 Hz
print(1 / np.mean(dt))           # about 66.7 Hz
```

The median describes typical spacing despite one long gap. It does not prove that all samples arrived or that the hardware clock is accurate. If most intervals are abnormal, even a median can be misleading.

Before dividing, require a one-dimensional finite time array, at least two observations, and strictly positive differences. A duplicate timestamp produces zero; decreasing times can indicate a reset, reordered packets, or concatenated sessions. Diagnose those cases before deciding to sort or discard anything.

```python
if t.ndim != 1 or len(t) < 2:
    raise ValueError("Need at least two timestamps")
if not np.isfinite(t).all() or (np.diff(t) <= 0).any():
    raise ValueError("Invalid timeline")
```

## Gaps and jitter are different

Jitter is variation in sample timing. A gap is an unusually long interval, possibly caused by missing observations. In this exercise, a gap is any interval greater than 1.5 times the median interval.

```python
typical_dt = np.median(dt)
gap_after = np.flatnonzero(dt > 1.5 * typical_dt)
print(gap_after)  # [2]: the gap follows sample position 2
```

These are positional indices, not DataFrame row labels. A 0.03 s interval in an otherwise 0.01 s stream suggests two missing nominal sample positions. It does not identify why they are missing. Sensor sequence numbers provide stronger loss evidence than timestamps alone.

## What aliasing looks like

Sampling cannot distinguish every possible continuous signal. At 100 Hz, a 70 Hz sine produces the same sampled values as a negative 30 Hz sine:

```python
import matplotlib.pyplot as plt

fs = 100
t = np.arange(100) / fs
high = np.sin(2 * np.pi * 70 * t)
alias = -np.sin(2 * np.pi * 30 * t)
print(np.allclose(high, alias))  # True, within floating-point tolerance

plt.plot(t[:20], high[:20], "o-", label="70 Hz sampled")
plt.plot(t[:20], alias[:20], "x--", label="negative 30 Hz sampled")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (a.u.)")
plt.legend()
plt.show()
```

The Nyquist limit is half the sampling rate: 50 Hz here. Sampling above twice the highest frequency of interest is a theoretical starting point; practical acquisition also needs filtering and margin. Once unwanted high-frequency content has aliased into stored data, applying a digital filter afterward cannot recover the original source.

## Downsampling needs thought

Selecting `x[::5]` from a 100 Hz recording leaves 20 observations per second. Frequencies above the new 10 Hz Nyquist limit can fold into the retained band unless they are attenuated before downsampling. Never assume a slower plot or smaller CSV is equivalent information.

## Try it

1. Generate 10 seconds at 50, 100, and 200 Hz. Print sample count, last timestamp, and median spacing.
2. Delete samples 100–109 from a 100 Hz recording. Find the index before the gap and compare mean/median rate estimates.
3. Add one duplicated time and one NaN timestamp to separate copies. Confirm your validation rejects both.
4. Repeat the aliasing experiment with 80 Hz and 20 Hz. Explain the sign relationship.
5. Write a paragraph distinguishing sampling rate, timestamp jitter, packet loss, and host arrival delay.

**Check yourself:** 500 samples at 50 Hz end at 9.98 s. Deleting positions 100–109 leaves a gap after position 99 in the shortened array. A good median rate does not mean there were no dropouts.

Next: [Data-quality checks](03_quality.md)
