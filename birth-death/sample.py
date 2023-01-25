# """
#  :parameter
#     N0: initial population size at time 0
#     lambda_birth: birth rate
#     mu_death: death rate
#     p_birth: lambda / (lambda + mu)
#     p_death: mu / (lambda + mu)
#
#     x: vector that contain the entire history of population sizes
#
# at each step (time interval), the cell either births another, or dies
# """
#
# import numpy as np
# import matplotlib.pyplot as plt
#
#
# lambda_birth = 9
# t = 0
# N = 0
# t_vector = [t]
# N_vector = [N]
#
# tmax = 1000
#
# while t < tmax:
#     # generate an exponential random variable at rate lambda
#     # to determine time of next mutation
#     t = t + np.random.exponential(scale=1/lambda_birth)
#
#     # record count at time before the jump
#     t_vector.append(t)
#     N_vector.append(N)
#
#     # increment count by 1
#     N = N + 1
#
#     # record jump in count at time t
#     t_vector.append(t)
#     N_vector.append(N)
#
#
# plt.plot(t_vector, N_vector)
# plt.ylabel("number of mutations")
# plt.xlabel("time (days)")
# plt.show()
#
#

import dendropy
import matplotlib.pyplot as plt

b = 2
d = 1

tree = dendropy.model.birthdeath.birth_death_tree(b, d, max_time=5.)

tree.print_plot()