import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def review(df, units, events, out_path):
    """Save an event-overlay review with channel quality summaries."""
    t=df['timestamp_s'].to_numpy(dtype=float)
    channels=[c for c in df if c!='timestamp_s']
    if len(t)<2 or not np.isfinite(t).all() or (np.diff(t)<=0).any() or not channels:
        raise ValueError("Invalid session")
    if not all(isinstance(units.get(c),str) and units[c].strip() for c in channels):
        raise ValueError("Missing units")
    events=np.asarray(events,dtype=float)
    if events.ndim!=1 or not np.isfinite(events).all() or ((events<t[0]) | (events>t[-1])).any():
        raise ValueError("Invalid events")
    quality={}
    values={c:df[c].to_numpy(dtype=float) for c in channels}
    fig,grid=plt.subplots(len(channels),1,sharex=True,squeeze=False,figsize=(10,3*len(channels)))
    axes=grid[:,0]
    try:
        for ax,c in zip(axes,channels):
            x=values[c]; finite=x[np.isfinite(x)]
            quality[c]={'missing_samples':int((~np.isfinite(x)).sum()),'constant':bool(len(finite)>0 and np.all(finite==finite[0]))}
            ax.plot(t,np.where(np.isfinite(x),x,np.nan),label=c)
            for i,event in enumerate(events):
                ax.axvline(event,linestyle='--',color='black',alpha=.5,label='event' if i==0 else None)
            ax.set_ylabel(f'{c} ({units[c]})')
            ax.set_title(f"{c}: missing={quality[c]['missing_samples']}, constant={quality[c]['constant']}")
            ax.legend()
        axes[-1].set_xlabel('Time (s)')
        fig.tight_layout(); fig.savefig(out_path,dpi=140)
    except Exception:
        plt.close(fig); raise
    return fig,axes,quality

def visible_window(df, end_s, width_s=2.0):
    """Select a finite-duration replay view, including both boundaries."""
    if not np.isfinite(end_s) or not np.isfinite(width_s) or width_s<=0:
        raise ValueError("Invalid replay interval")
    return df.loc[df.timestamp_s.between(end_s-width_s,end_s)].copy()
