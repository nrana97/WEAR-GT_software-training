"""Behavioral checks for Level 1: Sensors and time series: checkpoint."""
import unittest
import numpy as np
import pandas as pd
from audit import audit


class TestAudit(unittest.TestCase):
    def test_three_problems(self):
        df = pd.DataFrame({'timestamp_s':[0,.01,.02,.06,.07], 'raw':[10,np.nan,4095,np.inf,0]}, index=[8,9,10,11,12])
        original = df.copy(deep=True)
        out = audit(df)
        self.assertAlmostEqual(out['sample_rate_hz'],100)
        self.assertEqual(out['missing_values'],2)
        self.assertEqual(out['saturated_samples'],2)
        self.assertEqual(out['gap_after_indices'],[2])
        pd.testing.assert_frame_equal(df, original)
    def test_valid_and_invalid(self):
        self.assertEqual(audit(pd.DataFrame({'timestamp_s':[0,1,2], 'raw':[3,4,5]}))['gap_after_indices'], [])
        with self.assertRaises(ValueError): audit(pd.DataFrame({'timestamp_s':[0,0], 'raw':[1,2]}))


if __name__ == "__main__":
    unittest.main()
