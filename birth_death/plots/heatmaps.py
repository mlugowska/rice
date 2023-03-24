import os

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

PATH = '/Users/magdalena/PycharmProjects/rice/birth_death/results/1x/stats'
sort_cells = True
sort_mutations = True

files = [file for file in os.listdir(PATH) if 'mu-occur' in file]

# N = 490
# file = [stat for stat in files if f'{N}' in stat][0]
for file in files:
    mu = pd.read_excel(f'{PATH}/{file}', dtype=str)

    if sort_cells:
        mu = mu.sort_values(by=['Unnamed: 0'], ascending=True, key=lambda x: x.str.len(), kind='mergesort')

    mu = mu.set_index(keys=['Unnamed: 0'])
    mu = mu.astype(int)

    if sort_mutations:
        mu.loc['freq'] = mu.mean(axis=0)
        mu = mu.sort_values(mu.last_valid_index(), ascending=False, axis=1, kind='mergesort')

    fig, ax = plt.subplots(figsize=(50, 20), dpi=80)
    sns.heatmap(mu, annot=False, cmap=['#FFD00D', '#CB0100'], cbar=False, xticklabels=True, yticklabels=True, ax=ax)
    plt.yticks(rotation='horizontal', fontsize=2)
    plt.xticks(rotation='vertical', fontsize=2)
    plt.xlabel('Mutation')
    plt.ylabel('Cell')
    plt.savefig(f'/Users/magdalena/PycharmProjects/rice/birth_death/results/1x/plots/heatmaps/{file[:-11]}-sorted cell.png', dpi=300)


