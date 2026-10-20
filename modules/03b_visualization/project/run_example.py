"""Run after implementing the project starter. Synthetic data only."""
from generate_data import generate
from review_plot import plot_session
import matplotlib.pyplot as plt

def main():
    fig,_=plot_session(generate(),{'raw':'count','signal':'a.u.'},'session_review.png')
    plt.close(fig)
    print('Wrote session_review.png')

if __name__=='__main__': main()
