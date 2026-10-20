# Checkpoint: Level 4: ML for movement

Implement `evaluate_subjects(df, feature_columns)` for leave-one-subject-out evaluation. Use the same feature/label validation and pipeline as the project, fit a fresh model/scaler in each fold, and require >=3 subjects with both classes in every training fold.

Return dict: `folds` is a DataFrame with sorted `subject_id`, `n_test`, `accuracy`, `baseline_accuracy`; `mean_accuracy` is the unweighted mean of fold accuracies; `std_accuracy` is their sample standard deviation (ddof=1). Do not report std as a confidence interval. No held-out row may participate in fitting its fold. ValueError for invalid data.

Report per-subject and mean results, baseline comparisons, and at least two reasons these synthetic results do not imply real-device performance. You may reuse your project logic by copying it into this standalone file, but do not import across task folders.


## Run and submit

```bash
python generate_data.py
python -m unittest -v test_task
# Equivalent, if pytest is installed:
pytest -v
```

Implement `group_evaluation.py`. Keep the public function signatures unchanged. Tests
use deterministic fixtures in addition to the generated CSV; do not hard-code
answers for the sample file. Add your own tests for one extra edge case.

Submit the implementation, tests, and a short `REPORT.md` explaining your
choices, one failure mode, and what would need to change for real recordings.
Do not commit generated recordings or personal data. Passing automated checks
is necessary; a reviewer must also inspect the report and plots where requested.
Reference implementation: `../../../reference_solutions/04_ml_for_movement/group_evaluation.py`
(relative to this task folder).
