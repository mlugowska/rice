import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from utils import calculate_mean_bd


def N_freq_in_random_timesteps(df: pd.DataFrame):
    nth_t = df[df.columns[::7]]  # select every n-th column with time point
    mean_N_in_m_dt = calculate_mean_bd(df)
    mean_nth_t = mean_N_in_m_dt[df.columns[::7]].apply(np.floor)

    fig, axes = plt.subplots(len(nth_t.columns) // 3, 3, figsize=(8, 8))

    i = 0
    for tri_axis in axes:
        for axis in tri_axis:
            # draw hist with labels
            counts, edges, bars = axis.hist(nth_t[nth_t.columns[i]])
            axis.bar_label(bars, fontsize=6)

            min_ylim, max_ylim = plt.ylim()
            min_xlim, max_xlim = plt.xlim()

            # draw mean N
            x_mean = mean_nth_t[nth_t.columns[i]]
            axis.axvline(x_mean, linestyle='dashed', linewidth=1, color='red')
            axis.text(max_xlim * .95, max_ylim * .95, f'mean: {x_mean:.0f}', horizontalalignment='right',
                      verticalalignment='top', transform=axis.transAxes, fontsize=8)

            # add skew info
            # 𝐴𝑠>0- asymetria prawostronna (prawostronna skośność):
            # dominanta < mediana < średnia
            # prawa strona (prawy ogon rozkładu) jest dłuższy
            # im większe 𝐴𝑠 tym mocniejsza prawostronna skośność
            skew = nth_t[nth_t.columns[i]].skew()
            axis.text(max_xlim * .95, max_ylim * .8, f'skewness: {skew:.2f}', horizontalalignment='right',
                      verticalalignment='top', transform=axis.transAxes, fontsize=8)

            # set plot title
            axis.set_title(f't = {nth_t.columns[i]}')
            i += 1
        plt.tight_layout()

    fig.supxlabel('N')
    fig.supylabel('Frequency')

