# Streams and clock domains

A sensor timestamp and a host arrival time describe different events. USB buffering can delay arrivals even when device sampling is regular. Save device time, arrival time, sequence numbers, units, and sensor identity when the real protocol supplies them.

For these exercises the stream is a DataFrame with `timestamp_s` and `value`. A constant offset correction maps device B into reference A time:

```python
reference_time = device_time + offset_s
```

This does not correct clock drift. Estimate offsets using a shared trigger or a validated synchronization protocol; do not infer synchronization just because two motions look similar.

**Try:** simulate timestamps `np.arange(10)/50 + .2`. What offset maps them to a recording starting at zero?
