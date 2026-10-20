# Project: Level 2: Data collection and logging

Implement `write_session(df, metadata, directory)`.

Require `timestamp_s` and at least one sensor column, at least two rows, finite strictly increasing timestamps, and numeric sensor columns (NaNs allowed). Required metadata keys: `session_id`, `subject_id`, `task`, `sensor_placement`, `firmware_version`; each is a nonempty string. Validate JSON serialization before creating files. Raise `ValueError` on invalid input and `FileExistsError` if directory exists. Write `samples.csv` without an index and `metadata.json`; return the directory as a `Path`. Leave no partial directory after a write failure.

Use sample.csv as a replay input; this project does not open serial hardware. In your report outline a bounded queue, a dropped-packet counter, and how you would test sustained acquisition.


## Run and submit

```bash
python generate_data.py
python -m unittest -v test_task
# Equivalent, if pytest is installed:
pytest -v
```

Implement `session_logger.py`. Keep the public function signatures unchanged. Tests
use deterministic fixtures in addition to the generated CSV; do not hard-code
answers for the sample file. Add your own tests for one extra edge case.

Submit the implementation, tests, and a short `REPORT.md` explaining your
choices, one failure mode, and what would need to change for real recordings.
Do not commit generated recordings or personal data. Passing automated checks
is necessary; a reviewer must also inspect the report and plots where requested.
Reference implementation: `../../../reference_solutions/02_data_collection_logging/session_logger.py`
(relative to this task folder).

## Worked usage

After implementing the starter, run `python run_example.py` for a runnable
demonstration using synthetic inputs. The example is a driver, not a solution.
