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

T = 5.  # total time for running each simulation
k = 1  # number of simulations to repeat
bd_list = []  # list to save all simulations

# dt = 0.05
# m_dt = np.around(np.arange(0, T + dt, dt), decimals=2)  # time sampling from 0 to T with step 0.05

"""
simulation of continuous-time birth-and-death processes at birth and death event times
"""

for k_i in range(k):
    bd = BirthDeath(b=b, d=d, N0=N0, mu=mu)  # create a simulation
    bd.run(T)  # run simulation until time T
    print(f'current time = {bd.t}, current population size = {bd.N}')
    print(f'events: {bd.events}')
    bd_list.append(bd)  # save the simulation in a list

    # create df with N(m_dt): population size at each time point
    # (time points same for all simulations to calculate average N)
    # if k_i == 0:
    #     df = pd.DataFrame(columns=m_dt, index=range(1, k + 1))
    #     df = df.fillna(0)
    # df = bd.count_N_in_timestep(df, k_i + 1, m_dt)

"""
generate binary tree
"""
n_extinct = count_extinct_bd(bd_list)
print(f'Number of extinct processes: {n_extinct}')

"""
generate binary tree
"""
for k_i, bd in enumerate(bd_list):
    tree = generate_tree(bd, T, k_i)
    print(f'Expected number of mutations: {tree.expected_mutations_number()}')

    about_cell = Cells(bd, tree)
    about_cell.add_cells_path()
    about_cell.add_cells_birth_death_time()
    about_cell.add_mutations()
    df = about_cell.create_dataframe()
    print(df)
    # df.to_excel(f'/Users/magdalena/PycharmProjects/rice/birth-death/{k_i + 1}-N-{bd.N}-cells.xlsx')

"""
plot trajectories
"""
# bd_trajectory.plot_trajectory(bd_list)
# bd_trajectory.plot_mean_and_median(m_dt, df)
# bd_trajectory.plot_analytic(m_dt, b, d, N0)
# plt.show()
#
# """
# plot histogram of N frequency
# """
# histograms.N_freq_in_random_timesteps(df)
# plt.show()
#
