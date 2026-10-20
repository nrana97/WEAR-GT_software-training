"""Behavioral checks for Level 5: Deployment and safety: checkpoint."""
import unittest
import numpy as np
import pandas as pd
from safety_loop import reset, step


class TestSafety(unittest.TestCase):
    def test_latch_and_reset(self):
        state={}; reset(state)
        self.assertEqual(step(state,lambda x:.5,[1],0,.01,.001),{'output':.5,'reason':'ok'})
        self.assertEqual(step(state,lambda x:.5,[1],0,.02,.001)['reason'],'replayed')
        self.assertEqual(state['fault'],'replayed')
        self.assertEqual(step(state,lambda x:.5,[1],.03,.04,.001)['reason'],'latched')
        reset(state)
        self.assertEqual(step(state,lambda x:.5,[1],.03,.04,.001)['reason'],'ok')
    def test_fault_injection_and_no_call(self):
        def broken(x): raise RuntimeError('fault')
        cases=[(lambda x:.2,[1],0,.2,.001,'stale'),(lambda x:.2,[np.nan],0,0,.001,'invalid_input'),
               (lambda x:.2,[11],0,0,.001,'invalid_input'),(lambda x:.2,[1],0,0,.02,'deadline'),
               (broken,[1],0,0,.001,'model_error'),(lambda x:np.inf,[1],0,0,.001,'invalid_output'),
               (lambda x:[.2],[1],0,0,.001,'invalid_output'),(lambda x:.2,[1],1,0,.001,'stale')]
        for predictor,x,s,n,l,reason in cases:
            state={}; reset(state)
            out=step(state,predictor,x,s,n,l)
            self.assertEqual(out,{'output':0.0,'reason':reason}); self.assertEqual(state['fault'],reason)
            self.assertIsNone(state['last_sample_s'])
        calls=[]; state={}; reset(state)
        step(state,lambda x:calls.append(x),[1],0,0,.02)
        self.assertEqual(calls,[])
    def test_inclusive_bounds(self):
        state={}; reset(state)
        self.assertEqual(step(state,lambda x:1,[10],0,.1,.01)['reason'],'ok')


if __name__ == "__main__":
    unittest.main()
