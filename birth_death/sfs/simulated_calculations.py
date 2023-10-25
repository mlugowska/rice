import math
import os
import pdb
from typing import List

import numpy as np
import pandas as pd


def cumulative_simulated_sfs(Sn: List[int], n: int, Kn=None):
    if Kn is None:
        Kn = []
    for k in range(n - 1):
        Sn_nonan = [0 if math.isnan(x) else x for x in Sn]
        K_n_n = sum(Sn_nonan[:k + 1])
        Kn.append(round(K_n_n, 2))
    return Kn


def cumulative_simulated_sfs_Durrett(n: int, mu: float, r: float, N: int) -> List[float]:
    Ekn = []
    for k in range(2, n + 1):
        E_K_n_n = (mu / r) * k * (np.log(N * r) + (1 - (1 / (k - 1))))
        Ekn.append(E_K_n_n)
    return Ekn


def simulated_sfs(n: int, rep: int, set_no: str):
    Sn = []
    PATH = f'/Users/magdalena/PycharmProjects/rice/birth_death/results/{set_no}/{rep}'
    sfs = [file for file in os.listdir(PATH) if 'partial_100_cells.xlsx' in file][0]
    df_sfs = pd.read_excel(f'{PATH}/{sfs}')

    for k in range(1, n):
        Sn_k = df_sfs.loc[df_sfs['Number of cells'] == k]['clone 0']
        if not Sn_k.empty:
            Sn.append(Sn_k.values[0])
        else:
            Sn.append(0)
    return Sn


def simulated_sfs_avg(n: int, set_no: str):
    Sn_all = []
    for k in range(1, n):
        Sn = []
        for rep in range(1, 11):
            PATH = f'/Users/magdalena/PycharmProjects/rice/birth_death/results/{set_no}/{rep}'
            sfs = [file for file in os.listdir(PATH) if 'partial_100_cells.xlsx' in file][0]
            df_sfs = pd.read_excel(f'{PATH}/{sfs}')
            Sn_k = df_sfs.loc[df_sfs['Number of cells'] == k]['clone 0']

            if not Sn_k.empty:
                Sn.append(Sn_k.values[0])
            else:
                Sn.append(0)

        if Sn:
            Sn_avg = sum(Sn) / len(Sn)
            Sn_all.append(round(Sn_avg, 2))
        else:
            Sn_all.append(np.nan)

    return Sn_all
