# Lesson 3: Evaluate by subject and report limitations honestly

**Goal:** interpret model metrics, run leave-one-subject-out evaluation, and distinguish variation across subjects from statistical certainty.

**Allow 60–75 minutes**, including a short results report. Good evaluation is part of the engineering work, not a final formatting step.

## Report more than one number

For binary classification, include held-out subject IDs, number of windows per class, accuracy, balanced accuracy where meaningful, a labeled confusion matrix, and a baseline evaluated on identical test rows.

```python
from sklearn.metrics import confusion_matrix

truth = [0, 0, 1, 1, 1]
predicted = [0, 1, 0, 1, 1]
print(confusion_matrix(truth, predicted, labels=[0, 1]))
# [[1, 1],
#  [1, 2]]
```

Three of five windows are correct, so accuracy is 0.6. Class-0 recall is 1/2 and class-1 recall is 2/3; balanced accuracy is about 0.583. False positives and false negatives may have different practical consequences, so describe them rather than ranking every model by one aggregate metric.

## Pooled and per-subject scores answer different questions

Suppose one held-out subject has 900 windows at 90% accuracy and another has 100 windows at 50%. Pooled accuracy is 86%, while the unweighted mean subject accuracy is 70%.

```python
import numpy as np

n = np.array([900, 100])
accuracy = np.array([.9, .5])
print(np.average(accuracy, weights=n))  # .86
print(accuracy.mean())                 # .70
```

Neither calculation is inherently wrong. The first weights windows equally; the second weights subjects equally. Report which you use. A strong overall score can conceal poor performance on a particular subject.

## Leave one subject out

The checkpoint holds each subject out once and trains a fresh scaler/model on all remaining subjects. A six-subject fixture produces six folds:

```python
from generate_data import generate

df = generate()  # Run this example from the Module 04 project directory.
subjects = sorted(df.subject_id.unique())
for subject in subjects:
    test_mask = df.subject_id == subject
    train_fold = df.loc[~test_mask]
    test_fold = df.loc[test_mask]
    # Build and fit a NEW pipeline here.
    # Evaluate only this subject, then store its score and sample count.
```

Do not reuse an already fitted scaler or classifier between folds. Each fold represents a separate hypothetical deployment on an unseen subject. Both classes must remain in every training fold. A held-out subject may contain only one class in other datasets; report that limitation when choosing metrics.

Leave-one-subject-out results used for model selection become development evidence. They do not magically replace an independent final evaluation if you repeatedly optimize using them.

## Mean and standard deviation are not a confidence interval

```python
scores = np.array([.70, .80, .90])
print(scores.mean())        # .80
print(scores.std(ddof=1))   # .10
```

The sample standard deviation describes variation among held-out subject scores. It is not a 95% confidence interval, and mean ± standard deviation should not be described that way.

Window observations are correlated, especially with overlap. Bootstrapping individual windows can make uncertainty look artificially small. A subject-level bootstrap treats subjects as the resampling unit, but very small cohorts still give limited evidence. The checkpoint intentionally reports descriptive mean/std rather than claiming population-level confidence from a tiny synthetic cohort.

## Inspect errors and challenge assumptions

Look at errors by subject, activity, and data quality. Could placement changes, missing windows, label ambiguity, or a new sensor alter results? Was calibration learned without using test observations? Were all preprocessing choices made before final evaluation?

The fixture has an intentionally simple class relationship. High accuracy proves that your code can learn that relationship under the chosen split. It does not establish real-world activity recognition, clinical usefulness, or safe control.

## Try it

1. Recompute the confusion-matrix metrics above by hand and with scikit-learn.
2. Run leave-one-subject-out evaluation on the supplied fixture. Save the fold table with sample counts and baseline accuracy.
3. Compare pooled accuracy with the unweighted mean if you give one subject fewer windows.
4. Add noise to one subject in a separate robustness experiment. Describe what changes and what remains uncertain.
5. Write a one-page report: task, data, features, split, model, baseline, per-subject results, mistakes, and limitations. Label mean/std accurately.

Continue: [Project](../project/README.md) · [Checkpoint](../checkpoint/README.md)
