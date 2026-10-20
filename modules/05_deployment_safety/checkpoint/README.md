# Checkpoint: Level 5: Deployment and safety

Implement standalone `reset(state)` and `step(state, predict, features, sample_time_s, now_s, latency_s, max_age_s=0.1, budget_s=0.01, input_limit=10.0)`.

State is a dict with `fault` (None or reason string) and `last_sample_s` (None or float). `reset` mutates state to these two keys set to None. `step` returns `{'output': float, 'reason': str}` and updates state. This uses a **supplied simulated latency**, not measured runtime.

Check in this order: (1) validate positive finite configuration or raise ValueError; (2) existing fault returns zero with reason 'latched'; (3) invalid/nonfinite sample/now time, future time, or age>max_age_s faults as 'stale'; (4) sample_time <= last_sample faults as 'replayed'; (5) invalid/empty/nonfinite/non-1D features or absolute values >input_limit faults as 'invalid_input'; (6) nonfinite/negative latency or latency>budget faults as 'deadline' without calling predict; (7) predictor exception faults as 'model_error'; (8) non-scalar/nonfinite output or outside [-1,1] faults as 'invalid_output'. Otherwise update last_sample_s and return prediction with reason 'ok'. On each new fault set state['fault'] and return output=0.0, keeping last_sample_s unchanged. Boundaries are inclusive (age==max_age and latency==budget allowed).

Show reset behavior and each fault in REPORT.md. Explicitly state that safe output and limits are placeholders needing hardware/controls review, and that this simulator must not actuate a device.


## Run and submit

```bash
python generate_data.py
python -m unittest -v test_task
# Equivalent, if pytest is installed:
pytest -v
```

Implement `safety_loop.py`. Keep the public function signatures unchanged. Tests
use deterministic fixtures in addition to the generated CSV; do not hard-code
answers for the sample file. Add your own tests for one extra edge case.

Submit the implementation, tests, and a short `REPORT.md` explaining your
choices, one failure mode, and what would need to change for real recordings.
Do not commit generated recordings or personal data. Passing automated checks
is necessary; a reviewer must also inspect the report and plots where requested.
Reference implementation: `../../../reference_solutions/05_deployment_safety/safety_loop.py`
(relative to this task folder).
