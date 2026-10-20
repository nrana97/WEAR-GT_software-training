"""Behavioral checks for Level 5: Deployment and safety: project."""
import unittest
import numpy as np
import pandas as pd
from inference import infer


class TestInference(unittest.TestCase):
    def clock(self,dt):
        values=iter([10,10+dt]); return lambda: next(values)
    def test_success_and_deadline(self):
        good=infer(lambda x:.5,[1],clock=self.clock(.005))
        self.assertEqual(good['reason'],'ok'); self.assertEqual(good['output'],.5)
        self.assertEqual(infer(lambda x:.5,[1],clock=self.clock(.02))['reason'],'deadline')
    def test_faults(self):
        for value in (np.nan,np.inf,2,[.2]):
            out=infer(lambda x:value,[1],clock=self.clock(.001))
            self.assertEqual(out['reason'],'invalid_output'); self.assertEqual(out['output'],0)
        for x in ([],[np.nan],[[1]],['bad']):
            self.assertEqual(infer(lambda x:.2,x)['reason'],'invalid_input')
        def broken(x): raise RuntimeError('simulated')
        self.assertEqual(infer(broken,[1],clock=self.clock(.001))['reason'],'model_error')
        with self.assertRaises(ValueError): infer(lambda x:0,[1],budget_s=0)


if __name__ == "__main__":
    unittest.main()
