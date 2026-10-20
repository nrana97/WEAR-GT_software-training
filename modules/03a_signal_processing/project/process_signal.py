"""Level 3a: Signal processing: project. Implement the contracts in README.md."""

def lowpass(x, fs, cutoff_hz=5.0, order=4):
    """Offline zero-phase Butterworth filtering; never a streaming operation."""
    raise NotImplementedError("Implement lowpass")

def window_features(x, window=100, step=50):
    """Extract complete half-open windows and population statistics."""
    raise NotImplementedError("Implement window_features")

