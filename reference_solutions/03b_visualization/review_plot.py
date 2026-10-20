import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def plot_session(df, units, out_path):
    """Save a labeled multi-channel offline review figure."""
    t=df['timestamp_s'].to_numpy(dtype=float)
    channels=[c for c in df if c!='timestamp_s']
    if len(t)<2 or not np.isfinite(t).all() or (np.diff(t)<=0).any() or not channels:
        raise ValueError("Invalid session")
    if not all(isinstance(units.get(c),str) and units[c].strip() for c in channels):
        raise ValueError("Supply every channel's units")
    values=[df[c].to_numpy(dtype=float) for c in channels]
    fig,grid=plt.subplots(len(channels),1,sharex=True,squeeze=False,figsize=(10,2.5*len(channels)))
    axes=grid[:,0]
    try:
        for ax,c,x in zip(axes,channels,values):
            ax.plot(t,np.where(np.isfinite(x),x,np.nan),label=c)
            ax.set_ylabel(f'{c} ({units[c]})')
            ax.grid(alpha=.2)
        axes[-1].set_xlabel('Time (s)')
        axes[0].set_title('Synthetic session review')
        fig.tight_layout()
        fig.savefig(out_path,dpi=140)
    except Exception:
        plt.close(fig)
        raise
    return fig,axes
