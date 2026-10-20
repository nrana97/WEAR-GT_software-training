# Lesson 1: Streaming data, clocks, and packet loss

**Goal:** distinguish measurement time from arrival time and design a collection path whose failures can be measured.

**Allow 45–60 minutes** for the examples and a small simulated collector. No hardware is required.

## A stream is more than an array

A recording in a CSV is already complete. A stream arrives incrementally, and the next observation may be delayed, malformed, duplicated, or absent. Acquisition code needs to preserve enough information to diagnose those cases later.

A useful packet might contain:

```python
packet = {
    "sensor_id": "imu_01",
    "sequence": 103,
    "device_time_s": 1.03,
    "arrival_time_s": 8.417,
    "value": 2052,
}
```

The sequence number tracks device order, device time describes when the sensor says the observation happened, and arrival time describes when the host received it. They answer different questions. A larger arrival time does not mean the movement happened later by that amount.

## Clock domains need an explicit relationship

Two devices can sample the same motion with clocks that start at different times. In this exercise, device B is 0.2 s ahead of reference A:

```python
import numpy as np

a_time = np.arange(5) / 50
b_time = np.arange(5) / 50 + .2
b_in_a_time = b_time + (-.2)
print(np.allclose(a_time, b_in_a_time))  # True
```

The sign matters: the contract adds `offset_b_s`. A B timestamp of 0.2 maps to A time zero by adding −0.2. Document what clock the output uses.

Real clocks may also drift. A relation such as `reference = scale * device + offset` includes rate mismatch. A constant-offset exercise does not solve drift. Synchronization needs a shared trigger, known protocol, or other justified reference; matching two noisy peaks visually is not a reliable clock calibration.

## Arrival jitter is not necessarily sampling jitter

A USB device might sample at exactly 100 Hz but deliver packets in groups. Host arrival intervals could look irregular even when device timestamps are regular.

```python
device_time = np.arange(6) / 100
arrival_time = np.array([.10, .10, .10, .13, .13, .16])
print(np.diff(device_time))   # regular 0.01 s
print(np.diff(arrival_time))  # includes zero and longer intervals
```

If you assign arrival time as measurement time, the apparent sample rate changes with buffering. Save both where available. Within a running process, use a monotonic clock for elapsed time rather than a wall clock that may be adjusted.

## Sequence numbers reveal losses

```python
sequence = np.array([100, 101, 102, 105, 106])
jumps = np.diff(sequence)
missing_packets = np.maximum(jumps - 1, 0).sum()
print(missing_packets)  # 2
```

This assumes no wraparound or reset. In real protocols, handle counter width, resets, duplicates, and reordered packets explicitly. A gap is evidence about continuity, not proof that the operating system caused the loss.

## Separate collection from expensive work

Drawing a plot or fitting a model inside the acquisition loop can block the reader. A common design has a fast reader, a bounded queue, and a separate writer/consumer. A bounded queue prevents unlimited memory growth, but it needs a declared overload policy.

```python
from queue import Queue, Full

pending = Queue(maxsize=3)
dropped = 0
for number in range(5):
    try:
        pending.put_nowait({"sequence": number})
    except Full:
        dropped += 1
print(pending.qsize(), dropped)  # 3 queued, 2 rejected
```

This miniature example has no consumer, so overload is guaranteed. A real system must choose whether to block, drop oldest/newest, or stop acquisition, then record what happened. Never claim “no sample loss” merely because the program did not crash.

## Try it

1. Add simulated network delay to a regular device timeline. Plot device intervals and arrival intervals separately.
2. Insert a duplicate sequence number and a counter reset. Explain why the simple missing-packet formula is insufficient.
3. Modify the queue example to consume one item every second iteration. Log every rejected sequence number.
4. Sketch a reader/queue/writer design. Identify which component owns timestamps and which counts losses.
5. Write three requirements for a sustained acquisition test: include duration, sample rate, and observable loss/queue metrics.

**Check yourself:** a constant offset changes timestamp origins, not the interval between samples. A bounded queue prevents unbounded memory use; it does not guarantee complete data.

Next: [Session files and metadata](02_sessions.md)
