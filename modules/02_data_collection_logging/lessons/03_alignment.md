# Lesson 3: Align streams without inventing measurements

**Goal:** put offset-corrected streams on a common grid while preserving out-of-range coverage and long gaps as missing data.

**Allow 60–75 minutes.** Work through the interpolation arithmetic before implementing the checkpoint.

## Alignment answers a specific question

Suppose an IMU samples at 100 Hz and another sensor at 50 Hz. To compare them sample by sample, choose a reference timeline and estimate each signal at those times. This is resampling. It changes the representation; it does not increase the original information content.

```python
import numpy as np

a_t = np.array([0, .1, .2, .6])
a_x = np.array([0, 1, 2, 6])
grid = np.array([-.1, 0, .05, .1, .2, .3, .6, .7])
```

The checkpoint returns exactly the supplied grid. It must not secretly choose a new rate or shift the requested times.

## Correct clocks before interpolating

If B's time is 0.2 s ahead, add `offset_b_s=-0.2` before alignment. This is separate from interpolation:

```python
b_t = np.array([.2, .4, .6, .8])
b_reference_t = b_t - .2
```

Always validate that corrected times remain finite and strictly increasing. Duplicates and reordered times need a policy before interpolation; this task rejects them rather than silently sorting or averaging.

## Linear interpolation by hand

Between two observations `(t0,x0)` and `(t1,x1)`, use:

```python
t0, x0 = 0.0, 0.0
t1, x1 = 0.1, 1.0
target = 0.05
fraction = (target - t0) / (t1 - t0)
estimate = x0 + fraction * (x1 - x0)
print(estimate)  # 0.5
```

This assumes a straight-line change within the interval. It can be reasonable for a small gap in a smooth signal but can erase a sharp event or misrepresent an oscillatory waveform. The method needs a maximum acceptable gap defined in seconds.

## Find the neighboring observations

`np.searchsorted` returns an insertion position in a sorted array:

```python
position = np.searchsorted(a_t, .05)
print(position)  # 1
# Left neighbor is position-1; right neighbor is position.
```

At `.7`, the insertion position is the array length: there is no right neighbor. At `-.1`, there is no left neighbor. Those targets are outside coverage and must remain NaN. Beware `np.interp`'s default endpoint filling: it can make unobserved coverage look valid unless you explicitly handle boundaries.

## Use a decision order

For each target time:

1. If it matches an observation within the specified absolute tolerance, return that observation only if finite.
2. Otherwise require both a left and a right neighbor.
3. Require both neighboring values to be finite.
4. Require their time separation to be at most `max_gap_s`.
5. Interpolate only after every check passes; otherwise leave NaN.

Why exact matches first? A genuine observation at `.6` is still valid even if the preceding gap is long. With `max_gap_s=.21`, `.3` in A is missing because its neighbors are `.2` and `.6`, but `.6` itself is retained.

Floating-point timestamps may differ by tiny rounding errors. The checkpoint uses absolute tolerance `1e-12` for exact matches; do not use a default relative tolerance that becomes large for big clock values. A tolerance is an implementation convention, not evidence of synchronization accuracy.

## Carry quality information forward

After alignment, count missing output values and retain the original timestamps elsewhere. A perfectly rectangular table can contain much estimated data. For real analysis, useful additions include per-sample observed/interpolated flags, source gap size, and synchronization uncertainty.

## Try it

1. Calculate A's output on the example grid with `max_gap_s=.21`. Expected: NaN, 0, 0.5, 1, 2, NaN, 6, NaN.
2. Make the value at `.1` NaN. Explain why targets `.05` and `.15` must also become missing.
3. Correct B by −0.2 and calculate its values at `.1`, `.3`, and `.7`. Which is outside coverage?
4. Plot original observations as points and aligned output as a line. Keep long gaps visibly broken.
5. Explain in your report why a clock offset, interpolation limit, and sampling rate are three different parameters.

Continue: [Project](../project/README.md) · [Checkpoint](../checkpoint/README.md)
