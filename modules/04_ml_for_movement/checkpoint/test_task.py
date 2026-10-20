"""Behavioral checks for Level 4: ML for movement: checkpoint."""
import unittest
import numpy as np
import pandas as pd
from group_evaluation import evaluate_subjects


from unittest.mock import patch
from sklearn.preprocessing import StandardScaler
class TestGroups(unittest.TestCase):
    def fixture(self):
        return pd.DataFrame({'subject_id':['A']*4+['B']*4+['C']*4,'label':[0,0,1,1]*3,'rms':[-2,-1,1,2]*3})
    def test_folds(self):
        out=evaluate_subjects(self.fixture(),['rms'])
        self.assertEqual(out['folds'].subject_id.tolist(),['A','B','C'])
        self.assertEqual(out['folds'].n_test.tolist(),[4,4,4])
        self.assertEqual(out['mean_accuracy'],1)
        self.assertEqual(out['std_accuracy'],0)
        np.testing.assert_allclose(out['folds'].baseline_accuracy,.5)
    def test_fresh_training_only_scalers(self):
        df=self.fixture(); df.loc[df.subject_id=='C','rms']+=10
        seen=[]; original=StandardScaler.fit
        def spy(obj,x,y=None,**kwargs):
            seen.append(np.asarray(x).copy())
            return original(obj,x,y,**kwargs)
        with patch.object(StandardScaler,'fit',spy): evaluate_subjects(df,['rms'])
        self.assertEqual(len(seen),3)
        for data,subject in zip(seen,['A','B','C']):
            np.testing.assert_allclose(data,df.loc[df.subject_id!=subject,['rms']].to_numpy())
    def test_validation(self):
        df=self.fixture().astype({'rms':float})
        with self.assertRaises(ValueError): evaluate_subjects(df[df.subject_id!='C'],['rms'])
        df.loc[0,'rms']=np.inf
        with self.assertRaises(ValueError): evaluate_subjects(df,['rms'])


if __name__ == "__main__":
    unittest.main()
