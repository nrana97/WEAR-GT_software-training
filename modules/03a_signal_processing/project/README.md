# Project: Level 3a: Signal processing

Implement two functions on finite, nonempty 1-D arrays:

- `lowpass(x, fs, cutoff_hz=5.0, order=4)`: use a Butterworth low-pass in second-order sections and offline forward-backward filtering. Require finite positive fs, 0<cutoff<fs/2, positive integer order, and enough samples for SciPy's padding. Raise ValueError otherwise. Return an array of the same length.
- `window_features(x, window=100, step=50)`: require positive integer window and step. Include only complete windows. Return columns `start`, `stop`, `mean`, `std`, `rms` using half-open sample positions and population std. Return an empty table with those columns if x is shorter than window.

Filter sample.csv's finite `signal` column and compare raw/filtered plots. Do not filter the `raw` column with gaps without an explicit missing-data policy.


## Run and submit

```bash
python generate_data.py
python -m unittest -v test_task
# Equivalent, if pytest is installed:
pytest -v
```

Implement `process_signal.py`. Keep the public function signatures unchanged. Tests
use deterministic fixtures in addition to the generated CSV; do not hard-code
answers for the sample file. Add your own tests for one extra edge case.

Submit the implementation, tests, and a short `REPORT.md` explaining your
choices, one failure mode, and what would need to change for real recordings.
Do not commit generated recordings or personal data. Passing automated checks
is necessary; a reviewer must also inspect the report and plots where requested.
Reference implementation: `../../../reference_solutions/03a_signal_processing/process_signal.py`
(relative to this task folder).

## Worked usage

After implementing the starter, run `python run_example.py` for a runnable
demonstration using synthetic inputs. The example is a driver, not a solution.
