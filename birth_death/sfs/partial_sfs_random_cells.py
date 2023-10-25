import os

import pandas as pd
from matplotlib import pyplot as plt


def select_n_cells(set_no: str, rep: int, only_clone_0: bool = True):
    # rep = 10
    PATH = f'/Users/magdalena/PycharmProjects/rice/birth_death/results/{rep}'
    mutations = [file for file in os.listdir(PATH) if 'mu' in file][0]
    stats = [file for file in os.listdir(PATH) if 'stats' in file and 'clones' not in file][0]
    df_mutations = pd.read_excel(f'{PATH}/{mutations}', dtype=str)
    df_stats = pd.read_excel(f'{PATH}/{stats}', index_col=0, dtype=str)

    df_mutations = df_mutations.set_index(keys=['Unnamed: 0'])
    clone = df_stats['clone']

    for index in df_mutations.index:
        df_mutations.at[index, 'clone'] = int(clone[index])
    df_mutations = df_mutations.astype(int)

    df_1 = df_mutations.sample(n=100)
    df_1.to_excel(f'/Users/magdalena/PycharmProjects/rice/birth_death/results/{rep}/{stats[:-10]}partial_100_cells_mu_table.xlsx')

    df_clone_0 = df_1.loc[df_1['clone'] == 0].drop(columns=['clone'])
    clone_0_sum = df_clone_0.sum(axis=0).to_list()
    # df_clone_0.loc['freq'] = df_clone_0.sum(axis=0)
    clone_0_sum = list(filter(lambda num: num != 0, clone_0_sum))

    clone_0_sfs = {}
    for i in clone_0_sum:
        clone_0_sfs[i] = clone_0_sum.count(i)

    df_sfs_0 = pd.DataFrame([clone_0_sfs]).transpose().reset_index()
    df_sfs_0.rename(columns={0: 'clone 0', 'index': 'Number of cells'}, inplace=True)
    df_sfs_0.set_index('Number of cells', inplace=True)
    df_sfs_0 = df_sfs_0.groupby(df_sfs_0.index).sum()
    # df_sfs_0.to_excel(f'/Users/magdalena/PycharmProjects/rice/birth_death/results/{set_no}/constant_growth/{rep}/{stats[:-10]}sfs_partial_100_cells.xlsx')
    df_sfs_1 = pd.DataFrame()
    df_sfs_2 = pd.DataFrame()

    if not only_clone_0:
        df_clone_1 = df_1.loc[df_1['clone'] == 1].drop(columns=['clone'])
        clone_1_sum = df_clone_1.sum(axis=1).sort_values().to_list()
        clone_1_sfs = {i: clone_1_sum.count(i) for i in clone_1_sum}
        df_sfs_1 = pd.DataFrame([clone_1_sfs]).transpose().reset_index()
        df_sfs_1.rename(columns={0: 'Number of cells', 'index': 'clone 1'}, inplace=True)
        df_sfs_1.set_index('Number of cells', inplace=True)
        df_sfs_1 = df_sfs_1.groupby(df_sfs_1.index).sum()

        df_clone_2 = df_1.loc[df_1['clone'] == 2].drop(columns=['clone'])
        clone_2_sum = df_clone_2.sum(axis=1).sort_values().to_list()
        clone_2_sfs = {i: clone_2_sum.count(i) for i in clone_2_sum}
        df_sfs_2 = pd.DataFrame([clone_2_sfs]).transpose().reset_index()
        df_sfs_2.rename(columns={0: 'Number of cells', 'index': 'clone 2'}, inplace=True)
        df_sfs_2.set_index('Number of cells', inplace=True)
        df_sfs_2 = df_sfs_2.groupby(df_sfs_2.index).sum()
        #
        # # -------
    df_sfs = pd.concat([df_sfs_0, df_sfs_1, df_sfs_2], axis=1)
    df_sfs = df_sfs.groupby(df_sfs.index).sum()
    df_sfs.to_excel(f'/Users/magdalena/PycharmProjects/rice/birth_death/results/{rep}/{stats[:-10]}sfs_partial_100_cells.xlsx')
    x_range = list(range(1, max(df_sfs.index)))

    fig, ax = plt.subplots(figsize=(15, 15), dpi=80)
    colors = ["#264b96", "#27b376", '#bf212f']

    for number in x_range:
        if number not in df_sfs.index:
            df_sfs.at[number, 'clone 0'] = 0
            df_sfs.at[number, 'clone 1'] = 0
            df_sfs.at[number, 'clone 2'] = 0
    df_sfs = df_sfs.sort_index()

    df_sfs.plot.bar(alpha=0.65, color=colors, logy=True, fontsize=5, width=1., ax=ax)
    plt.savefig(f'/Users/magdalena/PycharmProjects/rice/birth_death/results/{rep}/{stats[:-10]}sfs-partial.png', dpi=300)


set_no = 'set 2'
for rep in range(40, 41):
    select_n_cells(set_no=set_no, only_clone_0=False, rep=rep)
