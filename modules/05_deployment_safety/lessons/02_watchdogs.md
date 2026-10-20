# Lesson 2: Freshness checks and a latched fault state

**Goal:** trace a simulated state machine that rejects stale, replayed, invalid, and late inputs and requires explicit reset after a fault.

**Allow 60–75 minutes**, including a hand-traced fault sequence. The output zero and numerical limits are training placeholders, not device safety specifications.

## A valid number can still be unusable

A feature vector can be finite and in range but describe old data. A model output can be numerically valid but arrive too late. Safety-related monitoring needs timing and state, not only arithmetic checks.

For the checkpoint, `sample_time_s` and `now_s` are in the same clock domain:

```python
sample_time_s = 1.00
now_s = 1.06
age_s = now_s - sample_time_s
print(age_s)  # approximately .06 s
```

Reject future samples, nonfinite times, and age greater than the allowed maximum. Clock offset must be handled before this comparison; otherwise correct data can appear stale or future-dated.

## Freshness and replay protection differ

A recent packet can still be a duplicate or an older packet arriving out of order. Track the last accepted sample time. The checkpoint requires strictly increasing sample times: a new time less than or equal to the previous accepted one faults as `replayed`.

```python
last_sample_s = 1.00
candidate_s = 1.00
print(candidate_s <= last_sample_s)  # True: duplicated timestamp
```

A real protocol may require sequence numbers and counter-wrap handling. The timestamp rule here is a simplified teaching contract.

## What a fault latch does

A latched fault persists. Later valid data do not automatically resume the simulated output. State stores `fault` and `last_sample_s`:

```python
state = {"fault": None, "last_sample_s": None}
# Successful observation:
state["last_sample_s"] = 0.0
# A later stale observation:
state["fault"] = "stale"
# Later calls return reason='latched' until reset.
```

This prevents a brief recovery from hiding an unresolved problem. Reset clears both fields in the exercise. In a real system, who may reset, which checks must pass, and whether motion may resume are separate engineering decisions.

## Check order is part of the interface

The checkpoint defines this order:

1. Validate positive finite configuration limits.
2. Return `latched` if a fault already exists.
3. Check sample freshness and clock validity.
4. Reject replayed/nonincreasing sample time.
5. Validate feature shape, finiteness, and magnitude limit.
6. Check supplied simulated latency.
7. Call the predictor and handle exceptions.
8. Validate scalar output and range.
9. On success, update the last accepted sample time.

If an input is both stale and out of range, the reported new fault is `stale`. Consistent priority makes tests and logs interpretable. On a fault, leave `last_sample_s` unchanged because the observation was not accepted.

## Injected latency is not measured latency

The checkpoint takes `latency_s` as an input so you can test state transitions deterministically. If that value exceeds the budget, the predictor must not be called. This is a simulator, unlike the project wrapper that measures a returned call.

Neither design can establish real-time hardware safety. A stalled Python process cannot supervise itself, and a physical device may need independent watchdogs, an emergency stop, and a safe state designed for its mechanics.

## Trace before coding

| Call | Input situation | Expected result |
|---|---|---|
| 1 | Fresh valid sample | `ok`, accept time |
| 2 | Same timestamp again | `replayed`, latch fault |
| 3 | Fresh valid sample | `latched`, no automatic recovery |
| Reset | Explicit reset call | Clear history and fault |
| 4 | Fresh valid sample | `ok` again |

Use a spy predictor that appends to a list to prove it is not called for pre-inference rejection cases. Checking the returned reason alone would miss an unnecessary or dangerous call.

## Try it

1. Trace the table with exact sample times and write state after each step.
2. Test age and latency exactly at the allowed boundary, then just above it. The checkpoint allows equality.
3. Inject NaN features, out-of-range features, a future time, and a negative latency independently.
4. Confirm a rejected packet does not update the accepted timestamp.
5. Explain why zero simulated output may not be physically safe for an exoskeleton or prosthesis, without proposing an unreviewed hardware solution.

Next: [Replay validation and team review](03_validation.md)
