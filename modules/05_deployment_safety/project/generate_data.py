"""Create a small fault-replay input; no device communication."""
import pandas as pd
if __name__=='__main__':
    pd.DataFrame({'sample_time_s':[0,.02,.04,.06], 'now_s':[.01,.03,.25,.07],
                  'feature':[1,2,3,99], 'latency_s':[.001,.002,.001,.02]}).to_csv('sample.csv',index=False)
    print('Wrote sample.csv: simulated timing and fault cases')
