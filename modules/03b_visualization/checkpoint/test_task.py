"""Behavioral checks for Level 3b: Visualization and dashboards: checkpoint."""
import unittest
import numpy as np
import pandas as pd
from dashboard import review, visible_window


import tempfile
from pathlib import Path
import matplotlib.pyplot as plt
class TestReview(unittest.TestCase):
    def test_quality_and_events(self):
        df=pd.DataFrame({'timestamp_s':[0,1,2,3],'x':[2,np.nan,2,2],'y':[np.nan,np.inf,np.nan,np.nan]})
        with tempfile.TemporaryDirectory() as d:
            fig,axes,q=review(df,{'x':'g','y':'V'},[1,2],Path(d)/'review.png')
            try:
                self.assertEqual(q,{'x':{'missing_samples':1,'constant':True},'y':{'missing_samples':4,'constant':False}})
                self.assertTrue(all(len(ax.lines)==3 for ax in axes))
                self.assertEqual(axes[0].get_legend_handles_labels()[1],['x','event'])
            finally: plt.close(fig)
            with self.assertRaises(ValueError): review(df,{'x':'g','y':'V'},[4],Path(d)/'bad.png')
    def test_replay_copy(self):
        df=pd.DataFrame({'timestamp_s':[0,1,2,3],'x':[1,2,3,4]})
        out=visible_window(df,2,1)
        self.assertEqual(out.timestamp_s.tolist(),[1,2])
        out.loc[:,'x']=99
        self.assertEqual(df.x.tolist(),[1,2,3,4])
        with self.assertRaises(ValueError): visible_window(df,2,0)


if __name__ == "__main__":
    unittest.main()
