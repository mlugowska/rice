"""
plot simulations with mean and median values
"""
from typing import List

from birth_death_model import BirthDeath
from utils import *

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from numpy import log


def plot_trajectory(bd_list):
    plt.figure()

    for bd in bd_list:
        N = np.asarray(bd.N_history)
        np.seterr(divide='ignore')
        N_log = np.where(N > 0, log(N), 0)
        plt.plot(bd.t_history, N_log, drawstyle='steps-post')  # stochastic realizations

    plt.xlabel('t')
    plt.ylabel('ln(N)')


def plot_mean_and_median(m_dt: np.ndarray, df: pd.DataFrame):
    N_mean_log = calculate_mean_log_bd(df)
    N_median_log = calculate_median_log_bd(df)

    plt.plot(m_dt, N_mean_log, label='mean', color='black')
    plt.plot(m_dt, N_median_log, label='median', color='yellow')
    plt.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left", borderaxespad=0, ncol=3)  # mode='expand'


def plot_analytic(dt: np.ndarray, b, d, N0):
    N = BirthDeath(b, d, N0).analytic(dt=dt)
    plt.plot(dt, log(N), label='analytic', color='brown')


def plot_mean_lifetime_distribution(mean_lifetimes: List[float], filename: str) -> None:
    plt.figure()
    plt.hist(mean_lifetimes, density=True, alpha=0.65, bins=15, color='steelblue')
    plt.xlabel('Lifetime')
    plt.ylabel('Frequency')
    plt.title('Mean lifetimes distribution')
    plt.legend(['lifetime', 'density'])
    plt.savefig(filename, dpi=300)


