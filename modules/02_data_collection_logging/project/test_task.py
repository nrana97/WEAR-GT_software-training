"""Behavioral checks for Level 2: Data collection and logging: project."""
import unittest
import numpy as np
import pandas as pd
from session_logger import write_session


import tempfile
import json
from pathlib import Path
class TestSession(unittest.TestCase):
    def test_roundtrip_and_no_overwrite(self):
        df=pd.DataFrame({'timestamp_s':[0,.1,.2], 'imu':[1,np.nan,3]})
        meta=dict(session_id='s01',subject_id='synthetic',task='walk',sensor_placement='ankle',firmware_version='sim1')
        with tempfile.TemporaryDirectory() as d:
            p=write_session(df,meta,Path(d)/'session')
            pd.testing.assert_frame_equal(pd.read_csv(p/'samples.csv'),df,check_dtype=False)
            self.assertEqual(json.loads((p/'metadata.json').read_text()),meta)
            with self.assertRaises(FileExistsError): write_session(df,meta,p)
    def test_invalid_leaves_no_directory(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad'
            with self.assertRaises(ValueError): write_session(pd.DataFrame({'timestamp_s':[0,0],'x':[1,2]}),{},p)
            self.assertFalse(p.exists())


if __name__ == "__main__":
    unittest.main()
