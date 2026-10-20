# Checkpoint: Level 3a: Signal processing

Implement `cycle_features(x, fs, min_interval_s=0.5, prominence=0.5)` using scipy.signal.find_peaks. Input is finite nonempty 1-D signal, positive finite fs and min_interval_s, nonnegative finite prominence. Minimum distance is ceil(fs*min_interval_s). Return `(events, table)` where events is the integer peak-index array and table has `start`, `stop`, `duration_s`, `mean`, `rms`, `peak_to_peak` for each consecutive event pair. Segments are `[start,stop)`. Return an empty table with the same schema for fewer than two events. Reject invalid input with ValueError.

Use sample.csv's `signal`, report event count and cycle durations, and overlay detections on the trace. Discuss why peaks are not guaranteed to be heel strikes. This checkpoint consumes a cleaned trace; it does not require copying the project filter.


## Run and submit

```bash
python generate_data.py
python -m unittest -v test_task
# Equivalent, if pytest is installed:
pytest -v
```

Implement `cycles.py`. Keep the public function signatures unchanged. Tests
use deterministic fixtures in addition to the generated CSV; do not hard-code
answers for the sample file. Add your own tests for one extra edge case.

Submit the implementation, tests, and a short `REPORT.md` explaining your
choices, one failure mode, and what would need to change for real recordings.
Do not commit generated recordings or personal data. Passing automated checks
is necessary; a reviewer must also inspect the report and plots where requested.
Reference implementation: `../../../reference_solutions/03a_signal_processing/cycles.py`
(relative to this task folder).
