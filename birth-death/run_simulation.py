"""
https://cmp.phys.ufl.edu/PHZ4710/files/unit3/birth-death.html
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from birth_death_model import BirthDeath
from plots import bd_trajectory, histograms
from utils import generate_tree, count_extinct_bd, get_tree_paths, get_cell_lifetime_values

"""
set up input parameters
"""

b = 2.
d = 1.
N0 = 1

T = 2.  # total time for running each simulation
k = 1  # number of simulations to repeat
bd_list = []  # list to save all simulations

dt = 0.05
m_dt = np.around(np.arange(0, T + dt, dt), decimals=2)  # time sampling from 0 to T with step 0.05

"""
simulation of continuous-time birth-and-death processes at birth and death event times
"""

for k_i in range(k):
    bd = BirthDeath(b, d, N0)  # create a simulation
    bd.run(T)  # run simulation until time T
    print(f'current time = {bd.t}, current population size = {bd.N}')
    print(f'events: {bd.events}')
    print(f'event time: {bd.t_events}')
    print(f'time history: {bd.t_history}')

    bd_list.append(bd)  # save the simulation in a list

    # create df with N(m_dt): population size at each time point
    # (time points same for all simulations to calculate average N)
    if k_i == 0:
        df = pd.DataFrame(columns=m_dt, index=range(1, k + 1))
        df = df.fillna(0)
    df = bd.count_N_in_timestep(df, k_i + 1, m_dt)

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
    paths = get_tree_paths(tree)
    lifetime_values = get_cell_lifetime_values(tree)
    print(lifetime_values)
    lifetime_values.hist()
    lifetime_values.hist(by=lifetime_values['is_alive'])

    plt.show()
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
