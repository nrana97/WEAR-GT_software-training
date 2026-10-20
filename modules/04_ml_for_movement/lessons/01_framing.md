# Lesson 1: Frame a movement problem and build a baseline

**Goal:** define an ML task, separate predictors from labels and identifiers, and choose a baseline before fitting a model.

**Allow 45–60 minutes**, including a metric calculation by hand. The training uses synthetic features; success here does not demonstrate performance on people.

## Begin with a concrete question

“Use AI on sensor data” is not a testable task. “Predict whether this synthetic window represents stillness or walking” gives a target, input unit, and evaluation scope.

Different tasks need different outputs:

| Task | Example target | Typical evaluation |
|---|---|---|
| Classification | Still versus walking | Confusion matrix, accuracy, balanced accuracy |
| Regression | Joint angle in degrees | Error in degrees, error by activity |
| State estimation | A changing latent movement state | Timing/estimation error against a reference |

The supplied project is binary classification: integer label 0 means still, 1 means walking. This is a teaching convention. Do not reinterpret the label as torque, intent certainty, or safety readiness.

## Understand the rows and columns

The generator produces six synthetic subjects with 80 windows each. It creates two features, `rms` and `gyro_std`, with class-related differences plus noise. These values are generated directly as a modeling fixture; they are not features extracted from an actual human recording.

```python
import pandas as pd

example = pd.DataFrame({
    "subject_id": ["S00", "S00", "S01", "S01"],
    "label": [0, 1, 0, 1],
    "rms": [.1, 1.6, .2, 1.4],
    "gyro_std": [.05, .9, .1, .8],
})
features = ["rms", "gyro_std"]
X = example[features]
y = example["label"]
```

`subject_id` describes provenance, `label` is the answer, and only the explicitly selected feature columns enter the model. Including the answer column makes evaluation meaningless. Including IDs can let a model learn recording-specific shortcuts rather than movement.

## Establish a baseline

A baseline tells you whether a more complicated system adds value. One simple baseline always predicts the majority class seen in training.

```python
import numpy as np

training_labels = np.array([0, 0, 0, 1])
counts = np.bincount(training_labels, minlength=2)
majority = int(counts.argmax())  # 0; ties also choose 0

test_labels = np.array([0, 1, 1, 0])
predictions = np.full(len(test_labels), majority)
print(np.mean(predictions == test_labels))  # .5
```

Determine the majority from training labels only, then evaluate it on the same test rows as the model. Choosing the baseline after inspecting test labels contaminates the comparison.

## Accuracy can hide the minority class

With 90 still windows and 10 walking windows, always predicting still gives 90% accuracy and zero ability to identify walking. Balanced accuracy averages recall across classes; if both classes are present, the always-still model has balanced accuracy 0.5.

```python
from sklearn.metrics import accuracy_score, balanced_accuracy_score, confusion_matrix

truth = np.array([0] * 90 + [1] * 10)
predicted = np.zeros(100, dtype=int)
print(accuracy_score(truth, predicted))           # .9
print(balanced_accuracy_score(truth, predicted))  # .5
print(confusion_matrix(truth, predicted, labels=[0, 1]))
# [[90, 0],
#  [10, 0]]
```

Rows are true class, columns predicted class. A fixed `[0,1]` label order keeps a two-by-two matrix even if one class is absent from a particular test set. In that case, some metrics cannot tell you how the absent class would perform; report the class support.

## Start with a model you can inspect

The exercises use standardized logistic regression. Its outputs support classification, but a high score is not a calibrated claim of real-world certainty. Neural networks are an optional extension after the baseline and split are trustworthy; extra complexity cannot fix leakage or incorrect labels.

## Try it

1. Write a one-paragraph task statement identifying input, target, intended held-out population, and a failure that matters.
2. Compute a majority baseline for balanced and imbalanced training labels. Explain the tie rule.
3. Reproduce the confusion matrix above and identify walking false negatives.
4. Add an accidental `label_copy` feature. Explain how to catch this leakage through schema review rather than celebrating a high score.
5. Run the supplied feature generator and inspect per-subject label counts and feature ranges before fitting anything.

Next: [Subject splits and preprocessing](02_splits.md)
