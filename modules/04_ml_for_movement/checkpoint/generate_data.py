"""Synthetic labeled features, six subjects, deterministic seed."""
import numpy as np
import pandas as pd

def generate(seed=42):
    rng=np.random.default_rng(seed); rows=[]
    for subject in range(6):
        offset=rng.normal(0,.1)
        for i in range(80):
            label=i%2
            rows.append((f"S{subject:02d}",label,offset+label*1.5+rng.normal(0,.25),label*.8+rng.normal(0,.2)))
    return pd.DataFrame(rows,columns=['subject_id','label','rms','gyro_std'])

if __name__=='__main__':
    generate().to_csv('features.csv',index=False)
    print('Wrote features.csv: synthetic features only; no human measurements')
