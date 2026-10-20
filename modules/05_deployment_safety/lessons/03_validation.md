# Replay validation and team review

Replay known inputs and injected faults before touching hardware. Record feature time, receipt time, inference duration, output, and fault reason. Summarize worst observed latency as well as median; an observed maximum is not a hard real-time guarantee.

For a worn device, controller and hardware leads must define actual safe states, watchdogs, limits, emergency stops, and review procedures. Zero is a simulated placeholder here, not a universally safe command. Do not connect this training code to a device.

**Deliverable:** a fault-injection table with stale, replayed, missing, nonfinite, out-of-range, slow, and exception-producing cases. Explain residual risks including process failure, clock mismatch, and a predictor that never returns.
