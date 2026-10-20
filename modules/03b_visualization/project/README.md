# Project: Level 3b: Visualization and dashboards

Implement `plot_session(df, units, out_path)` using Matplotlib. Require finite strictly increasing `timestamp_s` (>=2 rows), >=1 numeric sensor channel, and a nonempty unit string per sensor. Sensor values may contain NaN/inf; display both as missing. Save one panel per sensor with shared time axis, y-label `channel (unit)`, x-label `Time (s)` on the bottom panel, and a title. Return `(fig, axes)` with axes a 1-D NumPy array even for one channel. Do not mutate df. The caller closes the figure.

Use sample.csv to create your review figure. Manually inspect saved output; automatic checks cannot judge readability.


## Run and submit

```bash
python generate_data.py
python -m unittest -v test_task
# Equivalent, if pytest is installed:
pytest -v
```

Implement `review_plot.py`. Keep the public function signatures unchanged. Tests
use deterministic fixtures in addition to the generated CSV; do not hard-code
answers for the sample file. Add your own tests for one extra edge case.

Submit the implementation, tests, and a short `REPORT.md` explaining your
choices, one failure mode, and what would need to change for real recordings.
Do not commit generated recordings or personal data. Passing automated checks
is necessary; a reviewer must also inspect the report and plots where requested.
Reference implementation: `../../../reference_solutions/03b_visualization/review_plot.py`
(relative to this task folder).

## Worked usage

After implementing the starter, run `python run_example.py` for a runnable
demonstration using synthetic inputs. The example is a driver, not a solution.
