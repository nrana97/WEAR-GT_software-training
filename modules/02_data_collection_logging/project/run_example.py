"""Run after implementing the project starter. Synthetic data only."""
from generate_data import generate
from session_logger import write_session
from pathlib import Path
import tempfile

def main():
    metadata=dict(session_id='demo',subject_id='synthetic_01',task='simulated_walk',sensor_placement='simulated_ankle',firmware_version='sim_1')
    # Use a unique output directory; never overwrite an earlier session.
    directory=Path(tempfile.mkdtemp(prefix='wear-demo-',dir='.'))/'session'
    print('Session saved:',write_session(generate(),metadata,directory))

if __name__=='__main__': main()
