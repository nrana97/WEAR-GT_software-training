"""Behavioral checks for Level 4: ML for movement: project."""
import unittest
import numpy as np
import pandas as pd
from train_model import train_evaluate


class TestTraining(unittest.TestCase):
    def fixture(self):
        return pd.DataFrame({'subject_id':['A']*4+['B']*4+['C']*4,'label':[0,0,1,1]*3,'rms':[-2,-1,1,2]*3})
    def test_split_and_metrics(self):
        df=self.fixture(); before=df.copy()
        out=train_evaluate(df,['rms'],['C'])
        self.assertEqual(out['train_subjects'],['A','B'])
        self.assertEqual(out['test_subjects'],['C'])
        self.assertEqual(out['accuracy'],1)
        self.assertEqual(out['baseline_accuracy'],.5)
        np.testing.assert_array_equal(out['confusion_matrix'],[[2,0],[0,2]])
        scaler=out['model'].named_steps['standardscaler']
        self.assertAlmostEqual(scaler.mean_[0],df.loc[df.subject_id!='C','rms'].mean())
        pd.testing.assert_frame_equal(before,df)
    def test_scaler_does_not_see_test(self):
        df=self.fixture(); df.loc[df.subject_id=='C','rms']+=100
        out=train_evaluate(df,['rms'],['C'])
        self.assertAlmostEqual(out['model'].named_steps['standardscaler'].mean_[0],0)
    def test_rejections(self):
        for features,held in [(['subject_id'],['C']),(['rms'],['Z']),(['rms'],['A','B','C']),([],['C'])]:
            with self.assertRaises(ValueError): train_evaluate(self.fixture(),features,held)


if __name__ == "__main__":
    unittest.main()
