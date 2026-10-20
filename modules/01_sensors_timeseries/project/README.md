# Project: Level 1: Sensors and time series

Convert a teaching accelerometer recording and summarize its timing.

- `convert_counts(counts, vref=3.3, max_count=4095, zero_v=1.65, sensitivity_v_per_g=0.33)` returns a float NumPy array in g using the lesson equation. Preserve NaNs; reject infinities, finite counts outside [0,max_count], or nonpositive/nonfinite scale parameters with `ValueError`.
- `sampling_rate(t)` returns inverse median interval. Require a 1-D finite array of at least two strictly increasing times; otherwise raise `ValueError`.

Load `sample.csv`, convert `raw`, and save a labeled plot in your own driver script. Explain why NaNs are not zeros.


## Run and submit

```bash
python generate_data.py
python -m unittest -v test_task
# Equivalent, if pytest is installed:
pytest -v
```

Implement `calibrate.py`. Keep the public function signatures unchanged. Tests
use deterministic fixtures in addition to the generated CSV; do not hard-code
answers for the sample file. Add your own tests for one extra edge case.

Submit the implementation, tests, and a short `REPORT.md` explaining your
choices, one failure mode, and what would need to change for real recordings.
Do not commit generated recordings or personal data. Passing automated checks
is necessary; a reviewer must also inspect the report and plots where requested.
Reference implementation: `../../../reference_solutions/01_sensors_timeseries/calibrate.py`
(relative to this task folder).

## Worked usage

After implementing the starter, run `python run_example.py` for a runnable
demonstration using synthetic inputs. The example is a driver, not a solution.
