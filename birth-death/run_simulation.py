"""
https://cmp.phys.ufl.edu/PHZ4710/files/unit3/birth-death.html
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from birth_death_model import BirthDeath
from plots import bd_trajectory, histograms
from utils import generate_tree, count_extinct_bd
from cell_info import Cells

"""
set up input parameters
"""

b = 2.
d = 1.
mu = 1.
N0 = 1

T = 3.  # total time for running each simulation
k = 1  # number of simulations to repeat
bd_list = []  # list to save all simulations
tree_list = []

dt = 0.05
m_dt = np.around(np.arange(0, T + dt, dt), decimals=2)  # time sampling from 0 to T with step 0.05

"""
simulation of continuous-time birth-and-death processes at birth and death event times
"""

for k_i in range(k):
    bd = BirthDeath(b=b, d=d, N0=N0, mu=mu)  # create a simulation
    tree = generate_tree(bd, T, k_i)
    print(f'events: {bd.events}')
    print(f'events times: {bd.t_events}')
    print(f'cell index: {bd.c}')
    print(f'current population size = {bd.N}')
    bd_list.append(bd)  # save the simulation in a list
    tree_list.append(tree)

    # create df with N(m_dt): population size at each time point
    # (time points same for all simulations to calculate average N)
    if k_i == 0:
        df_N = pd.DataFrame(columns=m_dt, index=range(1, k + 1))
        df_N = df_N.fillna(0)
    df_N = bd.count_N_in_timestep(df_N, k_i + 1, m_dt)

"""
generate binary tree
"""
n_extinct = count_extinct_bd(bd_list)
print(f'Number of extinct processes: {n_extinct}')

"""
generate cells statistics
"""
for k_i, bd in enumerate(bd_list):
    tree = tree_list[k_i]
    print(f'Expected number of mutations: {tree.expected_mutations_number()}')

    about_cell = Cells(bd, tree)
    about_cell.add_cells_path()
    about_cell.add_cells_birth_death_time()
    about_cell.add_mutations()
    df = about_cell.create_dataframe()
    print(df[["birth_time", "death_time", 'is_alive']])
    print(f'mean birth: {df.loc[df["birth_time"] != 0.0]["birth_time"].mean(axis=0)}')
    print(f'mean death: {df.loc[df["death_time"] != 0.5]["death_time"].mean(axis=0)}')
    df.to_excel(f'/Users/magdalena/PycharmProjects/rice/birth-death/{k_i + 1}-N-{bd.N}-cells.xlsx')

    df['birth_time'].hist(grid=False, bins=20, alpha=0.5, color='green')
    df['death_time'].hist(grid=False, bins=20, alpha=0.3, color='red')
    plt.legend(['birth_time', 'death_time'])


"""
plot trajectories
"""
bd_trajectory.plot_trajectory(bd_list)
bd_trajectory.plot_mean_and_median(m_dt, df_N)
bd_trajectory.plot_analytic(m_dt, b, d, N0)
plt.show()
#
# """
# plot histogram of N frequency
# """
# histograms.N_freq_in_random_timesteps(df)
# plt.show()
#
