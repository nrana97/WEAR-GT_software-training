# Lesson 2: Detect events and divide a trace into cycles

**Goal:** locate repeatable peaks in a synthetic movement signal, translate timing constraints into samples, and build unambiguous cycle boundaries.

**Allow 45–60 minutes** for detection experiments and visual review.

## Define what an event means

An event is a time or index chosen according to a rule. A peak in a teaching waveform is a useful candidate event, but it is not automatically heel strike, toe-off, or a valid control trigger. Those meanings require the appropriate measurement, labels, and validation.

Start with a signal where the event timing is known:

```python
import numpy as np
from scipy.signal import find_peaks

fs = 100
t = np.arange(1000) / fs
x = np.sin(2 * np.pi * t)
peaks, properties = find_peaks(x)
print(peaks[:4])  # [25, 125, 225, 325]
print(t[peaks[:4]])  # [0.25, 1.25, 2.25, 3.25]
```

At 1 Hz, one cycle lasts one second, or 100 samples. The first maximum occurs after a quarter cycle. Use known construction details to check results before trying noisy data.

## Distance is in samples

`find_peaks` can require a minimum separation between retained peaks. If the separation is specified in seconds, convert it with the sampling rate:

```python
minimum_interval_s = .5
distance_samples = int(np.ceil(minimum_interval_s * fs))
peaks, properties = find_peaks(x, distance=distance_samples, prominence=.5)
```

Using `ceil` ensures the requested minimum duration is not rounded down. At 100 Hz, 0.505 s becomes 51 samples. This threshold encodes an assumption about the fastest acceptable events. Set it too large and real peaks will be suppressed; too small and noise may create extras.

## Height and prominence differ

Height compares a peak to an absolute y-value. Prominence describes how much a peak stands above its surrounding baseline according to the peak-finding algorithm. A baseline offset changes height but may leave prominence largely unchanged.

```python
rng = np.random.default_rng(3)
noisy = x + rng.normal(0, .08, len(x))
unrestricted, _ = find_peaks(noisy)
selected, _ = find_peaks(noisy, distance=50, prominence=.5)
print(len(unrestricted), len(selected))
```

Expect many more unrestricted local maxima. The exact selected count depends on data and thresholds. Inspect the trace rather than tuning until one sample happens to give the desired number.

## Review detections visually

```python
import matplotlib.pyplot as plt

plt.plot(t, noisy, label="signal")
plt.plot(t[selected], noisy[selected], "x", label="candidate events")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (a.u.)")
plt.legend()
plt.show()
```

Look for missed events and extra detections near noise bursts. Test more than one random seed and movement frequency. An algorithm that works on only one synthetic recording has weak evidence of robustness.

## Consecutive events define cycles

For peak indices `a` and `b`, use the half-open segment `x[a:b]`. It contains `a` through `b-1`, so the boundary sample is not included in both adjacent cycles.

```python
for a, b in zip(peaks[:-1], peaks[1:]):
    segment = x[a:b]
    duration_s = (b - a) / fs
    print(a, b, duration_s, len(segment))
```

Ten detected peaks define nine complete between-peak cycles. The data before the first peak and after the last peak are partial cycles and are excluded from this task. Duration uses the event-to-event interval; it is not `(len(segment)-1)/fs` under this definition.

## Failure cases to plan for

A flat trace yields no peaks. One event yields no complete cycle. A sign reversal turns maxima into minima. Irregular timestamps make a constant `fs` interpretation inaccurate. Missing values and saturated regions can invalidate event timing even if a function returns indices.

## Try it

1. Confirm the ten known event locations in the clean 1 Hz example.
2. Change the frequency to 2 Hz. Determine a valid minimum separation before running detection.
3. Add a constant offset and compare height-based with prominence-based detection.
4. Add one short high-amplitude artifact. Show how it can create a plausible-looking false event.
5. Write a report paragraph distinguishing a detected peak from a validated gait event. Include one additional measurement you would need to validate timing.

Next: [Features and windows](03_features.md)
