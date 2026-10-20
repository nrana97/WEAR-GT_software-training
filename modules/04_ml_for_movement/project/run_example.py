"""Run after implementing the project starter. Synthetic data only."""
from generate_data import generate
from train_model import train_evaluate

def main():
    result=train_evaluate(generate(),['rms','gyro_std'],['S04','S05'])
    for key in ('train_subjects','test_subjects','accuracy','balanced_accuracy','baseline_accuracy','confusion_matrix'):
        print(f'{key}: {result[key]}')

if __name__=='__main__': main()
