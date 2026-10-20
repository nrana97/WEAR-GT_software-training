# Lesson 2: Split by subject and fit preprocessing on training data

**Goal:** build a reproducible training/test split that measures performance on held-out subjects and prevents preprocessing leakage.

**Allow 60–75 minutes** for a split experiment and pipeline walkthrough.

## Decide what generalization means

Randomly splitting windows can put observations from the same person and session in both sets. Neighboring or overlapping windows can share raw samples. A model may then exploit subject-specific patterns that will not transfer to a new person.

If the question is performance on unseen subjects, every window from a subject must stay together. A different question—future sessions from already known subjects—needs a different split design. State the question before choosing a convenient splitter.

## Make the split visible

From the project directory, generate the fixture and choose a holdout:

```python
from generate_data import generate

df = generate()
feature_columns = ["rms", "gyro_std"]
test_subjects = {"S04", "S05"}
mask = df.subject_id.isin(test_subjects)
train = df.loc[~mask].copy()
test = df.loc[mask].copy()

assert set(train.subject_id).isdisjoint(set(test.subject_id))
print(len(train), len(test))  # 320 training, 160 test windows
```

Reject empty or unknown holdout IDs. A typo that silently yields an empty test set should be an error, not a mysterious metric. Also verify that training has both classes; binary logistic regression cannot learn from one class alone.

## Scaling learns parameters

Standardization commonly subtracts a training mean and divides by a training standard deviation. Those statistics are learned parameters just like model coefficients.

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train = scaler.fit_transform(train[feature_columns])
X_test = scaler.transform(test[feature_columns])
print(scaler.mean_)
```

`fit_transform` on training learns and applies the transformation. `transform` on test uses the already learned parameters. Calling `fit_transform` on test would define a different coordinate system and use held-out information.

A useful leakage check is to add a huge offset to test features in a copy. The fitted training scaler's mean must stay unchanged. The test predictions may worsen; that is evidence of distribution shift rather than a reason to refit on the test set.

## Keep the transformation and classifier together

```python
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression

model = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=1000, random_state=0),
)
model.fit(train[feature_columns], train.label)
predicted = model.predict(test[feature_columns])
print(model.named_steps["standardscaler"].mean_)
```

A pipeline makes it harder to forget scaling during inference. It does not choose your split for you. If you fit the pipeline on the entire table, you have still leaked test data.

Keep feature names, order, units, and window settings with the trained system. Swapping `rms` and `gyro_std` at inference changes the meaning of each input even if the array shape still matches.

## Validate data rather than hiding problems

Require finite numeric features and labels in the task's defined 0/1 set. A missing-data imputer is possible in a larger pipeline, but it too must learn only from training data. The supplied task rejects nonfinite features so the assumption is explicit.

Exclude identifiers and labels from predictors. Ensure the feature list is nonempty and unique. Duplicate names or columns can make array dimensions and feature interpretation ambiguous.

## Do not tune on the final test set

Repeatedly changing settings after seeing S04/S05 results makes those subjects a development set. If tuning is needed, use grouped validation within training subjects, then evaluate the untouched final test set once. With a small number of subjects, acknowledge the limits instead of manufacturing certainty through many window-level splits.

## Try it

1. Print subject IDs and class counts on each side of the split.
2. Fit a pipeline and compare predictions with the training-majority baseline.
3. Shift only the held-out features by +100 and confirm the training scaler mean is unchanged.
4. Intentionally fit on the full table in a disposable experiment. Explain precisely which information crossed the evaluation boundary.
5. Write an inference schema listing feature names, order, units, and preprocessing. State what should happen if any requirement is missing.

Next: [Evaluation and uncertainty](03_evaluation.md)
