import time
import numpy as np

def infer(predict, features, budget_s=0.01, clock=None):
    """Run bounded scalar inference in simulation; report late returned results."""
    if not np.isfinite(budget_s) or budget_s<=0: raise ValueError("Invalid deadline")
    try: x=np.asarray(features,dtype=float)
    except (TypeError,ValueError): return {'output':0.0,'latency_s':0.0,'reason':'invalid_input'}
    if x.ndim!=1 or not len(x) or not np.isfinite(x).all():
        return {'output':0.0,'latency_s':0.0,'reason':'invalid_input'}
    clock=time.perf_counter if clock is None else clock
    start=clock()
    try: value=predict(x)
    except Exception:
        return {'output':0.0,'latency_s':float(clock()-start),'reason':'model_error'}
    elapsed=float(clock()-start)
    if not np.isfinite(elapsed) or elapsed<0 or elapsed>budget_s:
        return {'output':0.0,'latency_s':elapsed,'reason':'deadline'}
    try:
        result=np.asarray(value,dtype=float)
        valid=result.ndim==0 and np.isfinite(result).item() and -1<=float(result)<=1
    except (ValueError,TypeError): valid=False
    if not valid: return {'output':0.0,'latency_s':elapsed,'reason':'invalid_output'}
    return {'output':float(result),'latency_s':elapsed,'reason':'ok'}
