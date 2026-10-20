"""Behavioral checks for Level 3a: Signal processing: checkpoint."""
import unittest
import numpy as np
import pandas as pd
from cycles import cycle_features


class TestCycles(unittest.TestCase):
    def test_periodic(self):
        x=np.sin(2*np.pi*np.arange(1000)/100)
        events,f=cycle_features(x,100)
        np.testing.assert_array_equal(events,np.arange(25,1000,100))
        np.testing.assert_allclose(f.duration_s,1)
        np.testing.assert_allclose(f.rms,1/np.sqrt(2))
        np.testing.assert_allclose(f.peak_to_peak,2)
        self.assertEqual(len(f),9)
    def test_flat_and_bad(self):
        e,f=cycle_features(np.zeros(100),100)
        self.assertEqual(len(e),0)
        self.assertEqual(list(f.columns),['start','stop','duration_s','mean','rms','peak_to_peak'])
        for x,fs in [([np.nan],100),([1,2],0),([],100)]:
            with self.assertRaises(ValueError): cycle_features(x,fs)


if __name__ == "__main__":
    unittest.main()
