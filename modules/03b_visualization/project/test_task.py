"""Behavioral checks for Level 3b: Visualization and dashboards: project."""
import unittest
import numpy as np
import pandas as pd
from review_plot import plot_session


import tempfile
from pathlib import Path
import matplotlib.pyplot as plt
class TestPlot(unittest.TestCase):
    def test_panels_labels_and_missing(self):
        df=pd.DataFrame({'timestamp_s':[0,1,2],'raw':[1,np.inf,2],'signal':[0,1,0]})
        before=df.copy()
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'plot.png'
            fig,axes=plot_session(df,{'raw':'count','signal':'a.u.'},p)
            try:
                self.assertEqual(len(axes),2)
                self.assertGreater(p.stat().st_size,1000)
                self.assertEqual(axes[0].get_ylabel(),'raw (count)')
                self.assertEqual(axes[-1].get_xlabel(),'Time (s)')
                self.assertTrue(np.isnan(axes[0].lines[0].get_ydata()[1]))
            finally: plt.close(fig)
        pd.testing.assert_frame_equal(before,df)
    def test_one_channel(self):
        with tempfile.TemporaryDirectory() as d:
            fig,axes=plot_session(pd.DataFrame({'timestamp_s':[0,1],'x':[2,3]}),{'x':'g'},Path(d)/'one.png')
            self.assertEqual(axes.shape,(1,))
            plt.close(fig)


if __name__ == "__main__":
    unittest.main()
