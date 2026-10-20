# Movement events and segmentation

For a synthetic periodic trace, peaks separated by a minimum duration can mark events. `scipy.signal.find_peaks` accepts a distance in samples and a prominence in signal units. Convert seconds to samples with `ceil(seconds * fs)`.

Peaks are candidate events, not clinically validated heel strikes. Sensor placement, direction, and walking speed affect timing. Compare detected events with known simulated peaks and inspect false positives. A pair of consecutive event indices defines a half-open segment `[start, stop)`; avoid counting the boundary twice.

**Try:** generate 10 seconds of `sin(2*pi*t)` at 100 Hz. Find ten peaks and test a second frequency. What happens if your minimum event separation is too large?
