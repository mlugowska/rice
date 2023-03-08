"""
https://cmp.phys.ufl.edu/PHZ4710/files/unit3/birth-death.html
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from birth_death_model import BirthDeath
from plots import bd_trajectory, histograms
from utils import generate_tree, count_extinct_bd, calculate_mean_birthtime, calculate_mean_deathtime, \
    calculate_mean_lifetime, mean_sfs, show_tree
from cell_info import Cells

# import pdb; pdb.set_trace()
# show_tree('/Users/magdalena/PycharmProjects/rice/birth_death/results/1x/trees/0-N-279.txt')
"""
set up input parameters
"""

b = .162
d = .1
mu = .2
N0 = 1

T = 17  # total time for running each simulation
s = 10  # time of new clone creation
k = 1  # number of simulations to repeat
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

for k_i in range(k):
    print(f'============= Create tree for k: {k_i} =============')
    bd = BirthDeath(b=b, d=d, N0=N0, mu=mu)  # create a simulation
    b_0 = b
    b_1 = 5 * b
    b_2 = 7 * b
    # bd_1 = BirthDeath(b=5 * b, d=d, N0=N0, mu=mu)  # create a simulation
    # bd_2 = BirthDeath(b=10 * b, d=d, N0=N0, mu=mu)  # create a simulation
    tree = generate_tree(bd=bd, b_0=b_0, b_1=b_1, b_2=b_2, T=T, k_i=k_i, k=k, s=s)
    # print(f'current population size = {bd.N}')
    #
    bd_list.append(bd)
    tree_list.append(tree)
    #
    # # print(f'current population size = {bd.N}')
    #
    # # create df with N(m_dt): population size at each time point
    # # (time points same for all simulations to calculate average N)
    # if len(bd_list) == 1:
    #     df_N = pd.DataFrame(columns=m_dt, index=range(1, k + 1))
    #     df_N = df_N.fillna(0)
    # df_N = bd.count_N_in_timestep(df_N, k_i + 1, m_dt)

"""
generate cells statistics
"""
for k_i, bd in enumerate(bd_list):
    print(f'============= Generate statistics for k: {k_i} =============')
    tree = tree_list[k_i]
    if tree.tree:
        about_cell = Cells(tree)
        about_cell.add_cells_path()
        about_cell.add_lifetimes(T)
        about_cell.add_mutations()
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

            df_cells['expected no. mu'] = tree.expected_mutations_number()
            df_cells['no. mu'] = bd.events.count(2)

            if not bd.extinct():
                df_mu_freq = about_cell.calculate_mutation_frequency()
                df_sfs_0, df_sfs_1, df_sfs_2 = about_cell.sfs(df_mu_freq)
                df_sfs_0['clone'] = 0
                df_sfs_1['clone'] = 1
                df_sfs_2['clone'] = 2

                df = pd.concat([df_sfs_0, df_sfs_1, df_sfs_2])

                df_sfs = pd.DataFrame({
                    "clone 0": df[df['clone'] == 0][0],
                    "clone 1": df[df['clone'] == 1][0],
                    "clone 2": df[df['clone'] == 2][0]
                }, index=df.index)
                import pdb; pdb.set_trace()

                # df_sfs_0.reset_index(level=[1, 2, 3])
                # df_sfs_1.reset_index(level=[1, 2, 3])
                # df_sfs_2.reset_index(level=[1, 2, 3])

                # sfs_list.append(df_sfs)

#                 df_mu_freq.to_excel(
#                     f'/Users/magdalena/PycharmProjects/rice/birth_death/results/{k}x/stats/{k_i}-N-{bd.N}-mu-freq.xlsx')
#                 df_sfs.to_excel(
#                     f'/Users/magdalena/PycharmProjects/rice/birth_death/results/{k}x/stats/{k_i}-N-{bd.N}-sfs.xlsx')

                histograms.sfs(df_sfs)
                plt.savefig(
                    f'/Users/magdalena/PycharmProjects/rice/birth_death/results/{k}x/plots/{k_i}-N-{bd.N}-sfs.png')

        df_cells.to_excel(
            f'/Users/magdalena/PycharmProjects/rice/birth_death/results/{k}x/stats/{k_i}-N-{bd.N}-stats.xlsx')

        # df_mu_occur.to_excel(
        #     f'/Users/magdalena/PycharmProjects/rice/birth_death/results/{k}x/stats/{k_i}-N-{bd.N}-mu-occur.xlsx')
        #
        histograms.cells_life_distribution(df_cells, mean_lifetime)
        plt.savefig(
            f'/Users/magdalena/PycharmProjects/rice/birth_death/results/{k}x/plots/{k_i}-N-{bd.N}-life-distribution.png')

# """
# mean lifetime distribution
# """
# plt.figure()
# plt.hist(mean_lifetimes, density=True, alpha=0.65, bins=15, color='steelblue')
# plt.xlabel('Lifetime')
# plt.ylabel('Frequency')
# plt.title('Mean lifetimes distribution')
# plt.legend(['lifetime', 'density'])
# plt.savefig(f'/Users/magdalena/PycharmProjects/rice/birth_death/results/{k}x/plots/mean-lifetime-distribution.png')
#
# """
# mean sfs
# """
# if sfs_list:
#     mean_sfs = mean_sfs(sfs_list)
#     histograms.sfs(mean_sfs)
#     plt.savefig(f'/Users/magdalena/PycharmProjects/rice/birth_death/results/{k}x/plots/mean-sfs.png')
#
# """
# generate binary tree
# """
# n_extinct = count_extinct_bd(bd_list)
# print(f'Number of extinct processes: {n_extinct}')
#
# """
# plot trajectories
# """
# bd_trajectory.plot_trajectory(bd_list)
# bd_trajectory.plot_mean_and_median(m_dt, df_N)
# bd_trajectory.plot_analytic(m_dt, b, d, N0)
# plt.savefig(f'/Users/magdalena/PycharmProjects/rice/birth_death/results/{k}x/plots/trajectory.png')

"""
plot histogram of N frequency
"""
# histograms.N_freq_in_specific_timesteps(df_N)
# plt.savefig(f'/Users/magdalena/PycharmProjects/rice/birth_death/results/{k}x/plots/N-distribution.png')
# # plt.show()


