"""Behavioral checks for Level 3a: Signal processing: project."""
import unittest
import numpy as np
import pandas as pd
from process_signal import lowpass, window_features


class TestProcessing(unittest.TestCase):
    def test_attenuation(self):
        t=np.arange(2000)/100
        target=np.sin(2*np.pi*t)
        x=target+.5*np.sin(2*np.pi*20*t)
        y=lowpass(x,100)
        self.assertEqual(y.shape,x.shape)
        self.assertLess(np.sqrt(np.mean((y[100:-100]-target[100:-100])**2)), .03)
    def test_features(self):
        f=window_features([1,-1,1,-1,8],4,2)
        self.assertEqual(f[['start','stop']].values.tolist(),[[0,4]])
        np.testing.assert_allclose(f[['mean','std','rms']].values,[[0,1,1]])
        self.assertTrue(window_features([1],2,1).empty)
    def test_validation(self):
        for x,fs,c in [([1]*100,100,50),([np.nan]*100,100,5),([1,2],100,5)]:
            with self.assertRaises(ValueError): lowpass(x,fs,c)
        with self.assertRaises(ValueError): window_features([1,2],0,1)


if __name__ == "__main__":
    unittest.main()
