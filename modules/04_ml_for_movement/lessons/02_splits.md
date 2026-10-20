# Subject splits and preprocessing

Windows from one subject are correlated. Put every window from a subject in either training or test, never both. The same concern can apply to sessions and overlapping windows. Define the generalization question before choosing groups.

```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
model.fit(train[feature_columns], train.label)
```

The scaler learns only from training data because it is inside the pipeline. Never fit a scaler or feature selector on held-out subjects. Keep the final test set untouched while tuning; grouped cross-validation belongs inside the training set when tuning is needed.

**Review:** list every operation that learns parameters. Which dataset is allowed to fit each one?
