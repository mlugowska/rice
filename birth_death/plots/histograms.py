import numpy as np
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

# -----------  SFS
import os
rep = 40
PATH = f'/Users/magdalena/PycharmProjects/rice/birth_death/results/{rep}'
file = [file for file in os.listdir(PATH) if 'sfs.xlsx' in file][0]

# N = 490
# file = [stat for stat in files if f'{N}' in stat][0]

df = pd.read_excel(f'{PATH}/{file}', index_col=0)
x_range = list(range(1, max(df.index)))

for number in x_range:
    if number not in df.index:
        df.at[number, 'clone 0'] = 0
        df.at[number, 'clone 1'] = 0
        df.at[number, 'clone 2'] = 0
df = df.sort_index()
df.fillna(0, inplace=True)

fig, ax = plt.subplots(figsize=(15, 15), dpi=80)
colors = ["#264b96", "#27b376", '#bf212f']
df.plot.bar(alpha=0.65, color=colors, logy=True, fontsize=5, width=1., ax=ax)
# for p in ax.patches:
#     ax.annotate(f'{p.get_height()}', (p.get_x() + 0.25, p.get_height() + 0.01))
plt.savefig(f'/Users/magdalena/PycharmProjects/rice/birth_death/results/{rep}/{file[:-5]}.png', dpi=300)


# ----------- PARTIAL SFS
# import os
#
# rep = 10
# PATH = f'/Users/magdalena/PycharmProjects/rice/birth_death/results/{rep}'
# mutations = [file for file in os.listdir(PATH) if 'mu' in file][0]
# stats = [file for file in os.listdir(PATH) if 'stats' in file][0]
# df_mutations = pd.read_excel(f'{PATH}/{mutations}', dtype=str)
# df_stats = pd.read_excel(f'{PATH}/{stats}', index_col=0, dtype=str)
#
# df_mutations = df_mutations.set_index(keys=['Unnamed: 0'])
# clone = df_stats['clone']
#
# for index in df_mutations.index:
#     df_mutations.at[index, 'clone'] = int(clone[index])
# df_mutations = df_mutations.astype(int)
#
# df_1 = df_mutations.sample(n=100)
#
# df_clone_0 = df_1.loc[df_1['clone'] == 0].drop(columns=['clone'])
# clone_0_sum = df_clone_0.sum(axis=0).to_list()
# # df_clone_0.loc['freq'] = df_clone_0.sum(axis=0)
# clone_0_sum = list(filter(lambda num: num != 0, clone_0_sum))
#
# clone_0_sfs = {}
# for i in clone_0_sum:
#     clone_0_sfs[i] = clone_0_sum.count(i)
#
# df_sfs_0 = pd.DataFrame([clone_0_sfs]).transpose().reset_index()
# df_sfs_0.rename(columns={0: 'clone 0', 'index': 'Number of cells'}, inplace=True)
# df_sfs_0.set_index('Number of cells', inplace=True)
# df_sfs_0 = df_sfs_0.groupby(df_sfs_0.index).sum()
# df_sfs_0.to_excel(f'/Users/magdalena/PycharmProjects/rice/birth_death/results/{rep}/{stats[:-10]}sfs_partial_100_cells.xlsx')

# df_clone_1 = df_1.loc[df_1['clone'] == 1].drop(columns=['clone'])
# clone_1_sum = df_clone_1.sum(axis=1).sort_values().to_list()
# clone_1_sfs = {i: clone_1_sum.count(i) for i in clone_1_sum}
# df_sfs_1 = pd.DataFrame([clone_1_sfs]).transpose().reset_index()
# df_sfs_1.rename(columns={0: 'Number of cells', 'index': 'clone 1'}, inplace=True)
# df_sfs_1.set_index('Number of cells', inplace=True)
# df_sfs_1 = df_sfs_1.groupby(df_sfs_1.index).sum()
#
# df_clone_2 = df_1.loc[df_1['clone'] == 2].drop(columns=['clone'])
# clone_2_sum = df_clone_2.sum(axis=1).sort_values().to_list()
# clone_2_sfs = {i: clone_2_sum.count(i) for i in clone_2_sum}
# df_sfs_2 = pd.DataFrame([clone_2_sfs]).transpose().reset_index()
# df_sfs_2.rename(columns={0: 'Number of cells', 'index': 'clone 2'}, inplace=True)
# df_sfs_2.set_index('Number of cells', inplace=True)
# df_sfs_2 = df_sfs_2.groupby(df_sfs_2.index).sum()
# #
# # # -------
# df_sfs = pd.concat([df_sfs_0, df_sfs_1, df_sfs_2], axis=1)
# df_sfs = df_sfs.groupby(df_sfs.index).sum()
# x_range = list(range(1, max(df_sfs.index)))
#
# fig, ax = plt.subplots(figsize=(15, 15), dpi=80)
# colors = ["#264b96", "#27b376", '#bf212f']
#
# for number in x_range:
#     if number not in df_sfs.index:
#         df_sfs.at[number, 'clone 0'] = 0
#         df_sfs.at[number, 'clone 1'] = 0
#         df_sfs.at[number, 'clone 2'] = 0
# df_sfs = df_sfs.sort_index()
#
# df_sfs.plot.bar(alpha=0.65, color=colors, logy=True, fontsize=5, width=1., ax=ax)
# plt.savefig(f'/Users/magdalena/PycharmProjects/rice/birth_death/results/{rep}/{stats[:-10]}sfs-partial.png', dpi=300)
