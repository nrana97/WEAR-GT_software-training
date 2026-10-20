# Filtering and artifacts

Start with a uniformly sampled finite signal. A low-pass filter attenuates high frequencies; a high-pass attenuates slow variation; a band-pass retains a chosen range. Cutoff is not a brick wall. Filter choices depend on both sensor modality and task; an IMU cutoff is not an EMG preprocessing recipe.

```python
from scipy.signal import butter, sosfiltfilt
sos = butter(4, 5, fs=100, output="sos")
filtered = sosfiltfilt(sos, signal)
```

Second-order sections improve numerical stability. Forward-backward filtering uses future samples and is offline only. It changes the effective magnitude response and has edge effects. A streaming filter needs causal state and delay characterization. Do not filter across unhandled dropouts.

**Try:** mix a 1 Hz sine with a 20 Hz sine, low-pass at 5 Hz, and compare residual RMS. Explain the difference between an artifact and genuine rapid movement.
