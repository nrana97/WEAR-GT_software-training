# Lesson 3: Validate with replay, fault injection, and evidence

**Goal:** create a reviewable simulation report that covers normal behavior, failures, timing limits, and remaining gaps.

**Allow 45–60 minutes** for reading and experiment design, then 60–90 minutes to run and document fault cases.

## Define the claim you are testing

“Works on my laptop” is too broad. A narrower claim is: “For the specified synthetic inputs and supplied timing values, this implementation rejects stale packets and latches a fault until reset.” That claim can be checked with a deterministic replay.

A simulation tests software behavior under its assumptions. It does not measure sensor accuracy, guarantee operating-system scheduling, or validate physical device safety. Keep the report's claims proportional to the evidence.

## Build a fault matrix before running experiments

Test one failure at a time so the cause is clear, then combine failures to verify priority.

| Case | Injection | Expected evidence |
|---|---|---|
| Normal | Finite bounded features and fresh time | `ok`, accepted timestamp updates |
| Missing/unusable input | Empty vector or NaN | `invalid_input`, zero simulated output |
| Stale/future time | Age beyond limit or negative age | `stale`, fault stored |
| Duplicate/out-of-order | Nonincreasing accepted time | `replayed` |
| Deadline | Supplied latency above limit | `deadline`, no predictor call |
| Model exception | Predictor raises | `model_error` |
| Invalid output | NaN, vector, or out-of-range scalar | `invalid_output` |
| Recovery attempt | Valid data after fault | `latched` until explicit reset |

Also test exact valid boundaries. A comparison using `<` instead of `<=` can reject a permitted boundary, while one reversed comparison can admit invalid data.

## Record enough detail to reproduce a result

A log row can contain sample time, evaluation time, input condition, latency, output, reason, and state before/after. Use synthetic identifiers and keep metadata describing configuration and code version.

```python
row = {
    "case": "stale",
    "sample_time_s": 0.0,
    "now_s": 0.2,
    "latency_s": .001,
    "max_age_s": .1,
    "expected_reason": "stale",
}
```

For deterministic replay, compute results from the same inputs on every run. For performance experiments, distinguish measured time from a simulated `latency_s` field; do not mix them in one chart without explicit labels.

## Summarize measured latency carefully

```python
import numpy as np

latencies_s = np.array([.001, .0012, .002, .015])
budget_s = .01
print(np.median(latencies_s))
print(latencies_s.max())
print(int((latencies_s > budget_s).sum()))  # 1 deadline miss
```

Report sample count, median, a high percentile when useful, observed maximum, and deadline-miss count. An observed maximum is not a mathematical worst-case bound. A tiny average can coexist with unacceptable rare delays. State what computation was timed and whether warm-up, load, and preprocessing were included.

## Review residual failure modes

Unit tests can verify rejection of known bad data. They cannot establish behavior when the process hangs, the clock domain is wrong, memory is exhausted, a queue loses packets silently, or a unit conversion changes unexpectedly. Document which failures are simulated, detected elsewhere, or still unaddressed.

For real hardware, the hardware and controls leads must define actual limits, physical safe states, independent supervision, emergency stops, and review procedures. The training code supplies none of that device-specific approval or integration. Keep it disconnected from actuators.

## Connect back to the earlier modules

A prediction depends on sensor calibration, timing continuity, documented session metadata, preprocessing, feature definitions, and an honest evaluation split. A correct deployment wrapper cannot rescue a model trained with leaked labels or sensor values in the wrong units.

Bring forward one artifact from each stage: quality audit, session metadata, filtered trace, review plot, and held-out model results. Identify where each stage's assumptions are checked and where they are only documented.

## Try it

1. Create the fault matrix above as a CSV or Markdown table with actual result, pass/fail, and one sentence of interpretation.
2. Verify both no-predictor-call behavior and the fault latch using explicit state inspection.
3. Repeat a replay twice and compare outputs. Explain which parts should be deterministic.
4. Measure the project wrapper separately and report deadline misses without describing a hard guarantee.
5. Write a final one-page handoff with implemented behavior, evidence, known limitations, and decisions requiring hardware/controls review.

**Completion criterion:** tests pass, the failure table matches the stated contract, and a reviewer can distinguish what was demonstrated from what remains unvalidated.

Continue: [Project](../project/README.md) · [Checkpoint](../checkpoint/README.md)
