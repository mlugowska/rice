import pandas as pd
from matplotlib import pyplot as plt


def normalize_N(df):
    from sklearn.preprocessing import MinMaxScaler

    scaler = MinMaxScaler()
    scaled_values = scaler.fit_transform(df)
    df.loc[:, :] = scaled_values
    return df


def N_freq_in_specific_timesteps(df: pd.DataFrame):
    df = normalize_N(df)

    nth_t = df[df.columns[::7]]  # select every n-th column with time point
    # mean_N_in_m_dt = calculate_mean_bd(df)
    # mean_nth_t = mean_N_in_m_dt[df.columns[::7]].apply(np.floor)

    fig, axes = plt.subplots(len(nth_t.columns) // 3, 3, figsize=(8, 8))

    i = 0
    for tri_axis in axes:
        for axis in tri_axis:
            # draw hist with labels
            data = nth_t[nth_t.columns[i]]
            counts, edges, bars = axis.hist(data)
            axis.bar_label(bars, fontsize=6)

            min_ylim, max_ylim = plt.ylim()
            min_xlim, max_xlim = plt.xlim()

            # draw mean N
            # x_mean = mean_nth_t[nth_t.columns[i]]
            # axis.axvline(x_mean, linestyle='dashed', linewidth=1, color='red')
            # axis.text(max_xlim * .95, max_ylim * .95, f'mean: {x_mean:.0f}', horizontalalignment='right',
            #           verticalalignment='top', transform=axis.transAxes, fontsize=8)

            # add skew info
            # 𝐴𝑠>0- asymetria prawostronna (prawostronna skośność):
            # dominanta < mediana < średnia
            # prawa strona (prawy ogon rozkładu) jest dłuższy
            # im większe 𝐴𝑠 tym mocniejsza prawostronna skośność
            skew = nth_t[nth_t.columns[i]].skew()
            axis.text(max_xlim * .95, max_ylim * .9, f'skewness: {skew:.2f}', horizontalalignment='right',
                      verticalalignment='top', transform=axis.transAxes, fontsize=8)

            # set plot title
            axis.set_title(f't = {nth_t.columns[i]}')
            i += 1
    plt.tight_layout()

    fig.supxlabel('N')
    fig.supylabel('Frequency')


def cells_life_distribution(df, mean_lifetime):
    fig, ax = plt.subplots(figsize=(6, 4))

    lifetime = df.loc[df["lifetime"] != 0.0]["lifetime"]

    lifetime.plot(kind='hist', density=True, alpha=0.65, bins=15)

    ax.set_xlim(0, max(lifetime + 0.05))
    min_ylim, max_ylim = plt.ylim()

    ax.axvline(mean_lifetime, alpha=0.65, linestyle=":")
    ax.text(mean_lifetime + .01, max_ylim * .9, f'{mean_lifetime:.2f}', color='steelblue')

    ax.set_xlabel('Lifetime')
    ax.set_ylabel('Frequency')
    ax.set_title('Cells lifetimes distribution')

    plt.legend(['lifetime', 'mean'])


def sfs(df):
    fig, ax = plt.subplots(figsize=(15, 15), dpi=80)

    colors = ["#264b96", "#27b376", '#bf212f']

    x_range = list(range(1, max(df.index)))

    for number in x_range:
        if number not in df.index:
            df.at[number, 'clone 0'] = 0
            df.at[number, 'clone 1'] = 0
            df.at[number, 'clone 2'] = 0
    df = df.sort_index()

    df.plot.bar(alpha=0.65, color=colors, logy=True, fontsize=6, align='center')

    for p in ax.patches:
        ax.annotate(f'{p.get_height()}', (p.get_x() + 0.25, p.get_height() + 0.01))

    ax.set_xlabel('Number of cells', fontsize=8)
    ax.set_ylabel('Number of mutations', fontsize=8)
    ax.set_title('Mean SFS', fontsize=10)


# import os
#
# PATH = '/Users/magdalena/PycharmProjects/rice/birth_death/results/1x/stats'
# files = [file for file in os.listdir(PATH) if 'sfs' in file]
#
# N = 490
# file = [stat for stat in files if f'{N}' in stat][0]
#
# df = pd.read_excel(f'{PATH}/{file}', index_col=0)
# x_range = list(range(1, max(df.index)))
#
# for number in x_range:
#     if number not in df.index:
#         df.at[number, 'clone 0'] = 0
#         df.at[number, 'clone 1'] = 0
#         df.at[number, 'clone 2'] = 0
# df = df.sort_index()
# df.fillna(0, inplace=True)
#
# fig, ax = plt.subplots(figsize=(15, 15), dpi=80)
# colors = ["#264b96", "#27b376", '#bf212f']
# df.plot.bar(alpha=0.65, color=colors, logy=True, logx=True, fontsize=5, width=1., ax=ax)
# # for p in ax.patches:
# #     ax.annotate(f'{p.get_height()}', (p.get_x() + 0.25, p.get_height() + 0.01))
# # plt.savefig(f'/Users/magdalena/PycharmProjects/rice/birth_death/results/1x/plots/{file[:-5]}.png', dpi=300)
