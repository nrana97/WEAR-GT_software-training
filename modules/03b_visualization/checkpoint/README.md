# Checkpoint: Level 3b: Visualization and dashboards

Implement `review(df, units, events, out_path)` returning `(fig, axes, quality)`.

Use the same plot structure as the project. Events is a finite 1-D list/array of **seconds**, each inside the recording range. Overlay a dashed vertical line for every event on every panel; label at least one event marker in a legend per panel. `quality` is a dict per channel containing `missing_samples` (NaN or infinity) and `constant` (True if at least one finite value and all finite values equal; False if none). Show quality counts in each panel title. Reject invalid times, missing units, no sensor channels, invalid events with ValueError. Save a PNG after adding markers. Do not mutate df.

Also implement `visible_window(df, end_s, width_s=2.0)` returning a copy of rows in the inclusive interval [end_s-width_s,end_s]. Require finite end_s and positive finite width_s. This supports bounded-time replay; actual acquisition buffering is out of scope.

Submit one figure with gaps/events and demonstrate at least three replay cutoffs in your report. Explain what a constant channel can and cannot establish.


## Run and submit

```bash
python generate_data.py
python -m unittest -v test_task
# Equivalent, if pytest is installed:
pytest -v
```

Implement `dashboard.py`. Keep the public function signatures unchanged. Tests
use deterministic fixtures in addition to the generated CSV; do not hard-code
answers for the sample file. Add your own tests for one extra edge case.

Submit the implementation, tests, and a short `REPORT.md` explaining your
choices, one failure mode, and what would need to change for real recordings.
Do not commit generated recordings or personal data. Passing automated checks
is necessary; a reviewer must also inspect the report and plots where requested.
Reference implementation: `../../../reference_solutions/03b_visualization/dashboard.py`
(relative to this task folder).
