import numpy as np

def reset(state):
    """Explicitly clear the simulated fault latch and timestamp history."""
    state.clear(); state.update(fault=None,last_sample_s=None)

def step(state, predict, features, sample_time_s, now_s, latency_s, max_age_s=0.1, budget_s=0.01, input_limit=10.0):
    """Simulated latched monitor; latency_s is injected, never a real guarantee."""
    if not all(np.isfinite(v) and v>0 for v in (max_age_s,budget_s,input_limit)):
        raise ValueError("Invalid limits")
    if state.get('fault') is not None: return {'output':0.0,'reason':'latched'}
    def fault(reason):
        state['fault']=reason
        return {'output':0.0,'reason':reason}
    if not np.isfinite(sample_time_s) or not np.isfinite(now_s) or not 0<=now_s-sample_time_s<=max_age_s:
        return fault('stale')
    previous=state.get('last_sample_s')
    if previous is not None and sample_time_s<=previous: return fault('replayed')
    try: x=np.asarray(features,dtype=float)
    except (ValueError,TypeError): return fault('invalid_input')
    if x.ndim!=1 or not len(x) or not np.isfinite(x).all() or (np.abs(x)>input_limit).any():
        return fault('invalid_input')
    if not np.isfinite(latency_s) or not 0<=latency_s<=budget_s: return fault('deadline')
    try: result=predict(x)
    except Exception: return fault('model_error')
    try:
        result=np.asarray(result,dtype=float)
        valid=result.ndim==0 and np.isfinite(result).item() and -1<=float(result)<=1
    except (ValueError,TypeError): valid=False
    if not valid: return fault('invalid_output')
    state['last_sample_s']=float(sample_time_s)
    return {'output':float(result),'reason':'ok'}
