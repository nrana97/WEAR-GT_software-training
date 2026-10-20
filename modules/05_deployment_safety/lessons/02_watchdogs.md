# Freshness, bounds, and fault latching

Check sample age before inference. A stale or future timestamp indicates invalid timing. Require monotonic sample timestamps to reject replayed packets. Enforce input and output bounds and a latency deadline. Faults should return a simulated safe output with a reason.

The checkpoint latches a fault: later valid data cannot resume operation until an explicit reset. This is a teaching state machine, not a complete device safety design. Software timeouts cannot interrupt a permanently hung predictor in the same thread; a real system needs independent watchdogs and an engineered safe state.

**Trace:** valid packet → stale packet → valid packet → reset → valid packet. Predict every output and reason before running tests.
