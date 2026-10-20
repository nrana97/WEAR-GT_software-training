# Checkpoint: Level 1: Sensors and time series

Audit the unmodified recording; do not silently repair it.

`audit(df, max_count=4095)` accepts columns `timestamp_s` and `raw`. Return a dict with `sample_rate_hz`, `missing_values`, `saturated_samples`, and `gap_after_indices` (zero-based positional indices before gaps). Missing includes NaN and infinity in raw. Saturated means finite raw <=0 or >=max_count. Gap means interval >1.5 times median interval. Reject invalid/nonincreasing times, fewer than two rows, and nonpositive/nonfinite max_count. Do not mutate the input.

Produce a labeled plot and discuss saturation, missing values, and timing gaps. State why this audit cannot diagnose every sensor failure.


## Run and submit

```bash
python generate_data.py
python -m unittest -v test_task
# Equivalent, if pytest is installed:
pytest -v
```

Implement `audit.py`. Keep the public function signatures unchanged. Tests
use deterministic fixtures in addition to the generated CSV; do not hard-code
answers for the sample file. Add your own tests for one extra edge case.

Submit the implementation, tests, and a short `REPORT.md` explaining your
choices, one failure mode, and what would need to change for real recordings.
Do not commit generated recordings or personal data. Passing automated checks
is necessary; a reviewer must also inspect the report and plots where requested.
Reference implementation: `../../../reference_solutions/01_sensors_timeseries/audit.py`
(relative to this task folder).
