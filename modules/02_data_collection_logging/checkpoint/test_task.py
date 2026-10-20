"""Behavioral checks for Level 2: Data collection and logging: checkpoint."""
import unittest
import numpy as np
import pandas as pd
from align_streams import align


class TestAlign(unittest.TestCase):
    def test_offset_gaps_and_edges(self):
        a=pd.DataFrame({'timestamp_s':[0,.1,.2,.6], 'value':[0,1,2,6]})
        b=pd.DataFrame({'timestamp_s':[.2,.4,.6,.8], 'value':[0,2,4,6]})
        original=b.copy()
        out=align(a,b,[-.1,0,.05,.1,.2,.3,.6,.7],offset_b_s=-.2,max_gap_s=.21)
        np.testing.assert_allclose(out.a,[np.nan,0,.5,1,2,np.nan,6,np.nan],equal_nan=True)
        np.testing.assert_allclose(out.b,[np.nan,0,.5,1,2,3,6,np.nan],equal_nan=True)
        pd.testing.assert_frame_equal(original,b)
    def test_missing_and_invalid(self):
        a=pd.DataFrame({'timestamp_s':[0,.1,.2], 'value':[1,np.nan,3]})
        out=align(a,a,[0,.05,.1,.15,.2])
        np.testing.assert_allclose(out.a,[1,np.nan,np.nan,np.nan,3],equal_nan=True)
        with self.assertRaises(ValueError): align(a,a,[1,0])
        with self.assertRaises(ValueError): align(a,a,[0],max_gap_s=0)


if __name__ == "__main__":
    unittest.main()
