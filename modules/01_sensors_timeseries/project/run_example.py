"""Run after implementing the project starter. Synthetic data only."""
from generate_data import generate
from calibrate import convert_counts, sampling_rate
import matplotlib.pyplot as plt

def main():
    df=generate()
    g=convert_counts(df.raw)
    print(f"Estimated rate: {sampling_rate(df.timestamp_s):.1f} Hz")
    fig,ax=plt.subplots(figsize=(10,3))
    ax.plot(df.timestamp_s,g)
    ax.set(xlabel='Time (s)',ylabel='Acceleration (g)',title='Synthetic teaching accelerometer')
    fig.tight_layout(); fig.savefig('calibration.png',dpi=140); plt.close(fig)

if __name__=='__main__': main()
