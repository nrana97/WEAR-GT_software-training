# Readable sensor plots

A review plot should answer: which channel, which units, which interval, and where are the problems? Use a shared time axis for related channels; avoid misleading independent autoscaling when comparing magnitudes. Preserve missing samples as visible breaks.

```python
fig, axes = plt.subplots(2, 1, sharex=True)
axes[0].plot(t, acceleration)
axes[0].set_ylabel("Acceleration (g)")
axes[1].set_xlabel("Time (s)")
fig.tight_layout()
```

Label calibrated units accurately. A rail flag in ADC counts must not be applied to a channel in g. Show events with vertical markers and explain their meaning in a legend.

**Try:** plot a trace with 20 missing samples; compare leaving NaNs with replacing them by zero.
