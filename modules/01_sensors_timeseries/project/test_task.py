"""Behavioral checks for Level 1: Sensors and time series: project."""
import unittest
import numpy as np
import pandas as pd
from calibrate import convert_counts, sampling_rate


class TestCalibration(unittest.TestCase):
    def test_units_and_missing(self):
        np.testing.assert_allclose(convert_counts([0, 2047.5, 4095, np.nan]), [-5, 0, 5, np.nan], equal_nan=True)
    def test_custom_calibration(self):
        np.testing.assert_allclose(convert_counts([0, 100], 2, 100, 1, .5), [-2, 2])
    def test_invalid(self):
        for x in ([-1], [4096], [np.inf]):
            with self.assertRaises(ValueError): convert_counts(x)
        with self.assertRaises(ValueError): convert_counts([0], sensitivity_v_per_g=0)
    def test_rate(self):
        self.assertAlmostEqual(sampling_rate([0, .01, .02, .05, .06]), 100)
        for x in ([0,0], [1,0], [0,np.nan], [0], [[0,1]]):
            with self.assertRaises(ValueError): sampling_rate(x)


if __name__ == "__main__":
    unittest.main()
