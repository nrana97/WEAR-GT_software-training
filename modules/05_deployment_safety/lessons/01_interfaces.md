# Lesson 1: Inference interfaces, latency, and failure results

**Goal:** wrap a predictor in an explicit input/output contract, measure elapsed inference time, and report unusable outputs consistently.

**Allow 45–60 minutes.** Everything here is a synchronous software simulation; no device communication or actuation is implemented.

## Prediction is one stage of a larger system

A classifier can predict a class from a feature vector. A controller decides how a physical system should behave. Those are different interfaces. A class label of 1 is not permission to produce a torque of 1 N·m.

The teaching wrapper accepts a predictor that returns a single normalized scalar in [-1,1]. This scalar is a simulated result only. Real units, controller logic, authority limits, and physical safe states require hardware/controls design outside the exercise.

Define what the caller can depend on: input shape, finite values, output range, deadline, and failure reasons. A consistent result dictionary lets the caller distinguish a valid zero from a failure that returns zero.

## Validate features before calling the model

```python
import numpy as np

features = np.asarray([.2, .8], dtype=float)
valid = features.ndim == 1 and len(features) > 0 and np.isfinite(features).all()
print(valid)  # True
```

A two-dimensional array, empty input, NaN, or infinity violates this task's contract. A numeric conversion can also fail for strings. Do not call a predictor on invalid input and hope its output will be sensible.

Real inference also needs a fixed feature count, order, units, window definition, and preprocessing version. The project validates a generic vector; document those extra requirements rather than pretending shape alone is enough.

## Measure elapsed time with a monotonic clock

```python
from time import perf_counter

start = perf_counter()
output = float(np.tanh(features.mean()))
elapsed_s = perf_counter() - start
print(output, elapsed_s)
```

`perf_counter` is suitable for elapsed measurements. Wall time can change due to clock adjustments. The project measures the predictor call; acquisition, window construction, filtering, queueing, and transport add further delay in a complete pipeline.

At 100 Hz, a sample interval is 10 ms, but that does not automatically make 10 ms the correct end-to-end decision budget. A 1-second feature window can dominate response time even when model inference takes microseconds.

## Make failures distinguishable

The project returns `output`, `latency_s`, and `reason`:

| Reason | Meaning |
|---|---|
| `ok` | Returned scalar passed validity and timing checks |
| `invalid_input` | Features could not be used |
| `model_error` | Predictor raised an exception |
| `invalid_output` | Returned value was nonfinite, nonscalar, or outside bounds |
| `deadline` | Returned result missed the deadline or elapsed time was invalid |

Every failure returns simulated output 0.0. That value is a placeholder chosen for testing; it is not a universal physical safe command. The reason field carries the distinction.

A list containing one value is not a scalar under this contract. Be explicit about `np.asarray(result).ndim == 0`; permissive conversion can accidentally accept a shape your downstream interface does not support.

## Test timing without relying on machine load

Inject a clock so tests can create exact timing scenarios:

```python
times = iter([10.0, 10.02])
fake_clock = lambda: next(times)
start = fake_clock()
# A simulated predictor call happens here.
elapsed = fake_clock() - start
print(elapsed > .01)  # True: late for a 10 ms budget
```

This verifies decision logic, not actual runtime. Real performance measurements need repeated runs under representative load and a declared boundary around what is being timed.

## A synchronous timeout cannot stop a hung call

Checking the clock after a function returns detects late results. It cannot interrupt a predictor that never returns. An independent process, watchdog, or lower-level real-time mechanism is needed for stronger supervision. Do not use this wrapper as a hardware safety mechanism.

## Try it

1. Write toy predictors returning a valid scalar, NaN, a list, and an out-of-range value. Predict the reason for each before running it.
2. Create a predictor that raises an exception. Confirm the caller receives a failure result rather than a valid-looking prediction.
3. Use fake clocks for a fast and a late result. Explain what the test proves.
4. Draw up an end-to-end latency budget including a feature window, preprocessing, model, and transport.
5. Write the extra inference schema needed to reuse your Level 4 model without changing feature order or scaling.

Next: [Freshness, watchdogs, and fault latching](02_watchdogs.md)
