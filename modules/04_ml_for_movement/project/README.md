# Project: Level 4: ML for movement

Implement `train_evaluate(df, feature_columns, test_subjects)`.

Input columns include `subject_id`, binary integer `label` (0/1), and explicit numeric feature columns. Require nonempty unique features excluding subject_id and label, finite feature values, nonmissing subject IDs, known nonempty test_subjects, nonempty training data, and both classes in training. Reject invalid input with ValueError. Never use subject_id as a feature.

Fit StandardScaler + LogisticRegression(max_iter=1000, random_state=0) on training subjects only. Return dict with `model`, `accuracy`, `balanced_accuracy`, `baseline_accuracy` (training-majority class, ties choose 0), `confusion_matrix` (2x2 with labels [0,1]), `train_subjects`, `test_subjects`. Subject lists must be sorted. Baseline is evaluated on the same test rows. Leave inputs unchanged.

The generator here creates `features.csv`. Use subjects S04 and S05 as a demonstration holdout. Include a report comparing model and baseline and explaining leakage risks.


## Run and submit

```bash
python generate_data.py
python -m unittest -v test_task
# Equivalent, if pytest is installed:
pytest -v
```

Implement `train_model.py`. Keep the public function signatures unchanged. Tests
use deterministic fixtures in addition to the generated CSV; do not hard-code
answers for the sample file. Add your own tests for one extra edge case.

Submit the implementation, tests, and a short `REPORT.md` explaining your
choices, one failure mode, and what would need to change for real recordings.
Do not commit generated recordings or personal data. Passing automated checks
is necessary; a reviewer must also inspect the report and plots where requested.
Reference implementation: `../../../reference_solutions/04_ml_for_movement/train_model.py`
(relative to this task folder).

## Worked usage

After implementing the starter, run `python run_example.py` for a runnable
demonstration using synthetic inputs. The example is a driver, not a solution.
