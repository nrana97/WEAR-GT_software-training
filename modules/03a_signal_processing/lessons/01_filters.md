# Lesson 1: Filters, noise, and what preprocessing changes

**Goal:** choose a filter for a stated purpose, apply an offline Butterworth low-pass, and evaluate what changed instead of assuming a smoother signal is better.

**Allow 60–75 minutes**, including the frequency experiment. Install the root requirements to get SciPy.

## Define the signal you want to retain

A wearable recording can contain slow baseline variation, movement-related components, high-frequency interference, artifacts, and measurement noise. Those categories overlap in frequency. A rapid change might be interference, or it might be the event you need to detect.

A low-pass filter attenuates higher frequencies; a high-pass attenuates lower frequencies; a band-pass attenuates outside a selected range. “Attenuates” means reduces amplitude, not deletes perfectly. A cutoff is not a brick wall.

An IMU movement trace and raw EMG need different acquisition rates and preprocessing. The 5 Hz cutoff used below is a synthetic exercise setting, not a general wearable-sensor recommendation.

## Build a signal whose components you know

```python
import numpy as np
import matplotlib.pyplot as plt

fs = 100.0
t = np.arange(2000) / fs
movement = np.sin(2 * np.pi * 1 * t)
interference = .5 * np.sin(2 * np.pi * 20 * t)
x = movement + interference

plt.plot(t[:300], x[:300], label="mixture")
plt.plot(t[:300], movement[:300], label="known 1 Hz component")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (a.u.)")
plt.legend()
plt.show()
```

The known component is a ground truth available only because we constructed the data. In a real recording, a smoother trace may be a distorted trace; visual attractiveness is not a validation metric.

## Design in second-order sections

```python
from scipy.signal import butter, sosfiltfilt

sos = butter(4, 5.0, btype="lowpass", fs=fs, output="sos")
y = sosfiltfilt(sos, x)
```

`4` is the filter order; `5.0` is cutoff in Hz because we supplied `fs`. Second-order sections (`sos`) represent the filter as smaller numerical stages and are preferable to a single high-order coefficient polynomial for many applications.

Forward-backward filtering applies a filter in both directions. It avoids net phase shift in the interior but changes the magnitude response relative to one pass. It also requires future data and enough padding near boundaries. It is an offline method, not a live causal filter.

## Evaluate the result against a known target

```python
interior = slice(100, -100)
raw_error = np.sqrt(np.mean((x[interior] - movement[interior]) ** 2))
filtered_error = np.sqrt(np.mean((y[interior] - movement[interior]) ** 2))
print(raw_error, filtered_error)
```

The raw RMS error is about 0.354 for this example. The filtered interior error should be much smaller. Excluding boundaries makes the comparison less dominated by edge behavior; separately inspect those boundaries rather than pretending they do not matter.

An optional spectrum comparison makes attenuation easier to see:

```python
frequencies = np.fft.rfftfreq(len(x), d=1/fs)
raw_amplitude = np.abs(np.fft.rfft(x)) / len(x)
filtered_amplitude = np.abs(np.fft.rfft(y)) / len(y)
plt.plot(frequencies, raw_amplitude, label="raw")
plt.plot(frequencies, filtered_amplitude, label="filtered")
plt.xlim(0, 30)
plt.xlabel("Frequency (Hz)")
plt.ylabel("FFT magnitude / sample count")
plt.legend()
plt.show()
```

This is a simple magnitude comparison, not a fully normalized one-sided power spectral density estimate. Name the quantity you actually plotted.

## Validate and handle gaps first

Require finite one-dimensional input, positive finite sampling rate, cutoff strictly between zero and Nyquist, and a positive integer order. Very short arrays may not support the padding required by `sosfiltfilt`; report an error rather than silently choosing an unrelated method.

A NaN can contaminate many filtered values. Do not drop missing rows and pretend the remaining array is still uniformly sampled. Instead, process contiguous valid segments or use a documented bounded interpolation policy before filtering. Long gaps should remain separate segments.

## Try it

1. Compare cutoffs of 2, 5, and 15 Hz. Plot the same interval and compute interior error for each.
2. Replace the target with an 8 Hz component. Explain why 5 Hz filtering is now inappropriate for preserving that target.
3. Compare `sosfilt` with `sosfiltfilt`. The causal output will have transient and timing differences; mark the peak locations.
4. Insert a NaN and test what happens. Write a missing-data policy rather than silently filling it with zero.
5. Save a before/after figure and explain your selected cutoff in terms of the synthetic components.

Next: [Events and segmentation](02_events.md)
