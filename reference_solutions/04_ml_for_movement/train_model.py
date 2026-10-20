import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, confusion_matrix

def train_evaluate(df, feature_columns, test_subjects):
    """Fit preprocessing on training subjects and evaluate held-out subjects."""
    features=list(feature_columns)
    if not features or len(set(features))!=len(features) or set(features)&{'label','subject_id'}:
        raise ValueError("Invalid features")
    if not {'subject_id','label',*features}.issubset(df.columns):
        raise ValueError("Missing columns")
    if df.subject_id.isna().any() or not df.label.isin([0,1]).all():
        raise ValueError("Invalid subject or label")
    try: x=df[features].to_numpy(dtype=float)
    except (ValueError,TypeError) as exc: raise ValueError("Nonnumeric features") from exc
    if not np.isfinite(x).all(): raise ValueError("Nonfinite features")
    held=set(test_subjects)
    subjects=set(df.subject_id)
    if not held or not held<=subjects: raise ValueError("Unknown/empty holdout")
    mask=df.subject_id.isin(held).to_numpy()
    if mask.all() or not mask.any() or len(set(df.loc[~mask,'label']))!=2:
        raise ValueError("Need training subjects with both classes")
    model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000,random_state=0))
    y=df.label.to_numpy(dtype=int)
    model.fit(x[~mask],y[~mask]); predicted=model.predict(x[mask])
    majority=int(np.bincount(y[~mask],minlength=2).argmax())
    return {'model':model,'accuracy':float(accuracy_score(y[mask],predicted)),
            'balanced_accuracy':float(balanced_accuracy_score(y[mask],predicted)),
            'baseline_accuracy':float(accuracy_score(y[mask],np.full(mask.sum(),majority))),
            'confusion_matrix':confusion_matrix(y[mask],predicted,labels=[0,1]),
            'train_subjects':sorted(subjects-held),'test_subjects':sorted(held)}
