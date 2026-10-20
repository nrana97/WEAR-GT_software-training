"""Run after implementing the project starter. Synthetic data only."""
from inference import infer
import numpy as np

def main():
    # Scalar toy adapter; deliberately unrelated to actuator commands.
    predictor=lambda x: float(np.tanh(x.mean()/10))
    for features in ([1,2],[np.nan],[100]):
        print(features,infer(predictor,features))

if __name__=='__main__': main()
