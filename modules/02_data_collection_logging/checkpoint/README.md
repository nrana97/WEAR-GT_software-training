# Checkpoint: Level 2: Data collection and logging

Implement `align(a, b, grid, offset_b_s=0.0, max_gap_s=0.1)`.

Each stream has `timestamp_s` and `value`. Correct B time by **adding** offset_b_s. Return a DataFrame with `timestamp_s`, `a`, `b` on exactly the supplied grid. Require finite strictly increasing stream times and grid (>=2 observations per stream, >=1 grid point), finite offset, and positive finite max_gap_s. Values may be NaN/inf and must produce missing output when used as interpolation endpoints. No extrapolation. Preserve exact finite observations even next to long gaps. Fill interior values linearly only across gaps <=max_gap_s with finite endpoints. Use a 1e-12 absolute tolerance to identify exact times. Do not mutate inputs.

Demonstrate two rates, a clock offset, and a long dropout. Explain why offset correction alone cannot handle drifting clocks.


## Run and submit

```bash
python generate_data.py
python -m unittest -v test_task
# Equivalent, if pytest is installed:
pytest -v
```

Implement `align_streams.py`. Keep the public function signatures unchanged. Tests
use deterministic fixtures in addition to the generated CSV; do not hard-code
answers for the sample file. Add your own tests for one extra edge case.

Submit the implementation, tests, and a short `REPORT.md` explaining your
choices, one failure mode, and what would need to change for real recordings.
Do not commit generated recordings or personal data. Passing automated checks
is necessary; a reviewer must also inspect the report and plots where requested.
Reference implementation: `../../../reference_solutions/02_data_collection_logging/align_streams.py`
(relative to this task folder).
