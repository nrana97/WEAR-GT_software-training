# Lesson 3: Add events and quality context to session review

**Goal:** combine a readable recording plot with event markers and a quality summary that a non-programmer can interpret.

**Allow 45–60 minutes**, followed by a peer review of the saved output.

## Start from questions a reviewer asks

A reviewer may want to know when an activity started, whether a sensor disconnected, or why a model later produced a strange result. Showing only the waveform forces them to reconstruct context manually. Add event markers, missing-value counts, and clear channel identities.

A static PNG is a useful first deliverable because it opens without a Python environment. A future dashboard can add controls; the numerical and labeling rules should work before the interface grows.

## Keep event units explicit

The signal-processing module returns event sample indices. The visualization checkpoint expects event times in seconds. Convert deliberately:

```python
import numpy as np

fs = 100
peak_indices = np.array([25, 125, 225])
event_seconds = peak_indices / fs
print(event_seconds)  # [0.25, 1.25, 2.25]
```

For irregular timestamps, index into the actual timestamp array instead of dividing by an assumed rate. Do not plot sample index 125 at time 125 s when the event happened at 1.25 s.

Require a finite one-dimensional event list and keep events inside the displayed recording's coverage. An empty event list is valid: not every recording has annotations.

## Add markers on every panel

```python
import matplotlib.pyplot as plt

t = np.arange(300) / 100
x = np.sin(2 * np.pi * t)
fig, ax = plt.subplots(figsize=(10, 3))
ax.plot(t, x, label="signal")
for i, event in enumerate(event_seconds):
    ax.axvline(event, color="black", linestyle="--", alpha=.5,
               label="candidate event" if i == 0 else None)
ax.set(xlabel="Time (s)", ylabel="Amplitude (a.u.)")
ax.legend()
fig.tight_layout()
plt.show()
plt.close(fig)
```

Label the first marker so the legend explains all dashed lines without repeating the same entry. Use shape or line style as well as color; viewers should not need perfect color discrimination to understand the plot.

## Define quality flags precisely

For each channel, the checkpoint counts nonfinite observations and checks whether all finite observations have exactly the same value:

```python
values = np.array([2, np.nan, 2, np.inf, 2])
finite_values = values[np.isfinite(values)]
missing_samples = int((~np.isfinite(values)).sum())  # 2
constant = bool(len(finite_values) > 0 and
                np.all(finite_values == finite_values[0]))
print(constant)  # True
```

An all-missing channel has `constant=False` under this definition, because there is no valid value establishing a constant level. Report its missing count prominently so that False is not misread as “healthy variation.”

Exact equality detects perfectly flat finite values. A nearly flat channel needs a separate tolerance defined in physical units; do not quietly replace the checkpoint rule with a different statistic.

## Put context next to the trace

A panel title such as `acc_z: missing=20, constant=False` makes the summary available where the reviewer looks. A separate table can summarize a large recording, but it should not replace the time trace: the same missing count can mean scattered single samples or one continuous disconnect.

Avoid calling a constant channel “broken” in the title. Stillness, a stuck sensor, clipping, and an incorrect conversion are different possibilities. Use observation-based labels and discuss possible causes in the report.

## Review with another person

Ask someone to find one event, one gap, and the units without reading your code. If they cannot, revise the figure. Open the saved PNG at normal viewing size; notebook display can conceal cropped labels or tiny text.

## Try it

1. Create two channels: one with a missing block and one constant. Add three event times and save the review.
2. Add an all-missing channel. Confirm the summary says missing=N and constant=False.
3. Make the DataFrame index nonconsecutive. Confirm event times and quality counts still work.
4. Test an event outside recording coverage and explain why rejection is preferable to silently moving it.
5. Write a short caption describing what the figure establishes and what still requires hardware context.

**Ready for the checkpoint when:** every panel has units, events are in seconds, missing data remain visible, and your report distinguishes flags from diagnoses.

Continue: [Project](../project/README.md) · [Checkpoint](../checkpoint/README.md)
