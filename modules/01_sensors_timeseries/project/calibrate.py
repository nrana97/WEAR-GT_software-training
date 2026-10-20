"""Level 1: Sensors and time series: project. Implement the contracts in README.md."""

def convert_counts(counts, vref=3.3, max_count=4095, zero_v=1.65, sensitivity_v_per_g=0.33):
    """Convert calibrated ADC counts to g, preserving NaNs."""
    raise NotImplementedError("Implement convert_counts")

def sampling_rate(t):
    """Estimate Hz from valid strictly increasing seconds."""
    raise NotImplementedError("Implement sampling_rate")

