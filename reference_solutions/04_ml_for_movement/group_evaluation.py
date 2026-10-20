import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def evaluate_subjects(df, feature_columns):
    """Evaluate fresh pipelines with each subject held out in turn."""
    features=list(feature_columns)
    if not features or len(set(features))!=len(features) or set(features)&{'subject_id','label'}:
        raise ValueError("Invalid features")
    if not {'subject_id','label',*features}.issubset(df.columns) or df.subject_id.isna().any() or not df.label.isin([0,1]).all():
        raise ValueError("Invalid schema/labels")
    try: x=df[features].to_numpy(dtype=float)
    except (ValueError,TypeError) as exc: raise ValueError("Invalid features") from exc
    if not np.isfinite(x).all(): raise ValueError("Nonfinite features")
    subjects=sorted(df.subject_id.unique())
    if len(subjects)<3: raise ValueError("Need at least three subjects")
    y=df.label.to_numpy(dtype=int); rows=[]
    for subject in subjects:
        test=(df.subject_id==subject).to_numpy()
        if len(set(y[~test]))!=2: raise ValueError("Each training fold needs both classes")
        model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000,random_state=0))
        model.fit(x[~test],y[~test]); predicted=model.predict(x[test])
        majority=int(np.bincount(y[~test],minlength=2).argmax())
        rows.append((subject,int(test.sum()),float(accuracy_score(y[test],predicted)),float(np.mean(y[test]==majority))))
    folds=pd.DataFrame(rows,columns=['subject_id','n_test','accuracy','baseline_accuracy'])
    return {'folds':folds,'mean_accuracy':float(folds.accuracy.mean()),'std_accuracy':float(folds.accuracy.std(ddof=1))}
