# Data-quality checks

Look for missing samples, rail saturation, offsets, drift, and timing gaps. Saturation means a signal reaches a measurement limit, so its true amplitude is unknown. Drift is a slow baseline change; without context, do not automatically call it motion.

```python
missing = ~np.isfinite(values)
rail = (values == 0) | (values == 4095)
gaps = np.flatnonzero(np.diff(t) > 1.5 * np.median(np.diff(t)))
```

Flag problems separately from cleaning. Keep the raw file unchanged and record assumptions. A missing row has no NaN to count, so timestamp checks complement value checks.

**Review:** plot raw counts against seconds, label units, and annotate rail and missing-value locations. Explain what a plot cannot establish about sensor placement.
