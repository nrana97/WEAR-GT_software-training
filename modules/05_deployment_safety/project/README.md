# Project: Level 5: Deployment and safety

Implement `infer(predict, features, budget_s=0.01, clock=None)`.

Features must convert to a nonempty finite 1-D float array. budget_s is positive finite; invalid budget raises ValueError. Default clock is time.perf_counter; an injected clock returns seconds. Measure elapsed around predict(features). Return a dict with `output`, `latency_s`, `reason`. Valid scalar output is finite and inside [-1,1], and elapsed must be finite, >=0 and <=budget_s. On success reason='ok'. On invalid features use output=0.0, latency_s=0.0, reason='invalid_input'; on predictor exception reason='model_error'; on invalid/non-scalar result reason='invalid_output'; on late/invalid elapsed reason='deadline'. Every failure output is 0.0. For predictor exceptions still measure elapsed. Deadline takes priority over result validation for a returned result.

This is a synchronous simulation; it detects lateness only after the predictor returns. Explain why it cannot enforce a deadline on a hung process.


## Run and submit

```bash
python generate_data.py
python -m unittest -v test_task
# Equivalent, if pytest is installed:
pytest -v
```

Implement `inference.py`. Keep the public function signatures unchanged. Tests
use deterministic fixtures in addition to the generated CSV; do not hard-code
answers for the sample file. Add your own tests for one extra edge case.

Submit the implementation, tests, and a short `REPORT.md` explaining your
choices, one failure mode, and what would need to change for real recordings.
Do not commit generated recordings or personal data. Passing automated checks
is necessary; a reviewer must also inspect the report and plots where requested.
Reference implementation: `../../../reference_solutions/05_deployment_safety/inference.py`
(relative to this task folder).

## Worked usage

After implementing the starter, run `python run_example.py` for a runnable
demonstration using synthetic inputs. The example is a driver, not a solution.
