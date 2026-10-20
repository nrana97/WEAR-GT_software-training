"""Run after implementing the project starter. Synthetic data only."""
from generate_data import generate
from process_signal import lowpass, window_features
import matplotlib.pyplot as plt

def main():
    df=generate(); filtered=lowpass(df.signal,100)
    features=window_features(filtered)
    features.to_csv('window_features.csv',index=False)
    fig,ax=plt.subplots(figsize=(10,3))
    ax.plot(df.timestamp_s,df.signal,label='raw',alpha=.5)
    ax.plot(df.timestamp_s,filtered,label='5 Hz low-pass')
    ax.set(xlabel='Time (s)',ylabel='Synthetic signal (a.u.)',title='Offline filtering')
    ax.legend(); fig.tight_layout(); fig.savefig('filtered.png',dpi=140); plt.close(fig)
    print(features.head().to_string(index=False))

if __name__=='__main__': main()
