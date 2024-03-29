import os
import time
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from birth_death_model import BirthDeath
from cell_info import Cells
from plots import histograms
from utils import generate_tree, calculate_mean_birthtime, calculate_mean_deathtime, \
    calculate_mean_lifetime, show_tree


PATH = '/Users/magdalena/PycharmProjects/rice/birth_death/results'

"""
set up input parameters
"""

# b_0 = .016
# b_1 = .041
# b_2 = .155
b_0 = .1
b_1 = .3
b_2 = b_1

d_0 = .01
d_1 = .01
d_2 = .01
mu = .1
N0 = 1

T = 3500  # total time for running each simulation
t_1 = 20  # time of new clone 1 creation
t_2 = t_1  # time of new clone 2 creation
k = 30  # number of simulations to repeat
bd_list = []  # list to save all simulations
tree_list = []
mean_lifetimes = []
sfs_list = []

dt = 0.05
m_dt = np.around(np.arange(0, T + dt, dt), decimals=2)  # time sampling from 0 to T with step dt

n_extinct = 0

"""
simulation of continuous-time birth-and-death processes at birth and death event times
"""
k_i = 1

for _ in range(k):
    print(f'============= Create tree for k: {_} =============')
    bd = BirthDeath(b=b_0, d=d_0, N0=N0, mu=mu)  # create a simulation

    start = time.time()
    tree = generate_tree(bd=bd, b_0=b_0, b_1=b_1, b_2=b_2, T=T, k_i=k_i, k=_, t_1=t_1, t_2=t_2)
    end = time.time()
    print(f'run time: {end - start}')

    # bd_list.append(bd)
    # tree_list.append(tree)

    # # print(f'current population size = {bd.N}')
    #
    # # create df with N(m_dt): population size at each time point
    # # (time points same for all simulations to calculate average N)
    # if len(bd_list) == 1:
    #     df_N = pd.DataFrame(columns=m_dt, index=range(1, k + 1))
    #     df_N = df_N.fillna(0)
    # df_N = bd.count_N_in_timestep(df_N, k_i + 1, m_dt)
    if tree.tree:
        show_tree(tree.tree, N=bd.N, k=k, k_i=k_i)

        about_cell = Cells(tree, bd)
        about_cell.add_cells_path()
        about_cell.add_lifetimes(T)
        about_cell.add_mutations()
        about_cell.add_clone()
        df_mu_occur = about_cell.create_mutation_table()
        df_cells = about_cell.create_dataframe()

        mean_birthtime = calculate_mean_birthtime(df_cells)
        mean_deathtime = calculate_mean_deathtime(df_cells)
        mean_lifetime = calculate_mean_lifetime(df_cells)
        mean_lifetimes.append(mean_lifetime)

        print(f'mean birth: {mean_birthtime}')
        print(f'mean death: {mean_deathtime}')
        print(f'mean lifetime: {mean_lifetime}')

        if bd.mu:
            print(f'Expected number of mutations: {tree.expected_mutations_number()}')
            print(f'Number of mutations: {bd.events.count(2)}')

            df_growth = pd.DataFrame(columns=['clone 0', 'clone 1', 'clone 2'])
            df_growth.loc['exp. mutation time'] = [0, t_1, t_2]
            df_growth.loc['mutation time'] = [0, tree.mu_clone_1, tree.mu_clone_2]
            df_growth.loc['b'] = [b_0, b_1, b_2]
            df_growth.loc['d'] = [d_0, d_1, d_2]
            df_growth.loc['mu'] = [mu, mu, mu]
            df_growth.loc['N'] = [int(tree.N_0), int(tree.N_1), int(tree.N_2)]

            df_growth.loc['exp. r'] = [b_0 - d_0, b_1 - d_1, b_2 - d_2]

            def calculate_growth_rate(N, t=0):
                return np.log(N) / (bd.t - t) if N != 0 else np.nan

            df_growth.loc['r'] = [calculate_growth_rate(tree.N_0), calculate_growth_rate(tree.N_1, tree.mu_clone_1),
                                  calculate_growth_rate(tree.N_2, tree.mu_clone_2)]

            df_growth.loc['exp. no. mu [all clones]'] = [int(tree.expected_mutations_number()), np.nan, np.nan]
            df_growth.loc['no. mu [all clones]'] = [int(bd.events.count(2)), np.nan, np.nan]

            df_growth.to_excel(
                    f'{PATH}/N-{bd.N}/N-{bd.N}-clones-stats.xlsx')

            if not bd.extinct():
                df_mu_freq = about_cell.calculate_mutation_frequency()
                df_sfs_0, df_sfs_1, df_sfs_2 = about_cell.sfs(df_mu_freq)
                df_sfs_0['clone'] = 0
                df_sfs_1['clone'] = 1
                df_sfs_2['clone'] = 2

                df = pd.concat([df_sfs_0, df_sfs_1, df_sfs_2])
                try:
                    df_sfs = pd.DataFrame({
                        "clone 0": df[df['clone'] == 0][0],
                        "clone 1": df[df['clone'] == 1][0],
                        "clone 2": df[df['clone'] == 2][0]
                    }, index=df.index.drop_duplicates().sort_values())

                    df_sfs.to_excel(
                        f'{PATH}/N-{bd.N}/N-{bd.N}-sfs.xlsx')
                except ValueError:
                    pass
                # histograms.sfs(df_sfs)
                # plt.savefig(
                #     f'{PATH}/N-{bd.N}/N-{bd.N}-sfs.png', dpi=500)

        df_cells.to_excel(
            f'{PATH}/N-{bd.N}/N-{bd.N}-stats.xlsx')

        df_mu_occur.to_excel(
            f'{PATH}/N-{bd.N}/N-{bd.N}-mu-occur.xlsx')
        #
        # histograms.cells_life_distribution(df_cells, mean_lifetime)
        # plt.savefig(
        #     f'/Users/magdalena/PycharmProjects/rice/birth_death/results/{k}x/plots/{k_i}-N-{bd.N}-life-distribution.png', dpi=300)
