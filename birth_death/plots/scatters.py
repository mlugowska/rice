import os

import pandas as pd
from matplotlib import pyplot as plt

PATH = '/Users/magdalena/PycharmProjects/rice/birth_death/results/1x/stats'


def plot_growth_rate():
    files = [file for file in os.listdir(PATH) if 'clones-stats' in file]
    df_r = pd.DataFrame(columns=['r 0', 'r 1', 'r 2'])

    for file in files:
        df = pd.read_excel(f'{PATH}/{file}', index_col=0)
        exp_r_0, exp_r_1, exp_r_2 = df.loc['exp. r']
        r_0, r_1, r_2 = df.loc['r']
        N = int(sum(df.loc['N']))

        df_r.at[f'N_{N}', 'r 0'] = r_0
        df_r.at[f'N_{N}', 'r 1'] = r_1
        df_r.at[f'N_{N}', 'r 2'] = r_2

    df_r = df_r.transpose()
    df_exp_r = pd.DataFrame(columns=['exp'], index=['r 0', 'r 1', 'r 2'])
    df_exp_r.loc['r 0'] = exp_r_0
    df_exp_r.loc['r 1'] = exp_r_1
    df_exp_r.loc['r 2'] = exp_r_2

    fig, ax = plt.subplots(1, 1)
    df_exp_r.plot(style='o', ax=ax)
    df_r.plot(style='.', ax=ax)

    fig.savefig(f'{PATH}/growth_rate_plot.png', dpi=500)

plot_growth_rate()
