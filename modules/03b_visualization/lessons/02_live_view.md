# Lesson 2: Replay a session and design a bounded live view

**Goal:** implement a time-window view of recorded data and explain what additional work a genuinely live view needs.

**Allow 45–60 minutes**, plus a small replay experiment. The exercise uses recorded CSV-style data; it does not establish live acquisition performance.

## A replay is a useful first step

A replay reveals progressively more of an already recorded session. It is deterministic, easy to pause, and does not depend on hardware. A live monitor must handle new samples, delays, disconnects, and overload while acquisition continues.

For training we use Matplotlib to avoid committing the team to a dashboard framework prematurely. An interactive GUI or web application can be added after the underlying time selection and quality summaries are correct.

## Select a time interval, not a guessed sample count

Suppose the visible interval is the last two seconds ending at a chosen replay time:

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({
    "timestamp_s": np.arange(501) / 100,
    "signal": np.sin(2 * np.pi * np.arange(501) / 100),
})
end_s = 3.0
width_s = 2.0
mask = df.timestamp_s.between(end_s - width_s, end_s)
view = df.loc[mask].copy()
print(view.timestamp_s.min(), view.timestamp_s.max())  # 1.0, 3.0
```

The inclusive interval includes both endpoints. With exact timestamps in this example, that means 201 samples, not 200. If the recording has gaps, the number of rows changes even though the visible time interval is identical.

Require finite `end_s` and positive finite `width_s`. A cutoff before or after the recording can legitimately produce an empty or partially filled view. Return a copy so changing display data cannot alter the original recording.

## Advance the cutoff

```python
for end_s in [1.0, 2.5, 4.0]:
    view = df.loc[df.timestamp_s.between(end_s - 2, end_s)].copy()
    print(end_s, len(view))
```

Start with printing and saved snapshots before adding animation. It is easier to diagnose time selection without event-loop complications. Later, update an existing line with `line.set_data(t, x)` and redraw rather than creating new figures repeatedly.

## Acquisition rate and display rate differ

A sensor can acquire at 100 Hz while the display refreshes at 10 Hz. Each refresh can include all samples received since the last one. Drawing every sample as a separate GUI update can waste work and block acquisition.

A real monitor should separate the collector from the plot consumer. The consumer gets a snapshot of a bounded buffer rather than taking ownership of the collection loop. Measure rendering cost, queue depth, and dropped messages under representative load.

## Bound memory as well as visible time

A slice of a growing DataFrame limits visible duration but does not limit the original DataFrame's memory. A real rolling monitor needs bounded storage:

```python
from collections import deque

recent = deque(maxlen=200)
for i in range(300):
    recent.append((i / 100, float(i)))
print(len(recent))  # 200
```

This count-bounded example stores about two seconds at 100 Hz. Its exact elapsed coverage depends on timing and endpoints. With irregular rates, evict by timestamp or size the buffer with margin. Long-term logging should be a separate task so display eviction does not delete the only copy.

## Show freshness and connection state

A frozen line can look like a stationary person. Display last-sample age and whether acquisition is active. If data stop, keep the distinction between “the signal stayed flat” and “no new signal arrived.” Use a common clock domain before calculating age.

Avoid deriving a device safety decision from a visualization refresh. A display can lag or freeze; it is not a watchdog or emergency stop.

## Try it

1. Save three snapshots at different cutoffs using the same two-second width.
2. Delete half a second of samples and compare row counts in affected versus unaffected windows.
3. Modify a selected view and confirm the original DataFrame remains unchanged.
4. Estimate memory for a ring buffer with 1000 samples and eight float64 sensor channels, then account for timestamp and container overhead separately.
5. Design a display status line containing latest time, sample age, missing-value count, and connection state. Explain how each field would be updated.

Next: [Session review and quality summaries](03_review.md)
